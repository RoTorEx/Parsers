from bs4 import BeautifulSoup
import requests


url = "https://career.habr.com/vacancies?q=python&sort=date&type=all"

response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, "html.parser")

themes = soup.find_all('div', class_='vacancy-card__info')

for theme in themes:  # разбор каждой вакансии на странице по кусочкам
    # Компания
    company = theme.find('div', {'class': "vacancy-card__company-title"}).text

    # Тема
    topic = theme.find('a', {'class': "vacancy-card__title-link"})

    # Список скилов
    skills = theme.find('div', {'class': "vacancy-card__skills"}).text.split(' • ')
    if 'Python' in skills and 'удаленно' not in str(topic):
        sublink = "https://career.habr.com/" + topic.get('href')
        # print(topic.text, skills)
        print('==< ~ >==')  # Разделитель
