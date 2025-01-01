import requests
import csv

response = requests.get('https://randomuser.me/api/?results=2')
data = response.json()

#print(data)

def cat_age(age):
    if age<30:
        return 'G0'
    elif age>30 and age<50:
        return 'G1'
    else:
        return 'G2'

users = []

for user in data['results']:
    f_name = user['name']['first']
    l_name = user['name']['last']
    gender = user['gender']
    country = user['location']['country']
    email = user['email']
    dob = user['dob']['date']
    age = user['dob']['age']
    age_group = cat_age(age)

    users.append({'First name': f_name, 'Last Name': l_name,'Gender':gender,
                  'country':country,'email':email,'Date of Birth':dob,'Age':age,
                  'Age Group':age_group})

for  user in users:
    print(user)
    
output_file = 'user_data.csv'
header = ['First name','Last Name','Gender','country','email','Date of Birth','Age','Age Group']

with open(output_file,mode='w',newline='',encoding='utf-8') as file:
    writer= csv.DictWriter(file,fieldnames=header)
    writer.writerows(users)

print(output_file)
