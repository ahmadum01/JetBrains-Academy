import sys
import os
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore

args = sys.argv
directory_name = args[1]
if not os.access(directory_name, os.F_OK):  # If directory not exist
    os.mkdir(directory_name)
os.chdir(directory_name)


def save_to_file(name, content):
    """Save page to cash"""
    with open(name, 'w', encoding='utf-8') as file:
        file.write(content)


def open_page(name):
    if name in os.listdir():
        with open(name, 'r') as file:  # Reading page from cash
            print(file.read())
        stack.append(name)
    else:
        url = name if name.startswith('https://') else 'https://' + command
        r = requests.get(url)
        save_to_file(url[8:url.find('.')], to_text(r.content))
        print(to_text(r.content))


def back():
    """Return to previous page"""
    if len(stack) > 1:
        stack.pop()
        with open(stack[-1], 'r') as file:
            print(file.read())


def to_text(content):
    """Parse html to clean text"""
    soup = BeautifulSoup(content, 'html.parser')
    # pick up tags with text
    lines = soup.find_all(['a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])
    result = ''
    for line in lines:
        if line.name == 'a':
            result += Fore.BLUE + line.text + '\n'  # painting link to blue color
        else:
            result += line.text + '\n'
    return result


stack = []
while True:
    command = input()
    if re.match('.+[.].+', command):  # Check for valid url
        open_page(command)
    elif command == 'back':
        back()
    elif command == 'exit':
        break
    else:
        print('Incorrect URL')
