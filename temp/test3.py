import json

with open('rome.json', 'r', encoding='utf8') as file:
    data = json.load(file)

data = data.get('data').get('body').get('searchResults').get('results')

for hotel in data:
    print('расстояние от цента', hotel['landmarks'][0]['distance'], end=' ')
    print('цена за сутки:', hotel['ratePlan']['price']['exactCurrent'])
