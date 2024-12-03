import requests
import json
from bs4 import BeautifulSoup as bs
datas = []
url = "https://github.com/trending"

response = requests.get(url)
soup = bs(response.text, "html.parser")
for data in soup.find_all('article', class_="Box-row"):
    
    repo = data.find('a', class_='Link').get_text()
    
    stars = data.find('a', class_='Link Link--muted d-inline-block mr-3').get_text()
    datas.append({'repos': repo, "stars": stars})

    print(f"repo: {repo}, stars: {stars}")

    