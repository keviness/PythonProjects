#learn_web_spider_requests1_20190804
import requests
data = {"name":"germy", "age":22}
response = requests.post("http://httpbin.org/post", data=data)
print(type(response.text), response.text)
print(type(response.headers), response.headers)
print(type(response.status_code), response.status_code)
print(response.cookies)
print(response.history)
