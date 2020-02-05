import requests
from bs4 import BeautifulSoup
import json

def get_one_page(url):
    headers = {
        "User-Agent":"Mozilla/5.0(Macintosh;Inter Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
    }
    result = requests.get(url, headers=headers)
    if result.status_code == 200: 
        return result.text
    else:
        return None
def parse_one_page(html):
    soup = BeautifulSoup(html, "lxml")
    for ul in soup.find_all(attrs={"class":"book-info"}):
        yield{
            "bookname":ul.a.string,
            "author":ul.div.string
        }

def write_to_file(content):
    with open("豆瓣图书.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False)+"\n")
    f.close()
def main():
    url = "https://book.douban.com/"
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
if __name__ == "__main__":
    main()
