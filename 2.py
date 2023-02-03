#парсинг страницы html с ее локальным сохранением

#!/usr/bin/env python3
from urllib.request import urlopen
from collections import Counter


def sorting_into_boys_and_girls(name, Lastname):
    if name[-1] == 'а' or name[-1] == 'я' or Lastname[-1] == 'а':
        key = 'W'
    else:
        key = 'M'

    if name[-1] == 'й' or name == 'Илья' or name == 'Лёва':
        key = 'M'
    if name[-1] == 'л' or name[-1] == 'м' or name[-1] == 'р':
        key = 'M'
    if name == 'Никита' or name == 'Алехандро':
        key = 'M'
    return key


def sostid_arr(List):
    sortedList = {}
    sortedkeys = sorted(List, key=List.get, reverse=True)
    for w in sortedkeys:
        sortedList[w] = List[w]

    arr = []
    for key in sortedList.keys():
        arr.append((key, sortedList[key],))
    ans = tuple(arr)

    return ans


def make_stat(filename):
    with urlopen(filename) as resp:
        page = resp.read().decode('cp1251')
        print(page)
        pos_year = 0
        pos_name = 0
        statistic = {}
        nameW = []
        nameM = []

        while True:
            start_name = page.find('/>', pos_name)
            start_year = page.find('<h3>', pos_year)
            dop_Start_year = page.find('<h3>', start_year + 2)
            if dop_Start_year == -1:
                dop_Start_year = 50000

            if start_year < start_name < dop_Start_year and start_name != -1:

                end_name = page.find('</a', start_name)
                name = page[start_name + 2:end_name].split(' ')[1]
                lastname = page[start_name + 2:end_name].split(' ')[0]

                if sorting_into_boys_and_girls(name, lastname) == 'W':
                    nameW.append(name)
                else:
                    nameM.append(name)
                pos_name = end_name
            else:
                if start_name == -1 and start_year == -1:
                    break

                end_year = page.find('</h3', start_year)
                year = page[start_year + 4:end_year]
                pos_year = end_year

                if dop_Start_year == 50000:
                    year = '2004'
                    start_year = -1

                nameW_dict = {}
                nameM_dict = {}
                names_dict = {}

                for name in nameW:
                    if name in nameW_dict:
                        nameW_dict[name] += 1
                    else:
                        nameW_dict[name] = 1

                for name in nameM:
                    if name in nameM_dict:
                        nameM_dict[name] += 1
                    else:
                        nameM_dict[name] = 1

                names_dict['W'] = nameW_dict
                names_dict['M'] = nameM_dict
                statistic[year] = names_dict
                nameM.clear()
                nameW.clear()
    return statistic


def extract_years(stat):
    List = []
    for year in stat.keys():
        List = [year] + List
    return List


def extract_general(stat):
    List = {}
    BigList = []
    for year in stat.keys():
        for gender in stat[year].keys():
            for name in stat[year][gender].keys():
                for i in range(stat[year][gender][name]):
                    BigList.append(name)

    for name in BigList:
        if name in List:
            List[name] += 1
        else:
            List[name] = 1
    return sostid_arr(List)


def extract_general_male(stat):
    List = {}
    BigList = []
    for year in stat.keys():
        for name in stat[year]['M'].keys():
            for i in range(stat[year]['M'][name]):
                BigList.append(name)

    for name in BigList:
        if name in List:
            List[name] += 1
        else:
            List[name] = 1
    return sostid_arr(List)


def extract_general_female(stat):
    List = {}
    BigList = []
    for year in stat.keys():
        for name in stat[year]['W'].keys():
            for i in range(stat[year]['W'][name]):
                BigList.append(name)

    for name in BigList:
        if name in List:
            List[name] += 1
        else:
            List[name] = 1
    return sostid_arr(List)


def extract_year(stat, year):
    List = {}
    for gender in stat[year].keys():
        for name in stat[year][gender].keys():
            List[name] = stat[year][gender][name]
    return sostid_arr(List)


def extract_year_male(stat, year):
    List = {}
    for name in stat[year]['M'].keys():
        List[name] = stat[year]['M'][name]
    return sostid_arr(List)


def extract_year_female(stat, year):
    List = {}
    for name in stat[year]['W'].keys():
        List[name] = stat[year]['W'][name]
    return sostid_arr(List)


if __name__ == '__main__':
    sp = make_stat('http://shannon.usu.edu.ru/ftp/python/hw2/home.html')
    print(sp)
    print(extract_years(sp))
    print(extract_general(sp))
    print(extract_general_male(sp))
    print(extract_general_female(sp))
    print(extract_year(sp, '2010'))
    print(extract_year_male(sp, '2010'))
    print(extract_year_female(sp, '2010'))