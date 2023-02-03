# «из любой статьи на русской Википедии можно за несколько шагов перейти в статью „Философия“»
#парсинг страниц вики -> изьятие кликабильных ссылок на страницы сики -> нахождение пути от заданной страницы до страницы Философия

#!/usr/bin/env python3
import collections
import re
from urllib.error import URLError, HTTPError
from urllib.parse import quote
from urllib.parse import unquote
from urllib.request import urlopen
import sys


def get_content(name):
    try:
        with urlopen('http://ru.wikipedia.org/wiki/' + quote(name)) as resp:
            return resp.read().decode('utf-8')
    except (URLError, HTTPError):
        return None


def extract_content(page):
    if page is None:
        return 0, 0,
    begin = page.find('class="firstHeading mw-first-heading">', 0)
    if begin == -1:
        return 0, 0,
    end = page.find('cats-hidden">Скрытые категории:', 0) - 1
    return begin, end,


def extract_links(page, begin, end):
    if begin == end == 0:
        return None
    linkList = re.findall(r"/wiki[^>\"#: -]+[\"\']", page[begin:end])
    fullLinkList = []
    for i in range(len(linkList)):
        ext = ['.JPG', '.jpg', '.png', 'webm', 'jpeg', 'JPEG', '.gif', '.PNG']
        if linkList[i][-5:-1] not in ext and linkList[i][6:10] != 'edia':
            name = unquote(linkList[i][6:-1])
            if name not in fullLinkList:
                fullLinkList.append(name)
    return fullLinkList


def getting_list(name):
    content = get_content(name)
    if content is None:
        return None
    begin, end = extract_content(content)
    return extract_links(content, begin, end)


def find_chain(start, finish):
    global name2
    tree = {}
    name = start
    tek_arr = getting_list(start)

    if tek_arr is None:
        return None
    tree[name] = tek_arr
    name = tek_arr[0]
    k = 0

    while finish not in tek_arr:
        if k == len(tek_arr) or len(tek_arr) == 0:
            k = 0
            [name] = collections.deque(tree, maxlen=1)
            tek_arr = tree[name]
            tree[name].clear()

        name = tek_arr[k]
        if name not in tree and name.capitalize() not in tree:
            tek_arr = getting_list(name)
            if tek_arr is None:
                k += 1
                [name] = collections.deque(tree, maxlen=1)
                tek_arr = tree[name]
                name = tek_arr[k]
                continue
            tree[name] = tek_arr
            k = 0
        else:
            k += 1

    way = [finish]
    if name in tree:
        tree.pop(name)
        while name != start:
            way.insert(0, name)
            tek_arr = []
            while name not in tek_arr:
                [name2] = collections.deque(tree, maxlen=1)
                tek_arr = tree[name2]
                tree.pop(name2)
            name = name2
    way.insert(0, start)
    return way


def main():
    pass
    x = sys.argv
    #for i in x:
    #    print(find_chain(i, 'Философия'))


if __name__ == '__main__':
    main()
