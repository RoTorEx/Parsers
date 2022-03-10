#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os


def exit(exit_message):
    print(f'\n{exit_message}')
    os._exit(0)


def belmeta_parser(cnt, circs, file_write):

    # Полная ссылка на первую страницу - "https://belmeta.com/vacansii?q=python&sort=date&page=1"
    # Разбиваем ссылку, чтобы потом туда вклеить номер страницы
    pre_url = "https://belmeta.com/vacansii?q=python&sort=date&page="

    # Имя пути этого парсера для удаления / сохранении текстового файла при запуске парсера
    dir = os.path.split(__file__)
    # Удаляет файл vacancy.txt, если он есть
    try:
        os.remove(dir[0] + "/vacancy.txt")
    except FileNotFoundError:
        pass

    # Бесконечный цикл поиска вакансий
    while True:
        url = pre_url + str(cnt)
        # Ответ страницы - ожидаем [200]
        response = requests.get(url)
        # Имя для полученной страницы
        soup = BeautifulSoup(response.text, "html.parser")
        # Блоки вакансий
        themes = soup.find_all('article', class_='job no-logo')

        # Проверка страницы на наличии ваканский
        if not bool(themes):
            exit('Jobs run out.')

        # Разбор каждой вакансии
        for theme in themes:
            # Дата
            pre_date = theme.find('span', {'class': "days"}).get('data-value')
            date = pre_date[:2] + '.' + pre_date[3:5] + '.' + pre_date[6:10]
            # Компания
            company = theme.find('div', {'class': "job-data company"}).text.strip()
            # Тема
            title = theme.find('h2', {'class': "title"}).text.strip()
            # Инфо
            info = theme.find('div', {'class': "job-data region"})
            if info is not None:
                info = info.text.strip()
            # Зарплата
            salary = theme.find('div', {'class': "job-data salary"})
            if salary is not None:
                salary = salary.text.strip()
            # Ссылка
            link = "https://belmeta.com" + theme.find('a', {'rel': "nofollow"}).get('href')

            # Два кортежа на ввывод информации
            out_list = ['Date', 'Company', 'Title', 'Info', 'Salary', 'Link']
            theme_list = [date, company, title, info, salary, link]

            # Проверяем вакансию по ряду условий
            if any([item for item in circs if item in title]):

                # Блок (не) вывода в файл
                if file_write:
                    # Менеджер контекста для записи в текстовый файл всех вакансий
                    # конструкция dir[0] нужна для записи документа в папку скрипта при любом его запуске
                    with open(dir[0] + '/vacancy.txt', 'a+', encoding='utf-8') as vac:
                        print('==< ~ >==', file=vac)  # Разделитель

                        # Вывод через двойной перебор в цикле
                        for left, right in zip(out_list, theme_list):
                            print(left.ljust(7) + ' | ' + str(right if bool(right) else 'None'), file=vac)

                else:
                    print('==< ~ >==')  # Разделитель
                    # Вывод через двойной перебор в цикле
                    for left, right in zip(out_list, theme_list):
                        print(left.ljust(7) + ' | ' + str(right if bool(right) else 'None'))
        cnt += 1  # +1 к странице


# Начальный номер страницы
page_counter = 1
# Отбор по специлизации
circs = ('Python', 'Intern', 'Trainee', 'DevOps')
# Нужна ли запись вакансий в отдельный файл. True - запись в файл, False - вывод в Terminal
file_write = True


try:
    belmeta_parser(page_counter, circs, file_write)
except (KeyboardInterrupt, EOFError):
    exit(">>> WARNING! Forced termination of a job search... <<<")
