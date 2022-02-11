import streamlit as st
from english_words import english_words_set as eng
import numpy as np

###############
# FIXME
#answer = 'HOUSE'
answer = None
SEED=0
###############
np.random.seed(SEED)

# english dictionary book
eng5 = [e.upper() for e in eng if len(e) == 5]
eng5.append('EARLY')

if answer == None:
    answer = np.random.choice(eng5, 1)[0]

# color map
GREEN = 'rgb(91,194,54)'
GREY = 'rgb(200,200,200)'

def font(s, color='black', size=30, back=False):
    if back:
        if color == GREY:
            ret = f'<span style="font-family:Courier; color:black; background-color:{color}; font-size: {size}px;">{s}</span>'
        else:
            ret = f'<span style="font-family:Courier; color:white; background-color:{color}; font-size: {size}px;">{s}</span>'
    else:
        ret = f'<span style="font-family:Courier; color:{color}; font-size: {size}px;">{s}</span>'
    return ret

def list_replace(ls, old, new):
    for i, l in enumerate(ls):
        if l == old:
            ls[i] = new
    return ls

def check_word(inp, tgt, candidates):
    # input:
    #  inp: a word to be matched
    #  tgt: an answer word
    #  candidates: alphabet candidates
    # output:
    #  colored word
    #  number of matched
    #  modified candidates
    colored_inp = ''
    cnt = 0
    for i, w in enumerate(inp):
        if w == tgt[i]:
            colored_inp += font(w, GREEN, back=True)
            candidates = list_replace(candidates, font(w, GREY, size=25, back=True), font(w, GREEN, size=25, back=True))
            candidates = list_replace(candidates, font(w, 'orange', size=25, back=True), font(w, GREEN, size=25, back=True))
            cnt +=1
        elif w in tgt:
            colored_inp += font(w, 'orange', back=True)
            candidates = list_replace(candidates, font(w, GREY, size=25, back=True), font(w, 'orange', size=25, back=True))
        else:
            colored_inp += font(w, back=True)
            candidates = list_replace(candidates, font(w, GREY, size=25, back=True), font(w, 'black', size=25, back=True))
    return colored_inp, cnt, candidates


st.title('CUSTOM WORDLE')

candidates = [font(a, GREY, size=25, back=True) for a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

#status_str = font('Status: ')
status_msg = st.empty()
candidate_msg = st.empty()

for i in range(6):
    cnt = 0
    status_str = 'Status(TRIAL: {}/6): '.format(i+1)

    text_input_container = st.empty()
    candidate_str = \
        font('Candidate letters: <br>', size=25) + \
        ''.join(candidates[0:13] + ['<br>'] + candidates[13:]) # for mobile
    candidate_msg.markdown(candidate_str, unsafe_allow_html=True)

    while True:
        inp = text_input_container.text_input(label='type 5-length word ', key=i, max_chars=5)
        inp = inp.upper()
        if inp == '':
            status_msg.success(status_str + '')
        elif not len(inp) == 5:
            status_msg.warning(status_str + 'input should be 5-length word')
        elif not inp in eng5:
            status_msg.warning(status_str + 'input is not in a dictionary')
        else:
            text_input_container.empty()
            colored_inp, cnt, candidates = check_word(inp, answer, candidates)
            text_input_container.markdown('<__'+colored_inp+'__>', unsafe_allow_html=True)
            break
    if cnt == 5:
        status_msg.success(status_str + 'Success')
        st.balloons()
        break

if cnt != 5:
    status_msg.warning('Fail: {} was an answer'.format(answer))

# TODO
# check multiple hit alphabet
