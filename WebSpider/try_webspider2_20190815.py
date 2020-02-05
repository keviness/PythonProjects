import requests
import re
def get_one_page(url):
    try:
        headers = {
            "User-Agent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325 .162 Safari / 537.36 "
        } 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return(response.text)
        else:
            return None
    except RequestException as e:
        print(e)

def parse_one_page(html):
    res = '<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?>(.*?)</a>'
    pattern = re.compile(res, re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield{
            "index":item[0],
            "title":item[1]
        }

html = get_one_page("http://maoyan.com/board/4")
s = parse_one_page(html)
for i in s:
    print(i)

