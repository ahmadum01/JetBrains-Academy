import requests
import argparse
from bs4 import BeautifulSoup


def translate(lang_from, lang_to, word):
    """Take info from site ReversoContext"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://context.reverso.net/translation/{lang_from}-{lang_to}/{word}'
    try:
        page = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        return 'exception'
    status_code = 0
    while status_code != '200':
        status_code = str(page)[11:-2]
        if status_code == '404':
            return '404'
    return page


def parse(page):
    if page == 'exception':  # Check for internet connection
        print('Something wrong with your internet connection')
        return None
    if page == '404':  # if page not found
        print(f'Sorry, unable to find {args.word}')
        return None

    soup = BeautifulSoup(page.content, 'html.parser')
    lines = soup.find_all(['div', 'a'], 'dict')  # find 'div' and 'a' elements from css class 'dict'
    translates = [i.text.strip() for i in lines]

    if not translates:  # Check for empty translates list
        print(f'Sorry, unable to find {args.word}')
        return None

    lines = soup.find_all('div', ['src', 'trg'])  # find 'div' elements from css classes 'src' and 'trg'
    examples = [i.text.strip() for i in lines]
    examples = list(filter(None, examples))  # delete empty strings
    return translates, examples


def translate_all(lang_from, word):
    """For translate word in all languages from 'languages' list"""
    for lang in languages:
        if lang_from != lang:
            parsed_result = parse(translate(lang_from, lang, word))
            if not parsed_result:
                return None
            print_result(*parsed_result, lang, word)


def print_result(translates, examples, lang_to, word):
    with open(word + '.txt', 'a', encoding="utf-8") as file:
        print(f'\n{lang_to} Translations:', file=file)  # write in file
        print(f'\n{lang_to} Translations:')  # print in console
        for i in range(len(translates) if len(translates) <= 5 else 5):
            print(translates[i], file=file)
            print(translates[i])

        print(f'\n{lang_to} Examples:', file=file)
        print(f'\n{lang_to} Examples:')
        for i in range(len(examples) if len(examples) // 2 <= 5 else 10):
            if i % 2 == 1:
                print(examples[i], end='\n\n', file=file)
                print(examples[i], end='\n\n')
            else:
                print(examples[i], file=file)
                print(examples[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('lang_from')
    parser.add_argument('lang_to')
    parser.add_argument('word')
    args = parser.parse_args()
    languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
                 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']

    if args.lang_to not in languages and args.lang_to != 'all':
        print(f'Sorry, the program doesn\'t support {args.lang_to}')
    else:
        if args.lang_to == 'all':
            translate_all(args.lang_from, args.word)
        else:
            result = translate(args.lang_from, args.lang_to, args.word)
            parsed_result_ = parse(result)
            if parsed_result_:
                print_result(*parsed_result_, args.lang_to, args.word)
