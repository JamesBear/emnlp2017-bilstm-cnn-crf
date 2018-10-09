# coding: utf-8
f = open('input_names.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
from inference_helper import InferenceHelper
infer_helper = InferenceHelper()
infer_helper.init(model_path='models/NER_cn_names_artificial_data_0.9009_0.9036_1.h5', mode='name', timeit=False)
