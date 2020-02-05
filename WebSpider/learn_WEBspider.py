from urllib import request

responce = request.urlopen("https://www.python.org")
print(responce.read().decode("utf-8"))
print(responce.getheaders())
print(responce.status)
