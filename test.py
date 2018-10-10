# coding: utf-8
f = open('input_names.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
from inference_helper import InferenceHelper
infer_helper = InferenceHelper()
#infer_helper.init(model_path='models/NER_cn_names_artificial_data_0.9830_0.9821_14.h5', mode='name', timeit=False, mute=False)
infer_helper.init(model_path='models/NER_cn_names_artificial_data_0.9632_0.9640_10.h5', mode='name', timeit=False, mute=False)
def infer(s):
    _ = infer_helper.infer(s)
