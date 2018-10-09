#!/usr/bin/python
# This scripts loads a pretrained model and a raw .txt files. It then performs sentence splitting and tokenization and passes
# the input sentences to the model for tagging. Prints the tokens and the tags in a CoNLL format to stdout
# Usage: python RunModel.py modelPath inputPath
# For pretrained models see docs/Pretrained_Models.md
from __future__ import print_function
import nltk
from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM
import sys

#if len(sys.argv) < 3:
#    print("Usage: python RunModel.py modelPath inputPath")
#    exit()


def cn_word_segmentation(text):
    out_text = ''
    import jieba
    for line in text.splitlines():
        line_out = ' '.join(list(jieba.cut(line)))
        out_text += line_out + '\n'
    return out_text

class InferenceHelper:
    def __init__(self):
        pass

    def init(self, model_path, mode='cn', timeit=False, mute=True):
        self.is_chinese = False
        self.is_name_recognition = False
        self.is_timeit_mode = False
        if mode == 'cn':
            self.is_chinese = True
        if mode == 'name':
            self.is_name_recognition = True
        if timeit:
            self.is_timeit_mode = True
        self.mute = mute

        # :: Load the model ::
        self.lstmModel = BiLSTM.loadModel(model_path)

    def infer(self, text):
        if self.is_chinese:
            text = cn_word_segmentation(text)
            if not self.mute:
                print('Chinese mode. Segemented text:')
                print(text)
        if self.is_name_recognition:
            if not self.mute:
                print('Name mode.')
            text = ' '.join(text)

        # :: Prepare the input ::
        sentences = [{'tokens': nltk.word_tokenize(sent)} for sent in nltk.sent_tokenize(text)]
        addCharInformation(sentences)
        addCasingInformation(sentences)
        dataMatrix = createMatrices(sentences, self.lstmModel.mappings, True)

        # :: Tag the input ::
        tags = self.lstmModel.tagSentences(dataMatrix)
        if self.is_timeit_mode:
            print('timeit mode:')
            import time
            test_count = 100
            start_time = time.time()
            for i in range(test_count):
                tags = self.lstmModel.tagSentences(dataMatrix)
            elapsed = time.time() - start_time
            print('test_count = {}, avg time = {}'.format(test_count, elapsed/test_count))
        

        if not self.mute:
            # :: Output to stdout ::
            for sentenceIdx in range(len(sentences)):
                tokens = sentences[sentenceIdx]['tokens']

                for tokenIdx in range(len(tokens)):
                    tokenTags = []
                    for modelName in sorted(tags.keys()):
                        tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

                    print("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)))
                print("")

        return sentences, tags