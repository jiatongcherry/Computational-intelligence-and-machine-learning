import requests
import sqlite3
from bs4 import BeautifulSoup

url = "https://www.forbeschina.com/lists/1828"

response = requests.get(url, verify=False)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')


table = soup.find('table', {'id': 'data-view'})

rows = table.find_all('tr')[1:]


conn = sqlite3.connect('wealth_rankings.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS wealth_rankings (
    rank INTEGER PRIMARY KEY,
    name_en TEXT,
    name_cn TEXT,
    wealth REAL,
    source TEXT,
    country TEXT
)
''')


for row in rows:
    cols = row.find_all('td')
    if len(cols) == 6:
        rank = int(cols[0].text.strip())
        name_en = cols[1].text.strip()
        name_cn = cols[2].text.strip()
        wealth = float(cols[3].text.strip().replace(',', ''))
        source = cols[4].text.strip()
        country = cols[5].text.strip()


        cursor.execute('''
        INSERT OR REPLACE INTO wealth_rankings (rank, name_en, name_cn, wealth, source, country)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (rank, name_en, name_cn, wealth, source, country))

conn.commit()
conn.close()

print("数据已经保存到数据库中！")
