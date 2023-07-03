import json

with open('test.json','r+') as file:
    data = json.load(file)


for user in data['user_records']:
    if (user["email_sign"]=="sandesh@gmail.com"): 
        user["password"] = "sandesh@1234";         
with open('test.json', 'w') as file:
    json.dump(data, file, indent=4)
