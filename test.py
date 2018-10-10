# coding: utf-8
f = open('input_names.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
from inference_helper import InferenceHelper
infer_helper = InferenceHelper()
infer_helper.init(model_path='models/NER_cn_names_artificial_data_0.9830_0.9821_14.h5', mode='name', timeit=False, mute=True)
#infer_helper.init(model_path='models/NER_cn_names_artificial_data_0.9740_0.9727_3.h5', mode='name', timeit=False, mute=True)

def infer(s):
    sentences, tags = infer_helper.infer(s)
    
    if len(sentences) > 0 and len(tags.keys()) > 0:
        tokens = sentences[0]['tokens']
        bios = tags[list(tags.keys())[0]][0]

        out_str = ''
        name = ''
        for i in range(len(tokens)):
            c = tokens[i]
            if name == '':
                if bios[i] == 'B-NAME':
                    name += c
                    out_str += '['
                out_str += c
            elif bios[i] == 'I-NAME':
                name += c
                out_str += c
            else:
                out_str += ']' + c
                name = ''
        if name != '':
            out_str += ']'
        print(out_str)
