import requests
r = requests.get("https://megasportsworld.com/")
url = "https://megasportsworld.com/"

response = requests.post(url)
print(response.elapsed.total_seconds())
#print(r.headers)