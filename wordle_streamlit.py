import pandas as pd
import random
import math
import numpy as np
import streamlit as st

data = pd.read_csv('./wordle_data/allowed_words.txt', header = None)
data.columns = ['word']

def compare_word(w_target,w_guess):
    out = ""
    try:
        for i in range(5):
            temp = 0
            if w_guess[i] in w_target:
                temp = 1
                if w_guess[i] == w_target[i]:
                    temp = 2
            else:
                temp  = 0
            out = out + str(temp)
    except:
        return "-1"
    return out

def choose_word(data_his, guess_his, df,method,w):
    if method == 0:
        gss = w[len(data_his) - 1]
        return gss
    if method == 0.5:
        all_word = find_all_word(data_his, guess_his, df)
        if len(data_his) > 0:
            if len(all_word) >= 5:
                st.write('Posible word: ' + ', '.join(all_word[:4]))
            else:
                st.write('Posible word: ' + ', '.join(all_word))
        gss = w[len(data_his) - 1]
        return gss
    if method == 1:
        if len(data_his) > 0:
            all_word = find_all_word(data_his, guess_his, df)
            if len(all_word) >= 5:
                st.write('Posible word: ' + ', '.join(all_word[:4]))
            else:
                st.write('Posible word: ' + ', '.join(all_word))
            max_en, en_score = calculate_totel_entropy(all_word, df)
            en_score = [str(np.round(x,3)) for x in en_score]
            win_able = len(data_his) + len(all_word)
            if win_able > 6:
                st.write('Best guess: ' + ', '.join(max_en))
                st.write('Score guess: ' + ', '.join(en_score))
        gss = w[len(data_his) - 1]
        return gss
    if method == 2:
        if len(data_his) > 0:
            all_word = find_all_word(data_his, guess_his, df)
            win_able = len(data_his) + len(all_word)
            if win_able > 6:
                max_en, en_score = calculate_totel_entropy_auto(all_word, df)
                return max_en
            else:
                return all_word[0]
        else:
            return 'crane'
        
def find_all_word(data_his, guess_his,df):
    lsts  = list(df.word)
    out = []
    for lst in lsts:
        if check_meet_his(lst,data_his, guess_his):
            out.append(lst)
    return out
        
def check_meet_his(guess, data_his, guess_his):
    for i in range(len(guess_his)):
        temp = compare_word(guess, guess_his[i])
        tempp = data_his[i]
        for j in range(5):
            if temp[j] != tempp[j]:
                return False
    return True


def calculate_entropy(guess, all_pool):
    lst_score = []
    for w in all_pool:
        out_compare = compare_word(w, guess)
        temp = 0
        for i in range(5):
            temp = 3 * temp + int(out_compare[i])
        lst_score.append(temp)
    set_score = set(lst_score)
    fre = {x:lst_score.count(x) for x in set_score}
    temp = 0
    for js in set_score:
        temp = temp + math.log2(len(all_pool)/fre[js])*fre[js]/len(all_pool)
    return temp

def calculate_totel_entropy(all_pool, df):
    list1 = list(df.word)
    list2 = []
    for il in list1:
        score = calculate_entropy(il, all_pool)
        list2.append(score)
    list2, list1 = zip(*sorted(zip(list2, list1), reverse = True))
    return list1[:10], list2[:10]

def calculate_totel_entropy_auto(all_pool, df):
    list1 = list(df.word)
    list2 = []
    for il in list1:
        score = calculate_entropy(il, all_pool)
        list2.append(score)
    idx = list2.index(max(list2))
    return list1[idx], list2[idx]

def wordle_game_auto(df,idd,method):
    print(idd)
    target = list(df.word)[idd]
    state = 0
    temp_sum = 0
    data_his = []
    guess_his = []
#    print('=======')
    while (state <6) and (temp_sum<10):
        guess = choose_word(data_his, guess_his,df,method)
        guess_his.append(guess)
        out_compare = compare_word(target, guess)
        data_his.append(out_compare)
#        print(', '.join(guess))
#        print(', '.join([str(x) for x in out_compare]))
#            print([char for char in guess])
#            print([str(x) for x in out_compare])
        state = state + 1
        temp_sum = sum(out_compare)
    if temp_sum == 10:
        return 1, len(guess_his)
    else:
        return 0, 7
    
def wordle_game_streamlit(df,idd,w,method):
    target = list(df.word)[idd]
    state = 0
    temp_sum = 0
    data_his = []
    guess_his = []
    out_compare = []
    print('=======')
    for i in range(len(w)):
        st.write(w[i])
        st.write(len(w[i]))
        if len(w[i])>0:
            guess = choose_word(data_his, guess_his,df,method,w)
            guess_his.append(guess)
            out_compare = compare_word(target, guess)
            data_his.append(out_compare)
            st.write(', '.join(guess))
            st.write(', '.join([str(x) for x in out_compare]))
        else:
            guess = ''
            out_compare = []
            st.write(', '.join(guess))
            st.write(', '.join([str(x) for x in out_compare]))
        st.write("")
        temp_sum = sum(out_compare)
    if temp_sum == 10:
        st.write('WIN')
    else:
        st.write('LOSE HIU HIU')
    return None

method_lst = ['normal', 'suggestions', 'information entropy']
st.write("""
# WORDLE GAME
""")
st.sidebar.header('User Input Values')
method_en = st.sidebar.selectbox('Select method',method_lst, 0)
idd = st.slider('Select random id', 0, 12971, step = 1)
w1 = st.sidebar.text_input('Guess word 1',max_chars = 5, key = 1)
w2 = st.sidebar.text_input('Guess word 2',max_chars = 5, key = 2)
w3 = st.sidebar.text_input('Guess word 3',max_chars = 5, key = 3)
w4 = st.sidebar.text_input('Guess word 4',max_chars = 5, key = 4)
w5 = st.sidebar.text_input('Guess word 5',max_chars = 5, key = 5)
w6 = st.sidebar.text_input('Guess word 6',max_chars = 5, key = 6)
w = [w1,w2,w3,w4,w5,w6]
if method_en == 'normal':
    method = 0
if method_en == 'suggestions':
    method = 0.5
if method_en == 'information entropy':
    method = 1
target = list(data.word)[idd]
d = {
    'word_guess' : w
}
df = pd.DataFrame(d)
df['score'] = df['word_guess'].apply(lambda x: compare_word(target, x))
st.dataframe(df)

temp_sum = max([int(x) for x in df.score])
if temp_sum == 22222:
    st.write('WIN')
else:
    st.write('NOT WIN YET, HIU HIU')
st.write()
if method >= 0.5:
    st.write('Posiible Words')
    n = len(df[df['score']!= '-1'])
    guess_his = list(df.word_guess)[:n]
    data_his = list(df.score)[:n]
    all_pool = find_all_word(data_his, guess_his,data)
    n_max = min(len(all_pool),5)
    d_pool = {}
    for i in range(n_max):
        name_col = "word_" +str(i+1)
        d_pool[name_col] = [all_pool[i]]
    df_pool = pd.DataFrame(d_pool)
    st.dataframe(df_pool)
    
if method >= 1:
    st.write('Maximize Entropy')
    if n >= 1:
        l1, l2 = calculate_totel_entropy(all_pool, data)
        n_max = min(len(l1),5)
        d_en = {}
        for i in range(n_max):
            name_col = "word_" +str(i+1)
            d_en[name_col] = [l1[i], str(round(l2[i],2))]
        df_en = pd.DataFrame(d_en)
        st.dataframe(df_en)
