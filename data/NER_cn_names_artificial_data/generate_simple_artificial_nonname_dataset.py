
"""
Generate simple Chinese word NER dataset including these cases:
黄河
你好
自行车
"""
import random

PATTERNS= ['{0}']
WORD_COUNT = 20000
OUT_FILE_PREFIX = 'simple_word_'
SEPARATOR = ' '
TAG_OTHER = 'O'
TAG_E_BEGIN = 'B-NAME'
TAG_E_IN = 'I-NAME'
dev_ratio = 0.1
test_ratio = 0.1
dev_file='dev.txt'
test_file='test.txt'
train_file='train.txt'
WORD_CORPUS = 'common_chinese_words.txt'
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

def load_word_words(shuffle=True):
    content = get_file_content(WORD_CORPUS)
    word_list = []
    for word in content.splitlines():
        if word != '':
            word_list.append(word.split('\t'))
    word_list.sort(key=lambda item:int(item[2]))
    word_list = word_list[:WORD_COUNT]
    if shuffle:
        random.shuffle(word_list)
    return word_list

def generate_single(_pattern, word):
    out_str = ''
    for c in _pattern:
        if c == '@':
            for _char in word[0]:
                out_str += _char + SEPARATOR + TAG_OTHER + '\n'
        else:
            out_str += c + SEPARATOR + TAG_OTHER + '\n'
    return out_str

def generate_artificial_dataset(words):
    dataset = []
    for word in words:
        for pattern in PATTERNS:
            _pattern = pattern.format('@', '#')
            dataset.append(generate_single(_pattern, word))
    return dataset

def main():
    random.seed(random_seed)
    words = load_word_words()
    dataset = generate_artificial_dataset(words)
    train, dev, test = split_trainset(dataset)
    write_list(OUT_FILE_PREFIX+train_file, train)
    write_list(OUT_FILE_PREFIX+dev_file, dev)
    write_list(OUT_FILE_PREFIX+test_file, test)


if __name__ == '__main__':
    main()
