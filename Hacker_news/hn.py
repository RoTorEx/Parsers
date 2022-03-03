from bs4 import BeautifulSoup
import requests


url = "https://news.ycombinator.com/newest"

# Получаем искомую страницу. Код 200 - успешное получение
response = requests.get(url)

# Получаем код всей html страницы
soup = BeautifulSoup(response.text, "html.parser")
# print(soup)

# Находим все теги с нужным классом на странице
themes = soup.find_all("td", class_="title")

for topic in themes:  # Циклом идём по всем тегам поочерёдно из temes
    topic = topic.find("a", {'class': 'titlelink'})
    # Условимся двигатся дальше без None и зададимся конккретным параметром, который мы ищем (github.com)
    if topic is not None and 'youtube.com' in str(topic):
        # Это выдаст список всех тем со страницы
        # print(topic.text)
        # Введём переменную, которая уже будет хранить ссылки
        sublink = topic.get('href')
        print('===< ~ >===')  # Просто разделитель статей
        # Склеиваем тему с полученной ссылкой
        print('\n' + str(topic.text) + " --> " + str(sublink) + '\n')  # .text скрывает ссылку, сохраняя только нужный текст
else:
    print('==< ~ >===')  # Так же разделитель для красоты вывода :)
