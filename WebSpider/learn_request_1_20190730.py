import socket
from urllib import request, error, parse
data = bytes(parse.urlencode({"word":"hello"}), encoding="utf-8")
try:
    response = request.urlopen("https://www.baidu.com", data=data, timeout=3)
    print(response.read().decode("utf-8"))
except error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print("Time OUt")
