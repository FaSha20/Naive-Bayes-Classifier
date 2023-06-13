import statistics
import numpy as np
import math


def calc_post_prob(words, category):
    mult = 1
    for word in words:
        if word in words_dict_train[category]:
            mult *= words_dict_train[category][word]/words_count[category]
        elif word not in stop_words:
            mult = 0

    mult *= class_count[category]/class_count['sum']
    return mult

def calc_probs(max_probs, best_cats, probs):
    nomm = 0
    for i in range(len(test['description'])):
        words = test_tokenized_desc[i] + test_tokenized_title[i]
        for category in words_dict_train:
            mult = calc_post_prob(words, category)
            if mult > max_probs[i]:
                max_probs[i] = mult
                best_cats[i] = category

        r_category_idx = list(words_dict_test.keys()).index(test['categories'][i])
        p_category_idx = list(words_dict_test.keys()).index(best_cats[i])
        
        if p_category_idx == r_category_idx:
            probs['total_cor'] += 1
            probs['tp'][p_category_idx] += 1
        else:
            probs['fp'][p_category_idx] += 1
            probs['fn'][r_category_idx] += 1
            if nomm < 5:
                print("mismatch: ", test['title'][i]+ ","+ test['description'][i]+"\n"+ best_cats[i],"\n", test['categories'][i])
                nomm += 1

probs = {
    'total': len(test['description']),
    'total_cor': 0,
    'fp': [0]*6,
    'fn': [0]*6,
    'tp': [0]*6,
} 

max_probs, best_cats = [0]*len(test['description']), ['leisure-hobbies']*len(test['description'])
calc_probs(max_probs, best_cats, probs)
print("\n")
print("maximum probability for the first 20 posts: ", max_probs[0:20])
print("class detected for the first 20 posts: ",