import requests
import json
from bs4 import BeautifulSoup as bs
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
    
    
    soup = bs("<html></html>", "html.parser")
    
    head = soup.new_tag("head")
    soup.html.append(head)
    
    title = soup.new_tag("title")
    title.string = "Список репозиториев"
    head.append(title)

    style = soup.new_tag("style")
    style.string = """
        body {
            color: #333;
            background-color: #f4f4f4;
        }
        table {
            background: #ffffff;
        }
        th, td {
            padding: 15px;
            border: 1px solid #ccc;
            text-align: center;
        }
        th {
            background-color: #e0e0e0;
            color: #000;
        }
        h1 {
            text-align: left;
            margin-bottom: 20px;
        }
        p {
            text-align: left;
            margin-top: 20px;
        }
        a {
            color: #00ff62;
            text-decoration: underline;
        }
    """
    head.append(style)

    body = soup.new_tag("body")
    soup.html.append(body)
    
    header = soup.new_tag("h1")
    header.string = "Коллекция репозиториев"
    body.append(header)

    table = soup.new_tag("table")
    body.append(table)

    thead = soup.new_tag("tr")
    headers = ["№", "Repository", "Stars"]
    for h in headers:
        th = soup.new_tag("th")
        th.string = h
        thead.append(th)
    table.append(thead)


    for id, data in enumerate(datas, 1):
        tr = soup.new_tag("tr")
    
        td_num = soup.new_tag("td")
        td_num.string = str(id)
        tr.append(td_num)
        
        td_repo = soup.new_tag("td")
        td_repo.string = data["Repository"]
        tr.append(td_repo)
        
        td_stars = soup.new_tag("td")
        td_stars.string = data["Stars"]
        tr.append(td_stars)
        
        table.append(tr)
    
    
    source_link = soup.new_tag("p")
    a_tag = soup.new_tag("a", href="https://github.com/trending")
    a_tag.string = "Источник: Repositories in Trend (GitHUB)"
    source_link.append(a_tag)
    body.append(source_link)

   
    with open(file_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

html()