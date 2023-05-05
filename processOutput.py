# # Laptop Tổng hợp
# import json

# with open('outputFull.json', 'r', encoding = 'utf-8') as f:
#     data = json.load(f)

# new_data = []
# cnt = 0
# for item in data:
#     cnt += 1
#     new_item =  {
#                     'Type': item['Type'], 
#                     'Name': item['Name'] + ' - ' + item['Desc'][0]['CPU'] + ' | ' + item['Desc'][0]['RAM'] + ' | ' + item['Desc'][0]['OCung'] + ' | ' + item['Desc'][0]['KT&KL'],
#                     'Price': item['Price'],
#                     'Imgs': item['Imgs'],
#                     'ProductID': cnt,
#                     'Desc': item['Desc']
#                 }
#     new_data.append(new_item)

# with open('LaptopTongHop.json', 'w', encoding = 'utf-8') as f:
#     json.dump(new_data, f, indent = 4, ensure_ascii = False)

# Laptop Cụ thể

import json

with open('outputFull.json', 'r', encoding = 'utf-8') as f:
    data = json.load(f)

new_data = []
cnt = 0
for item in data:
    cnt += 1
    new_item =  {
                    'Url': item['Url'], 
                    'Name': item['Name'] + ' - ' + item['Desc'][0]['CPU'] + ' | ' + item['Desc'][0]['RAM'] + ' | ' + item['Desc'][0]['OCung'] + ' | ' + item['Desc'][0]['KT&KL'],
                    'Price': item['Price'],
                    'Original Price': item['Original_Price'], 
                    'WebsiteID': 1,
                }
    new_data.append(new_item)

with open('LaptopCuThe.json', 'w', encoding = 'utf-8') as f:
    json.dump(new_data, f, indent = 4, ensure_ascii = False)
