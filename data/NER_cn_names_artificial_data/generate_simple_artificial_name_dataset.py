
"""
Generate simple Chinese name NER dataset including these cases:
刘丽华
我是刘丽华
我叫刘丽华
我就是刘丽华
我姓刘
叫我刘丽华吧
就叫我刘丽华吧
"""
import random

PATTERNS= ['{0}', '我是{0}', '我叫{0}', '我就是{0}', '我姓{1}', '叫我{0}吧']
NAME_COUNT = 10000
OUT_FILE_PREFIX = 'simple_name_'
SEPARATOR = ' '
TAG_OTHER = 'O'
TAG_E_BEGIN = 'B-NAME'
TAG_E_IN = 'I-NAME'
dev_ratio = 0.1
test_ratio = 0.1
dev_file='dev.txt'
test_file='test.txt'
train_file='train.txt'
NAME_CORPUS = 'Chinese_Names_Corpus120W.txt'
random_seed = 3298482349

def get_file_content(path, encoding='utf-8'):
    f = open(path, encoding=encoding)
    content = f.read()
    f.close()
    return content

def write_to_file(path, content, encoding='utf-8'):
    f = open(path, 'w', encoding=encoding)
    f.write(content)
    f.close()

def write_list(file, _list):
    out_str = '\n'.join(_list)
    write_to_file(file, out_str)
    print('{} records written to {}'.format(len(_list), file))


def split_trainset(train_list):
    count = len(train_list)
    dev_count = int(count * dev_ratio)
    test_count = int(count * test_ratio)
    train = train_list[:count - dev_count - test_count]
    dev = train_list[count - dev_count - test_count : count - test_count]
    test = train_list[count-test_count:]
    return train, dev, test

def load_names(shuffle=True):
    content = get_file_content(NAME_CORPUS)
    name_list = []
    for name in content.splitlines():
        if name != '':
            name_list.append(name)
    if shuffle:
        random.shuffle(name_list)
    return name_list

def generate_single(_pattern, name):
    out_str = ''
    family_name = name[0]
    for c in _pattern:
        if c == '@' or c == '#':
            name_str = name
            if c == '#':
                name_str = family_name
            is_first = True
            for _char in name_str:
                tag = TAG_E_IN
                if is_first:
                    is_first = False
                    tag = TAG_E_BEGIN
                out_str += _char + SEPARATOR + tag + '\n'
        else:
            out_str += c + SEPARATOR + TAG_OTHER + '\n'
    return out_str

def generate_artificial_dataset(names):
    dataset = []
    for name in names:
        for pattern in PATTERNS:
            _pattern = pattern.format('@', '#')
            dataset.append(generate_single(_pattern, name))

    return dataset

def main():
    random.seed(random_seed)
    names = load_names()
    names = names[:NAME_COUNT]
    dataset = generate_artificial_dataset(names)
    train, dev, test = split_trainset(dataset)
    write_list(OUT_FILE_PREFIX+train_file, train)
    write_list(OUT_FILE_PREFIX+dev_file, dev)
    write_list(OUT_FILE_PREFIX+test_file, test)


if __name__ == '__main__':
    main()
