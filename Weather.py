import requests
from bs4 import BeautifulSoup

#LINEに通知を送る関数
def LineNotify(date):
    #==================================================================================
    #LINEのトークン
    TOKEN= "haEUzrkL7frUJLadWeF1HCUvL3C132I9m58jNWXWmLY"
    #==================================================================================

    #LineAPIのURL
    api_url = "https://notify-api.line.me/api/notify"

    #==================================================================================
    #送りたい文字列
    send_contents = date + "が雨の予報です"
    #==================================================================================

    #情報を辞書型にする
    TOKEN_dic = {"Authorization": "Bearer" + " " + TOKEN}
    send_dic = {"message": send_contents}
    
    #LINE通知を送る（200: 成功時、400: リクエストが不正、401: アクセストークンが無効：公式より）
    requests.post(api_url, headers=TOKEN_dic, data=send_dic)

#==================================================================================
#自分の地域のエリアコード(yahoo天気でURLを調べる)
AreaCode = 4410
#==================================================================================

#requestsを用いてHTMLを取得
url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(AreaCode) + ".html"
r = requests.get(url)
#BeautifulSoupを使用してhtml形式にパース
soup = BeautifulSoup(r.text, 'html.parser')

#データの抽出
rs = soup.find(class_='forecastCity')
#リストの加工
rs = [i.strip() for i in rs.text.splitlines()]
rs = [i for i in rs if i != ""]
#データの抽出
ts = soup.find(class_='yjw_main_md tracked_mods')
#リストの加工
ts = [i.strip() for i in ts.text.splitlines()]
ts = [i for i in ts if i != ""]

#デバッグ用プリント
"""
print(rs)
print(ts)
print(rs[0] + "の天気は" + rs[1] + "です。")
print(rs[18] + "の天気は" + rs[19] + "です。")
print(ts[3] + ts[4] + "の天気は" + ts[14]+ "です。")
print(ts[5] + ts[6] + "の天気は" + ts[15]+ "です。")
print(ts[7] + "の天気は" + ts[16]+ "です。")
"""

#取得した天気と文字列が合致したらLINE通知の関数呼び出し
weather = "雨"

if(weather in rs[1]):
    LineNotify(rs[0])
if(weather in rs[19]):
    LineNotify(rs[18])
if(weather in ts[14]):
    datefix = ts[3] + ts[4]
    LineNotify(datefix)
if(weather in ts[15]):
    datefix = ts[5] + ts[6]
    LineNotify(datefix)
if(weather in ts[16]):
    LineNotify(ts[7])