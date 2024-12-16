import requests
import json
from bs4 import BeautifulSoup as bs
from bs4 import Tag

datas = []
url = "https://github.com/trending"

response = requests.get(url)
soup = bs(response.text, "html.parser")
count = 1

for data in soup.find_all('article', class_="Box-row"):
    
    repo = data.find('a', class_='Link').get_text().strip().replace(' ', '').splitlines()
    
    stars = data.find('a', class_='Link Link--muted d-inline-block mr-3').get_text().strip().replace(' ', '')
    repos = repo[0]+repo[2]
    datas.append({'Repository': repos, "Stars": stars})

    print(f"{count}. Repository: {repos}; Stars: {stars};")

    count+=1

def save_to_json(datas, file="data.json"):
    with open(file,"w",encoding="utf-8")as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)

save_to_json(datas)

def html(file="data.json", file_html="index.html"):
    with open(file, "r", encoding="utf-8") as f:
        datas = json.load(f)
    
    with open(file_html, "r", encoding="utf-8") as f:
        soup = bs(f, "html.parser")
    
    table = soup.find("table", class_="table")
    if not table:
        print(f"Ошибка: Таблица с классом 'table' не найдена в шаблоне.")
        return

    # Добавление строк данных в таблицу
    for id, data in enumerate(datas, 1):
        tr = Tag(name="tr")
        
        td_num = Tag(name="td")
        td_num.string = str(id)
        tr.append(td_num)
        
        td_repo = Tag(name="td")
        td_repo.string = data["Repository"]
        tr.append(td_repo)
        
        td_stars = Tag(name="td")
        td_stars.string = data["Stars"]
        tr.append(td_stars)
        
        table.append(tr)

    # Сохранение изменений в тот же HTML-файл
    with open(file_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

html()