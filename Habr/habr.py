#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os


def exit(exit_message):
    print(f'\n{exit_message}')
    os._exit(0)


def habr_parser(cnt, circs, file_write):
    # Полная ссылка на первую страницу - "https://career.habr.com/vacancies?page=1&q=python&sort=date&type=all"
    # Забиваем ссылку, чтобы потом туда вклеивать стараницу
    url_1 = "https://career.habr.com/vacancies?page="
    url_2 = "&q=python&sort=date&type=all"

    # Имя пути этого парсера для удаления / сохранении текстового файла при запуске парсера
    dir = os.path.split(__file__)

    # Удаляет файл vacancy.txt, если он есть
    try:
        os.remove(dir[0] + "/vacancy.txt")
    except FileNotFoundError:
        pass

    # Бесконечный цикл поиска вакансий
    while True:
        url = url_1 + str(cnt) + url_2
        # Ответ страницы - ожидаем [200]
        response = requests.get(url)
        # Имя для полученной страницы
        soup = BeautifulSoup(response.text, "html.parser")
        # Блоки вакансий
        themes = soup.find_all('div', class_='vacancy-card')

        # Проверка страницы на наличии ваканский
        if not bool(themes):
            exit('Jobs run out.')

        # Разбор каждой вакансии
        for theme in themes:
            # Дата
            date = theme.find('time', {'class': "basic-date"}).text
            # Компания
            company = theme.find('div', {'class': "vacancy-card__company-title"}).text
            # Тема
            title = theme.find('a', {'class': "vacancy-card__title-link"})
            # Инфо
            info = theme.find('div', {'class': "vacancy-card__meta"}).text.split(' • ')
            # Зарплата
            salary = theme.find('div', {'class': "vacancy-card__salary"}).text.strip()
            # Скилы
            skills = theme.find('div', {'class': "vacancy-card__skills"}).text.split(' • ')
            # Ссылка
            link = "https://career.habr.com/" + title.get('href')

            # Проверяем вакансию по ряду условий
            if 'удаленно' not in title:  # На актуальность

                # Проверка на 'Python' и на перечень условий в circs
                if 'Python' in skills and any([item for item in info if item in circs]):

                    # Два кортежа на ввывод информации
                    out_list = ('Date', 'Company', 'Title', 'Info', 'Salary', 'Skills', 'Link')
                    theme_list = (date, company, title.text, ' '.join(info), salary, ' '.join(skills), link)

                    # Блок (не) вывода в файл
                    if file_write:

                        mode = {1: 'a+', 2: 'w'}
                        # Менеджер контекста для записи в текстовый файл всех вакансий
                        # конструкция dir[0] нужна для записи документа в папку скрипта при любом его запуске
                        # mode[ ] задаёт тип работы с файлом
                        with open(dir[0] + '/vacancy.txt', mode[1], encoding='utf-8') as vac:
                            print('==< ~ >==', file=vac)  # Разделитель

                            # Вывод через двойной перебор в цикле
                            for left, right in zip(out_list, theme_list):
                                print(left.ljust(7) + ' | ' + (right if bool(right) else 'None'), file=vac)

                    else:
                        print('==< ~ >==')  # Разделитель
                        # Вывод через двойной перебор в цикле
                        for left, right in zip(out_list, theme_list):
                            print(left.ljust(7) + ' | ' + (right if bool(right) else 'None'))
        cnt += 1  # Повышает страницу в цикле


# Начальный номер страницы
page_counter = 1
# Поиск по уловиям работы
circs = ('Минск', 'Можно удаленно')
# Нужна ли запись вакансий в отдельный файл. True - запись в файл, False - вывод в Terminal
file_write = True


try:
    habr_parser(page_counter, circs, file_write)
except (KeyboardInterrupt, EOFError):
    exit(">>> WARNING! Forced termination of a job search... <<<")
