import json

with open('property_list_london.json', 'r', encoding='utf8') as file:
    data = json.load(file)

data = data.get('data').get('body').get('searchResults').get('results')

for hotel in data:
    print(f'{hotel["id"]}', end=' ===> ')
    print(hotel['landmarks'][0]['distance'], end=' ')
    print('цена:', hotel['ratePlan']['price']['exactCurrent'])
