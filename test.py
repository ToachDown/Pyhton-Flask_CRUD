import requests

BASE = "http://localhost:5000/"

data = [
    {"likes": 101, "name": "Saloed 3000", "views": 111},
    {"likes": 1034, "name": "zalo bomza", "views": 222},
    {"likes": 560, "name": "black pussy", "views": 333},
    {"likes": 11140, "name": "green gun", "views": 4444}
]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()
# response = requests.delete(BASE + "video/1")
# print(response)
# response = requests.get(BASE + "video/2")
# print(response.json())
resource = requests.get(BASE + "video")
print(resource.json())
