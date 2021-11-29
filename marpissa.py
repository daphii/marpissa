import requests
import time
import os

from bs4 import BeautifulSoup

# classes
class Target:

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.filename = 'stash/' + clean_name(name) + '.txt'
    
    def __repr__(self):
        return 'Name: {} \nURL: {}\n'.format(self.name, self.url)

    def get(self):

        with open(self.filename, 'w') as output:

            print('> Searching for: {}...'.format(self.name))
            
            page = requests.get(self.url)
            print('> Data collected!')

            plaintext = str(page.content)
            print('> Converted to text!')

            if captcha(plaintext):
                print('> WARNING: Likely blocked by captcha!')
            
            cleantext = plaintext.split('\\n')
            print('> Fixing line breaks!')
            
            for line in cleantext:
                output.write(line + '\n')
            print('> File written to {}\n'.format(self.filename))

   
# text outputs
lucas = '''
       ,;,;,,;,;,
      (.)__''__(.)
    >x< / ,\/, \\ >x<
    >xx<\__/\__/>xx<
     ^>xx< ^^ >xx<^
       ^>xx<>xx<^
         ^^  ^^
'''

# lambdas
now = lambda i: time.localtime()[i]
clear = lambda: os.system('cls')

# functions
def greet():

    if now(3) < 12:
        x = 'morning'

    if now(3) >= 12 and now(3) < 17:
        x = 'afternoon'

    if now(3) >= 17:
        x = 'evening'

    greeting = '> Good {} mum <3 \n> New goodies await us!\n'.format(x)

    print(lucas)
    print(greeting)

target_dict = {}
def read_targets():

    with open('ingest/ingest.txt') as targets:

        lines = targets.readlines()
        names = [line[1:-1] for line in lines if line[0] == '>']
        urls = [line[1:-1] for line in lines if line[0] == '=']

        target_data_dict = {}
        for i in range(len(names)):
            target_data_dict[names[i]] = urls[i]
        
        for target in target_data_dict:
            name = target
            url = target_data_dict[target]
            target_dict[target] = Target(name, url)

        return target_dict

def check_targets():

    print('> Here is my to-do list! \n')

    targets = read_targets()

    for target in targets:
        print(targets[target])

def confirm():
    idx = 1

    for target in target_dict.values():
        print('> Target {}'.format(idx))
        print(target.name)
        print(target.url)
        print('> Will be output as: ' + target.filename + '\n')
        idx += 1

def clean_name(string):
    clean = ''
    for x in string:
        if x == ' ':
            clean += '_'
        else:
            clean += x

    return clean.lower()

def captcha(x):
    if 'captcha' in x or 'recaptcha' in x:
        return True


# running

play = True
menu_code = 1

while play:

    while menu_code == 1:
        user = ''
        clear()
        greet()
        check_targets()
        user = input('> Does this look right? y/n - ')

        if user == 'y':
            menu_code = 2

        if user == 'n':
            clear()
            greet()
            print('> Lets fix that\n')
            os.system('start ingest/ingest.txt')
            user = input('> I opened the ingest file for you. \n> Ready to try again? ready/cancel - ')

        if user == 'cancel':
            print("\n> I'll be here when you are ready!")
            menu_code = 0
            play = False

        if user == 'ready':
            target_dict = {}
            continue

    while menu_code == 2:
        user = ''

        clear()
        print(lucas)
        confirm()
        user = input('>  I am all ready to go now, may I? y/n - ')

        if user == 'y':
            menu_code = 3

        if user == 'n':
            menu_code = 1

    while menu_code == 3:
        user = ''
        clear()
        print(lucas)
        print('Here we go!\n')
        for target in target_dict.values():
            target.get()
            time.sleep(1)
        print('> All done! :D\n')
        menu_code = 4

    while menu_code == 4:
        user = input('Can I show you what I found? y/n - ')

        if user == 'y':
            for target in target_dict.values():
                os.system('start ' + target.filename)
            print('> See you next time!')
            menu_code = 0
            play = False

        if user == 'n':
            print('> See you next time!')
            menu_code = 0
            play = False


        
