import requests

requisition_quantity = 0
response = []

while requisition_quantity < 10:
  requisition_quantity += 1
  response.append(requests.get('https://jsonplaceholder.typicode.com/posts'))

print(response)