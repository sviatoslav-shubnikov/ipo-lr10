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
    with open(file,"r",encoding="utf-8")as f:
        datas=json.load(f)
    
    html_cont='''
<html>
    <head>
        <title>Список репозиториев</title>
        <style>
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
        </style>
    </head>
    <body>
        <div>
            <h1>Коллекция репозиториев</h1>
            <table>
                <tr>
                    <th>№</th>
                    <th>Repository</th>
                    <th>Stars</th>
                </tr>
    '''

    
    for id, data in enumerate(datas, 1):
        html_cont += f'''
        <tr>
            <td><h3>{id}</h3></td>
            <td><h3>{data["Repository"]}</h3></td>
            <td><h3>{data["Stars"]}<h3></td>
        </tr>
        '''

    
    html_cont += '''
            </table>
            <p>
                <h2><a href="https://github.com/trending">Источник: Repositories in Trend (GitHUB)</a></h2>
            </p>
        </div>
    </body>
</html>
    '''

    
    with open(file_html, "w", encoding="utf-8") as f:
        f.write(html_cont)


html()