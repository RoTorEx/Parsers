from bs4 import BeautifulSoup
import requests


# # Блок запроса у пользователя количества страниц для парсеринга
# num_of_pages = input("Enter number of pages: ")
# if num_of_pages.isdigit():
#     num_of_pages = int(num_of_pages)
# else:
#     num_of_pages = True


def parser():
    x = 0  # Счётчик страниц
    next = ''  # Чтобы flake8 не ругался
    while True:
        if x == 0:
            url = "https://news.ycombinator.com/newest"
        else:
            url = "https://news.ycombinator.com/newest" + next

        # Получаем искомую страницу. Код 200 - успешное получение
        response = requests.get(url)
        # Получаем код всей html страницы
        soup = BeautifulSoup(response.text, "html.parser")
        # Находим все теги с нужным классом на странице
        themes = soup.find_all("td", class_="title")

        for topic in themes:  # Циклом идём по всем тегам поочерёдно из temes
            topic = topic.find("a", {'class': 'titlelink'})
            # Условимся двигатся дальше без None и зададимся конккретным параметром, который мы ищем (github.com)
            if topic is not None and 'github.com' in str(topic):
                # Переменная, которая будет хранить ссылки
                sublink = topic.get('href')
                output = str(topic.text) + " --> " + str(sublink)  # Склеили теми и ссылку
                print(output)  # .text скрывает ссылку, сохраняя заголовок
                print('==< ~ >==')  # Разделитель

        # Заметим, чем отличаются ссылки при переходе на следующие страницы. То есть программа изначально должна
        # попадать на главную страницу, затем глубже, используя кнопку 'More'. Точнее извлекать хвост их ссылки,
        # что лежит внутри данной кнопки, и прибавлять её к изначальной ссылке. И всё это в бесконечном цикле.
        nx = soup.find(class_='morelink')
        nextlink = nx.get('href')
        next = nextlink[6:]
        x += 1


parser()
