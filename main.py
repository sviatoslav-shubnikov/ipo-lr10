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

def html(file="data.json", template_file="template.html", output_file="index.html"):
    with open(file, "r", encoding="utf-8") as f:
        datas = json.load(f)

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    soup = bs(template, "html.parser")
    container = soup.find("div", class_="place-here")
    
    if not container:
        raise ValueError("Template is missing a 'place-here' element for the table.")

    table = Tag(name="table", attrs={"class": "quotes-table"})
    
    # Create table headers
    thead = Tag(name="thead")
    tr_head = Tag(name="tr")
    headers = ["№", "Repository", "Stars"]
    
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    
    thead.append(tr_head)
    table.append(thead)

    # Create table body
    tbody = Tag(name="tbody")
    
    for idx, data in enumerate(datas, start=1):
        tr = Tag(name="tr")

        td_num = Tag(name="td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_repo = Tag(name="td")
        td_repo.string = data["Repository"]
        tr.append(td_repo)

        td_stars = Tag(name="td")
        td_stars.string = data["Stars"]
        tr.append(td_stars)

        tbody.append(tr)
    
    table.append(tbody)
    
    # Insert the table into the template
    container.append(table)

    # Save the modified HTML to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

html()