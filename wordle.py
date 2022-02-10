from termcolor import colored
from PyDictionary import PyDictionary
import os, sys


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def check_word(dictionary, word):
    blockPrint()
    ret = dictionary.meaning(word)
    enablePrint()
    return type(ret) == dict()

def list_replace(ls, old, new):
    for i, l in enumerate(ls):
        if l == old:
            ls[i] = new
    return ls

print(colored('custom', 'red'), colored('wordle', 'green'))

dictionary = PyDictionary()

answer = 'house'

candidates = [a for a in 'abcdefghijklmnopqrstuvwxyz']

print('## type a 5-length word')
for i in range(5):
    cnt = 0
    flg = True
    while flg:
        inp = input('##: ')
        if len(inp) != 5:
            print('input should be a 5-length word')
        elif check_word(dictionary, inp):
            print('input is not a word')
        else:
            flg = False

    colored_inp = []
    for ii, w in enumerate(inp):
        if w == answer[ii]:
            colored_inp.append(colored(w, 'green'))
            candidates = list_replace(candidates, w, colored(w, 'green'))
            candidates = list_replace(candidates, colored(w, 'yellow'), colored(w, 'green'))
            cnt += 1
        elif w in answer:
            colored_inp.append(colored(w, 'yellow'))
            candidates = list_replace(candidates, w, colored(w, 'yellow'))
        else:
            colored_inp.append(colored(w, 'white'))
            candidates = list_replace(candidates, w, colored(w, 'grey'))

    print(f'## {i + 1}th trial: ', *colored_inp )
    if cnt == 5:
        print('!!FASCINATING!!')
        break
    print(f'## candidates :', *candidates)

# todo
# streamlit
