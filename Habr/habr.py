from bs4 import BeautifulSoup
import requests


cnt = 0

url = "https://career.habr.com/vacancies?q=python&sort=date&type=all"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

themes = soup.find_all('div', class_='vacancy-card__info')

terms_info = ('Можно удаленно', 'Минск')

for theme in themes:  # разбор каждой вакансии на странице по кусочкам
    # Компания
    company = theme.find('div', {'class': "vacancy-card__company-title"}).text

    # Тема
    title = theme.find('a', {'class': "vacancy-card__title-link"})

    # Инфо
    info = theme.find('div', {'class': "vacancy-card__meta"}).text.split(' • ')

    # зарплата
    # salary = theme.find('div', {'class': "vacancy-card__salary"}).text.strip()

    # Скилы
    skills = theme.find('div', {'class': "vacancy-card__skills"}).text.split(' • ')

    # Ссылка
    link = "https://career.habr.com/" + title.get('href')

    if 'удаленно' not in title:
        if 'Python' in skills and any([item for item in info if item in terms_info]):
            info = ' '.join(info)
            skills = ' '.join(skills)
            print('==< ~ >==')  # Разделитель
            print(company, title.text, info, skills, link, sep='\n')
