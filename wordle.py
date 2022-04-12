import pandas as pd
import random
import math
import numpy as np

data = pd.read_csv('./wordle_data/allowed_words.txt', header = None)
data.columns = ['word']

def compare_word(w_target,w_guess):
    out = []
    for i in range(5):
        temp = 0
        if w_guess[i] in w_target:
            temp = 1
            if w_guess[i] == w_target[i]:
                temp = 2
        else:
            temp  = 0
        out.append(temp)
    return out

def choose_word(data_his, guess_his, df,method):
    if method == 0:
        gss = str(input('Guess b*tch: '))
        return gss
    if method == 0.5:
        all_word = find_all_word(data_his, guess_his, df)
        if len(data_his) > 0:
            if len(all_word) >= 5:
                print('Posible word: ' + ', '.join(all_word[:4]))
            else:
                print('Posible word: ' + ', '.join(all_word))
        gss = str(input('Guess b*tch: '))
        return gss
    if method == 1:
        if len(data_his) > 0:
            all_word = find_all_word(data_his, guess_his, df)
            if len(all_word) >= 5:
                print('Posible word: ' + ', '.join(all_word[:4]))
            else:
                print('Posible word: ' + ', '.join(all_word))
            max_en, en_score = calculate_totel_entropy(all_word, df)
            en_score = [str(np.round(x,3)) for x in en_score]
            win_able = len(data_his) + len(all_word)
            if win_able > 6:
                print('Best guess: ' + ', '.join(max_en))
                print('Score guess: ' + ', '.join(en_score))
        gss = str(input('Guess b*tch: '))
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
            temp = 3 * temp + out_compare[i]
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
    
st = int(input('start: '))
en = int(input('end: '))
list_out = []
name = 'wordle_' + str(st) + "_" + str(en) + '.npy'
for i in range(st,en,1):
    list_out.append(wordle_game_auto(data,i,2))
list_out = np.array(list_out)
np.save(name,list_out)