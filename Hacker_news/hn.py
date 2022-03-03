from bs4 import BeautifulSoup
import requests


url = "https://news.ycombinator.com/newest"

# Получаем искомую страницу. Код 200 - успешное получение
response = requests.get(url)

# Получаем код всей html страницы
soup = BeautifulSoup(response.text, "html.parser")
# print(soup)

# Находим все теги с нужным классом на странице
temes = soup.find_all("td", class_="title")

for teme in temes:  # Циклом идём по всем тегам поочерёдно из temes
    teme = temes.find("a", {'class': 'titlelink'})  #
    # print(teme)

    # Создадим условие, где

