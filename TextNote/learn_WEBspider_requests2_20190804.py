#learn_WEBspider_requests_2_20190804
import requests
r = requests.get("http://github.com/favicon.ico")
with open("github_picture.ico", "wb") as f:
    f.write(r.content)
f.close()
