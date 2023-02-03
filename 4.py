#Дан лог-файл web-сервера
#консольная утилита, выдающая статистику по данному логу и параметрам

class statistics:
    def __init__(self, filename):
        self.filename = filename
        self.__parts_s = []

        self.__slowest_page_list = {}
        self.__fastest_page_list = {}
        self.__slow_av_page_list = {}
        self.__most_popular_page_list = {}
        self.__most_active_client_list = {}
        self.__most_popular_browser_list = {}
        self.__most_active_client_by_day_list = {}

    def __open_log_file__(self):
        return open(self.filename, 'r', encoding='cp1251', errors='ignore')

    # Самая медленная страница
    def __slowest_page__(self):
        if len(self.__parts_s) > 6 and type(self.__parts_s[-1][-1]) != '\n':
            time_ = int(self.__parts_s[-1][0:-1])
            name = self.__parts_s[6]
            if name in self.__slowest_page_list:
                if self.__slowest_page_list[name] < time_:
                    self.__slowest_page_list[name] = time_
            else:
                self.__slowest_page_list[name] = time_

    # Самая быстрая страница
    def __fastest_page__(self):
        if len(self.__parts_s) > 6 and type(self.__parts_s[-1][-1]) != '\n':
            time_ = int(self.__parts_s[-1][0:-1])
            name = self.__parts_s[6]
            if name in self.__fastest_page_list:
                if self.__fastest_page_list[name] > time_:
                    self.__fastest_page_list[name] = time_
            else:
                self.__fastest_page_list[name] = time_

    # Самая медленная страница в среднем
    def __slowest_average_page(self):
        if len(self.__parts_s) > 6 and type(self.__parts_s[-1][-1]) != '\n':
            time = int(self.__parts_s[-1][0:-1])
            name = self.__parts_s[6]
            if name in self.__slow_av_page_list:
                self.__slow_av_page_list[name][0] += time
                self.__slow_av_page_list[name][1] += 1
            else:
                help_arr = [time, 1]
                self.__slow_av_page_list[name] = help_arr

    # Самая популярная страница
    def __most_popular_page__(self):
        if len(self.__parts_s) > 6:
            name = self.__parts_s[6]
            if name in self.__most_popular_page_list:
                self.__most_popular_page_list[name] += 1
            else:
                self.__most_popular_page_list[name] = 1

    # Самый активный клиент
    def __most_active_client__(self):
        if len(self.__parts_s) > 0:
            client = self.__parts_s[0]
            if client in self.__most_active_client_list:
                self.__most_active_client_list[client] += 1
            else:
                self.__most_active_client_list[client] = 1

    # Самый популярный браузер
    def __most_popular_browser__(self):
        if len(self.__parts_s) > 11:
            i = 12
            browser = self.__parts_s[11][1:]

            while i < len(self.__parts_s) - 1:
                if len(self.__parts_s[i]) > 1 and self.__parts_s[i][-1] != '"':
                    browser += ' ' + self.__parts_s[i]
                else:
                    browser += self.__parts_s[i][:-1]
                i += 1

            if browser in self.__most_popular_browser_list:
                self.__most_popular_browser_list[browser] += 1
            else:
                self.__most_popular_browser_list[browser] = 1

    # Самый активный клиент по дням
    def __most_active_client_by_day__(self):
        if len(self.__parts_s) > 6:
            day_pars = (str(self.__parts_s[3]).split(':')[0][1:]).split('/')

            months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                      'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                      'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

            day = day_pars[2] + '-' + months[day_pars[1]] + '-' + day_pars[0]
            name = self.__parts_s[0]

            if day in self.__most_active_client_by_day_list:
                if name in self.__most_active_client_by_day_list[day]:
                    self.__most_active_client_by_day_list[day][name] += 1
                else:
                    self.__most_active_client_by_day_list[day][name] = 1
            else:
                help_dictionary = {name: 1}
                self.__most_active_client_by_day_list[day] = help_dictionary

    # сбор всех статистик в словари
    def __collection_of_statistics__(self):
        file_handle = self.__open_log_file__()

        for line in file_handle:
            self.__parts_s = line.split(' ')
            self.__slowest_page__()
            self.__fastest_page__()
            self.__slowest_average_page()
            self.__most_popular_page__()
            self.__most_active_client__()
            self.__most_popular_browser__()
            self.__most_active_client_by_day__()

        for key in self.__slow_av_page_list:
            self.__slow_av_page_list[key] = self.__slow_av_page_list[key][0] // \
                                            self.__slow_av_page_list[key][1]

    # сортировка словаря по значениям
    def __sortid_list__(self, List, reverse, k=''):
        sortedList = {}

        sortedkeys = sorted(List, key=List.get, reverse=reverse)
        for w in sortedkeys:
            sortedList[w] = List[w]

        s = list(sortedList.keys())[0]
        sortedkeys.clear()

        for key in sortedList:
            if sortedList[key] == sortedList[s]:
                sortedkeys.append(key)

        if k == '*3':
            sortedkeys.sort()
        return sortedkeys

    def print_statistics(self) -> object:
        self.__collection_of_statistics__()
        print('FastestPage: ' + self.__sortid_list__(self.__fastest_page_list, 0)[-1])
        print('MostActiveClient: ' + self.__sortid_list__(self.__most_active_client_list, 1, '*3')[0])
        print('MostActiveClientByDay: ')
        self.__most_active_client_by_day_list = dict(sorted(self.__most_active_client_by_day_list.items()))
        for day in self.__most_active_client_by_day_list:
            print('   ' + day + ': ' + self.__sortid_list__(self.__most_active_client_by_day_list[day], 1, '*3')[0])
        print()
        print('MostPopularBrowser: ' + self.__sortid_list__(self.__most_popular_browser_list, 1, '*3')[0])
        print('MostPopularPage: ' + self.__sortid_list__(self.__most_popular_page_list, 1, '*3')[0])
        print('SlowestAveragePage: ' + self.__sortid_list__(self.__slow_av_page_list, 1)[0])
        print('SlowestPage: ' + self.__sortid_list__(self.__slowest_page_list, 1)[-1])


if __name__ == '__main__':
    # если запускать с консоли, то
    # my_statistics = statistics(sys.argv[1])

    #start = time.perf_counter()
    #print(start)

    my_statistics = statistics('access.59G.log')
    #my_statistics = statistics('example_3.log')
    my_statistics.print_statistics()

    #print(time.perf_counter() - start)
