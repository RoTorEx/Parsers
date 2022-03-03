from bs4 import BeautifulSoup
import requests


url = "https://news.ycombinator.com/newest"

request = requests.get(url)

soup = BeautifulSoup(request.text, "html.parser")

print(soup)
