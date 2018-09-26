
"""
Sample input: {{product_name:浙江在线杭州}}{{time:4月25日}}讯（记者{{person_name: 施宇翔}} 通讯员 {{person_name:方英}}）毒贩很“时髦”，用{{product_name:微信}}交易毒品。没料想警方也很“潮”，将计就计，一举将其擒获。记者从{{org_name:杭州江干区公安分局}}了解到，经过一个多月的侦查工作，{{org_name:江干区禁毒专案组}}抓获吸贩毒人员5名，缴获“冰毒”400余克，毒资30000余元，扣押汽车一辆。{{location:黑龙江}}籍男子{{person_name:钱某}}长期落脚于宾馆、单身公寓，经常变换住址。他有一辆车，经常半夜驾车来往于{{location:杭州主城区}}的各大宾馆和单身公寓，并且常要活动到{{time:凌晨6、7点钟}}，{{time:白天}}则在家里呼呼大睡。{{person_name:钱某}}不寻常的特征，引起了警方注意。禁毒大队通过侦查，发现{{person_name:钱某}}实际上是在向落脚于宾馆和单身公寓的吸毒人员贩送“冰毒”。

Sample output:
浙 B-PRODUCT_NAME
江 I-PRODUCT_NAME
..
毒 O
贩 O
...
"""

import re

fast_extraction_pattern = '\\{\\{([^{:]+):([^:}]+)\\}\\}'
fast_extraction = re.compile(fast_extraction_pattern)
ORIGINAL_FILE = 'BosonNLP_NER_6C.txt'
SEPARATOR = ' '
TAG_OTHER = 'O'
TAG_E_BEGIN_PREFIX = 'B-'
TAG_E_IN_PREFIX = 'I-'
starting_digits = set('0123456789零一二三四五六七八九两')
normal_digits = set('0123456789零一二三四五六七八九两-\\年月日时分秒十百千万亿')
out_file = 'test_output.txt'
dev_ratio = 0.1
test_ratio = 0.1
train_file = 'train.txt'
dev_file = 'dev.txt'
test_file = 'test.txt'

def get_file_content(path, encoding='utf-8'):
    f = open(path, encoding=encoding)
    content = f.read()
    f.close()
    return content

def write_to_file(path, content, encoding='utf-8'):
    f = open(path, 'w', encoding=encoding)
    f.write(content)
    f.close()

def split_trainset(train_list):
    count = len(train_list)
    dev_count = int(count * dev_ratio)
    test_count = int(count * test_ratio)
    train = train_list[:count - dev_count - test_count]
    dev = train_list[count - dev_count - test_count : count - test_count]
    test = train_list[count-test_count:]
    return train, dev, test

def write_list(file, _list):
    out_str = '\n'.join(_list)
    write_to_file(file, out_str)
    print('{} records written to {}'.format(len(_list), file))

def test():
    content = get_file_content(ORIGINAL_FILE)
    types = set()
    out_list = []
    current = 0
    line_count = 0
    for line in content.splitlines():
        line_count += 1
        groups = []
        sample_out_list = []
        for m in fast_extraction.finditer(line):
            #print(key, ':', value)
            #print(line[m.start():m.end()], ':', m.group(1), ',', m.group(2))
            types.add(m.group(1))
            if current < m.start():
                groups.append(('o', current, m.start(), None, None))
            current = m.end()
            groups.append(('e', m.start(), m.end(), m.group(2), m.group(1)))
        if current < len(line):
            groups.append(('o', current, m.start(), None, None))
        for tag_type, start_index, end_index, entity, tag_name in groups:
            if tag_type == 'o':
                for i in range(start_index, end_index):
                    sample_out_list.append(line[i] + SEPARATOR + TAG_OTHER)
            else:
                # naive implementation
                tag_begin = TAG_E_BEGIN_PREFIX + tag_name.upper().replace('_', '')
                tag_in = TAG_E_IN_PREFIX + tag_name.upper().replace('_', '')
                is_first = True
                for c in entity:
                    if is_first:
                        tag = tag_begin
                        is_first = False
                    else:
                        tag = tag_in
                    sample_out_list.append(c + SEPARATOR + tag)
        line_output = '\n'.join(sample_out_list)
        #print(line_output)
        out_list.append(line_output)
    train, dev, test = split_trainset(out_list)
    write_list(train_file, train)
    write_list(dev_file, dev)
    write_list(test_file, test)
    #out_str = '\n'.join(out_list)
    #print(out_str)
    
    #write_to_file(out_file, out_str)

    #print('line_count = ', line_count)
    print(types)

if __name__ == '__main__':
    test()