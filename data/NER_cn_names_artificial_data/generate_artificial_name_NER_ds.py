
import os
import random

NAME_FILE = 'Chinese_Names_Corpus120W.txt'
ARTICLE_FILE = 'news_extraction.txt'

SEPARATOR = ' '
TAG_OTHER = 'O'
TAG_E_BEGIN = 'B-NAME'
TAG_E_IN = 'I-NAME'
dev_ratio = 0.1
test_ratio = 0.1
train_file = 'train.txt'
dev_file = 'dev.txt'
test_file = 'test.txt'
MIN_ARTICLE_LENGTH = 20
MAX_CHAR_PER_LINE = 45
MAX_ARTICLES_NEEDED = 300


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
    content = get_file_content(NAME_FILE)
    name_list = []
    for name in content.splitlines():
        if name != '':
            name_list.append(name)
    if shuffle:
        random.shuffle(name_list)
    return name_list

def load_articles(shuffle=True):
    content = get_file_content(ARTICLE_FILE)
    article_list = []
    for article in content.splitlines():
        if len(article) > MIN_ARTICLE_LENGTH:
            article_list.append(article)
    if shuffle:
        random.shuffle(article_list)
    return article_list

def assign_names_to_articles(names, articles):
    print('names: {}, articles: {}'.format(len(names), len(articles)))

    batch_size = len(names)/len(articles)
    if batch_size > int(batch_size):
        batch_size = int(batch_size) + 1
    else:
        batch_size = int(batch_size)
    name_batches = []
    for i in range(len(names)//batch_size):
        name_batches.append(names[i*batch_size:(i+1)*batch_size])
    print('names per article: ', batch_size)
    if batch_size >= MIN_ARTICLE_LENGTH:
        print('WARNING: batch_size >= MIN_ARTICLE_LENGTH')

    selected = []
    random.shuffle(articles)
    for i in range(len(name_batches)):
        selected.append((articles[i], name_batches[i]))
    return selected

def insert_normal_word(c):
    return c + SEPARATOR + TAG_OTHER + '\n'

def insert_name(name):
    s = ''
    is_first = True
    for c in name:
        if is_first:
            tag = TAG_E_BEGIN
            is_first = False
        else:
            tag = TAG_E_IN
        s += c + SEPARATOR + tag + '\n'
    return s

# Insert several names into one article at random positions.
def insert_names_into_article(article, names):
    out_str = ''
    insert_pos = set(random.sample(range(len(article)), len(names)))
    current_name_index = 0
    char_count = 0
    for i, c in enumerate(article):
        if i in insert_pos:
            out_str += insert_name(names[current_name_index])
            char_count += len(names[current_name_index])
            current_name_index += 1
        if not c.isspace():
            out_str += insert_normal_word(c)
            char_count += 1
        if char_count > MAX_CHAR_PER_LINE:
            char_count = 0
            out_str += '\n'
    return out_str

def generate_tag_files(selected):
    output_list = []
    count = 0
    for article, names in selected:
        if len(names) > 0:
            new_article = insert_names_into_article(article, names)
            output_list.append(new_article)
            count += 1
        if count > MAX_ARTICLES_NEEDED:
            print('Max articles count reached, stop generating.')
            break
    train, dev, test = split_trainset(output_list)
    write_list(train_file, train)
    write_list(dev_file, dev)
    write_list(test_file, test)

def main():
    random.seed(42)
    names = load_names()
    articles = load_articles()
    selected = assign_names_to_articles(names, articles)
    generate_tag_files(selected)

if __name__ == '__main__':
    main()
