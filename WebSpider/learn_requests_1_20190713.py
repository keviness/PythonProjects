import requests
url = "http://www.moe.gov.cn/jyb_xxgk/"
html = requests.get(url).text.splitlines()
for i in range(0, 15):
    print(html[i])