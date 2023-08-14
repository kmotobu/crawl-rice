import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://ineweb.narcc.affrc.go.jp/search/ine.cgi?action=hinsyu_table&getRow=100&suito=0&uruchi=0&chihou=ALL&chihouetc=SOR&hinmeikana=ON&rikuto=ON&mochi=ON&keitocode=ON&ikuseinen=ON&haifunen=ON&nourincode=ON&nourinnen=ON&meimeinen=ON&ikuseichi=ON&kouhai=ON&order1=0&order2=0&order3=0&rowid="


def main():
    total_num, df = get_table_info()
    record_num = 1
    while record_num <= total_num:
        df = get_table_row(df, record_num)
        record_num += 100
        # 愛知県警避け
        time.sleep(10)
    df.to_csv("data/raw_rice.csv", encoding='utf-8')

def get_table_row(df, record_num):
    response = requests.get(url+ str(record_num))
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table').find('table')
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            continue
        df.loc[record_num + i - 1] = [r.text for r in row.find_all('td')]
    return df

def get_table_info():
    # カラム取得と件数取得。
    # 呼び出し回数が冗長になる上にDirtyだが、theadが設定されていないので苦肉の策
    # 分類のIndexが呼び出し元でニコイチされているので分ける、コードが汚いのでサイト側の仕様が変わったら要修正
    response = requests.get(url+"1")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    total_num = int(soup.find_all("span", class_="s")[1].text.split(" ")[0])
    table = soup.find('table').find('table')
    row_name = table.find('tr')
    df = pd.DataFrame(columns=[i.text for i in row_name.find_all('th')])
    df = df.rename(columns={'分類': "分類:水陸"})
    df.insert(4, "分類:粳糯", 0)

    return total_num, df

main()