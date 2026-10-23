import html
import os
import random
import requests

# Open Trivia Database — API gratuit, nu necesita cheie
URL = "https://opentdb.com/api.php"


def curata_ecranul():
    os.system('cls' if os.name == 'nt' else 'clear')


def citeste_numar(mesaj, minim, maxim):
    """Cere un numar de la utilizator pana cand e valid."""
    while True:
        valoare = input(mesaj).strip()
        if valoare.isdigit() and minim <= int(valoare) <= maxim:
            return int(valoare)
        print(f"Introduceti un numar intre {minim} si {maxim}.")


def ia_intrebari(numar, dificultate):
    params = {'amount': numar}
    if dificultate:
        params['difficulty'] = dificultate

    raspuns = requests.get(URL, params=params, timeout=10).json()

    if raspuns.get('response_code') != 0:
        print("Eroare la API, cod:", raspuns.get('response_code'))
        return []
    return raspuns['results']


def main():
    curata_ecranul()
    print("=== QUIZ ===\n")

    numar = citeste_numar("Cate intrebari vrei (1-20)? ", 1, 20)

    print("\nDificultate: 1 - usor, 2 - mediu, 3 - greu, 4 - oricare")
    alegere = citeste_numar("Alege: ", 1, 4)
    dificultate = {1: 'easy', 2: 'medium', 3: 'hard', 4: None}[alegere]

    intrebari = ia_intrebari(numar, dificultate)
    if not intrebari:
        return

    puncte = 0

    for i, q in enumerate(intrebari, start=1):
        # textele vin cu caractere HTML (&quot; &#039; etc.) — le decodam
        intrebare = html.unescape(q['question'])
        corect = html.unescape(q['correct_answer']).strip()
        variante = [html.unescape(v).strip() for v in q['incorrect_answers']] + [corect]

        if q['type'] == 'boolean':
            variante = ['True', 'False']
        else:
            random.shuffle(variante)

        print(f"\nIntrebarea {i}/{len(intrebari)}  [{html.unescape(q['category'])}]")
        print(intrebare)
        for nr, varianta in enumerate(variante, start=1):
            print(f"  {nr}. {varianta}")

        ales = citeste_numar("Raspunsul tau: ", 1, len(variante))

        if variante[ales - 1] == corect:
            puncte += 1
            print("Corect! +1 punct")
        else:
            print(f"Gresit. Raspunsul corect: {corect}")

    print(f"\n=== Scor final: {puncte}/{len(intrebari)} ===")


if __name__ == "__main__":
    main()