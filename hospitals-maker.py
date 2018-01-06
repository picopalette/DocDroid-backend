import requests
import json

with open('out.json') as file:
  data = json.load(file)
  names = data[0]
  addresses = data[1]
  locations = data[3]
  for index, (name, address, location) in enumerate(zip(names, addresses, locations)):
    post_data = dict()
    post_data['name'] = name
    post_data['address'] = address
    post_data['lat'] = str(location['lat'])
    post_data['log'] = str(location['lng'])
    post_data['email'] = str(index) + '@gmail.com'
    post_data['password'] = str(index)
    post_json = json.dumps(post_data)
    result = requests.post('http://172.16.8.43:8000/signUpHospital', data=post_json)
    print(post_json)