
import os
import re

NEWS_DIRECTORY = 'news'
content_reg = re.compile('<content>([^<>]+)</content>')
OUT_FILE = 'news_extraction.txt'
MIN_LEN = 100

def get_file_content(path, encoding='utf-8'):
    f = open(path, encoding=encoding)
    content = f.read()
    f.close()
    return content

def write_to_file(path, content, encoding='utf-8'):
    f = open(path, 'w', encoding=encoding)
    f.write(content)
    f.close()

def load_path(path, out_list):
    content = get_file_content(path, encoding='gb18030')
    for article in content_reg.findall(content):
        if len(article) > MIN_LEN:
            out_list.append(article)

def load_directory(directory):
    out_list = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            load_path(path, out_list)
    return out_list

def main():
    out_list = load_directory(NEWS_DIRECTORY)
    out_str = '\n'.join(out_list)
    write_to_file(OUT_FILE, out_str)
    print('{} articles, {} characters, written to {}'.format(len(out_list), len(out_str), OUT_FILE))

if __name__ == '__main__':
    main()

