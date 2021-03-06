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

if len(sys.argv) < 3:
    print("Usage: python RunModel.py modelPath inputPath")
    exit()

modelPath = sys.argv[1]
inputPath = sys.argv[2]
is_chinese = False
is_name_recognition = False
is_timeit_mode = False
if len(sys.argv) > 3 and sys.argv[3] == 'cn':
    is_chinese = True
if len(sys.argv) > 3 and sys.argv[3] == 'name':
    is_name_recognition = True
if len(sys.argv) > 4 and sys.argv[4] == 'timeit':
    is_timeit_mode = True

def cn_word_segmentation(text):
    out_text = ''
    import jieba
    for line in text.splitlines():
        line_out = ' '.join(list(jieba.cut(line)))
        out_text += line_out + '\n'
    return out_text

# :: Read input ::
with open(inputPath, 'r', encoding='utf8') as f:
    text = f.read()
if is_chinese:
    text = cn_word_segmentation(text)
    print('Chinese mode. Segemented text:')
    print(text)
if is_name_recognition:
    print('Name mode.')
    text = ' '.join(text)

# :: Load the model ::
lstmModel = BiLSTM.loadModel(modelPath)


# :: Prepare the input ::
sentences = [{'tokens': nltk.word_tokenize(sent)} for sent in nltk.sent_tokenize(text)]
addCharInformation(sentences)
addCasingInformation(sentences)
dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

# :: Tag the input ::
tags = lstmModel.tagSentences(dataMatrix)
if is_timeit_mode:
    print('timeit mode:')
    import time
    test_count = 100
    start_time = time.time()
    for i in range(test_count):
        tags = lstmModel.tagSentences(dataMatrix)
    elapsed = time.time() - start_time
    print('test_count = {}, avg time = {}'.format(test_count, elapsed/test_count))
        

# :: Output to stdout ::
for sentenceIdx in range(len(sentences)):
    tokens = sentences[sentenceIdx]['tokens']

    for tokenIdx in range(len(tokens)):
        tokenTags = []
        for modelName in sorted(tags.keys()):
            tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

        print("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)))
    print("")