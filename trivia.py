import requests

url = "https://opentdb.com/api.php"
trivia = requests.get(url, params={
    'amount': 10,
    'category': 28,
    'difficulty': 'easy',
    'type': 'boolean'
}).json()
print(trivia)
# for x in trivia['results']:
#     print(x['question'])
#     print("Raspuns corect:", x['correct_answer'])