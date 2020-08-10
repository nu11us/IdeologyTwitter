import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
#import re
#from collections import defaultdict, Counter
#from nltk.corpus import stopwords

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


bernie = "BernieSanders"
aoc  = "AOC"
obama = "BarackObama"
shapiro = "benshapiro"
oreilly = "BillOReilly"
cenk = "cenkuygur"
baier = "BretBaier"
ap = "AP"

def last_month(month_string):
    year, month = month_string.split("-")
    year, month = int(year), int(month)
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    if month >= 10:
        return "{}-{}".format(year,month)
    else:
        return "{}-0{}".format(year,month)

def next_month(month_string):
    year, month = month_string.split("-")
    year, month = int(year), int(month)
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    if month >= 10:
        return "{}-{}".format(year,month)
    else:
        return "{}-0{}".format(year,month)

def get_df(name):
    data = []
    month = "2020-04"
    while os.path.exists("twl/{}/{}-{}.csv".format(name,name,month)):
        month = last_month(month)
    month = next_month(month)
    while month != "2020-05":
        with open("twl/{}/{}-{}.csv".format(name,name,month), "r", encoding='utf-8') as csv:
            header = True
            for line in csv:
                if header:
                    header = False
                else:
                    a = line.split(',')
                    data.append([int(a[-2]),a[1],a[0],','.join(a[6:-5]), embed([','.join(a[6:-5])])[0]])
        month = next_month(month)
    return pd.DataFrame(data, columns=['id', 'username', 'date', 'text', 'embed'])

"""

def get_vocab(df):
    vocab = defaultdict(int)
    lst = df['text'].to_list()
    for e in lst:
        # regex from https://stackoverflow.com/a/50036508
        words = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " URL", e)
        words = re.sub("[^a-zA-Z]", " ", words)
        words = [word for word in words.split(" ") if len(word) > 0]
        for word in words:
            vocab[word] += 1
    for word in stopwords.words("english"):
        vocab.pop(word, None)
    return vocab 

"""
def get_vocab(df, n=(1,1), stops=None, feat_max=None):
    if feat_max is not None:
        vectorizer = CountVectorizer(decode_error="replace", strip_accents='unicode', stop_words=stops, ngram_range=n, max_features=feat_max)
    else:
        vectorizer = CountVectorizer(decode_error="replace", strip_accents='unicode', stop_words=stops, ngram_range=n)
    vec = vectorizer.fit_transform(df['text'])
    print(vectorizer.get_feature_names())

bernie_df = get_df(bernie)
print('b')
aoc_df = get_df(aoc)
print('a')
obama_df = get_df(obama)
print('0')
cenk_df = get_df(cenk)
print('c')

shapiro_df = get_df(shapiro)
print('s')
oreilly_df = get_df(oreilly)
print('or')
#baier_df = get_df(baier)
#print('b')
#ap_df = get_df(ap)
#print('ap')

left_df = pd.concat([bernie_df, aoc_df, obama_df, cenk_df], ignore_index=True)
#right_df = pd.concat([shapiro_df, oreilly_df, baier_df], ignore_index=True)
right_df = shapiro_df
center_df = oreilly_df
#center_df = ap_df

# gun control
gun_control = ['gun', 'firearms', 'rifle', 'pistol', 'ammmo', 'ammunition', 'semiautomatic', 'nra', 'second amendment', '2nd amendment', 'bump stock', 'bear arms', 'school shooting']
left_guns = []
right_guns = []
center_guns = []
for i in gun_control:
    left_guns += list(left_df[left_df['text'].str.contains(i, case=False, regex=False)].index)
    right_guns += list(right_df[right_df['text'].str.contains(i, case=False, regex=False)].index)
    center_guns += list(center_df[center_df['text'].str.contains(i, case=False, regex=False)].index)
left_guns, right_guns, center_guns = list(set(left_guns)), list(set(right_guns)), list(set(center_guns))

# abortion
abortion = ['abortion', 'pro-life', 'pro-choice', 'prolife', 'prochoice', 'pro life', 'pro choice', 'fetus', 'planned parenthood', 'embryo', 'womb', "reproductive right", "reproductive freedom", "reproductive justice"]

left_abortion = []
right_abortion = []
center_abortion = []
for i in abortion:
    left_abortion += list(left_df[left_df['text'].str.contains(i, case=False, regex=False)].index)
    right_abortion += list(right_df[right_df['text'].str.contains(i, case=False, regex=False)].index)
    center_abortion += list(center_df[center_df['text'].str.contains(i, case=False, regex=False)].index)

left_abortion, right_abortion, center_abortion = list(set(left_abortion)), list(set(right_abortion)), list(set(center_abortion))

# capitalism
capitalism = ["free market", "corporation", "free trade", "one percent", "1%", "bank", "capitalism", "welfare", "market", "minimum wage", "economy", "economics", "tax", "inequality", "rich", "poor", "working class", "upper class", "middle class"]
left_cap = []
right_cap = []
center_cap = []
for i in capitalism:
    left_cap += list(left_df[left_df['text'].str.contains(i, case=False, regex=False)].index)
    right_cap += list(right_df[right_df['text'].str.contains(i, case=False, regex=False)].index)
    center_cap += list(center_df[center_df['text'].str.contains(i, case=False, regex=False)].index)

left_cap, right_cap, center_cap = list(set(left_cap)), list(set(right_cap)), list(set(center_cap)) 

# healthcare
health = ["healthcare", "health care", "single payer", "single-payer", "private insurance", "medicare", "medicaid", "obamacare", "medical insurance", "prescription drug", "affordable care act", "public option", "pharmaceutical"]
left_h = []
right_h = []
center_h = []
for i in health:
    left_h += list(left_df[left_df['text'].str.contains(i, case=False, regex=False)].index)
    right_h += list(right_df[right_df['text'].str.contains(i, case=False, regex=False)].index)
    center_h += list(center_df[center_df['text'].str.contains(i, case=False, regex=False)].index)
left_h, right_h, center_h = list(set(left_h)), list(set(right_h)), list(set(center_h))

"""
print("Gun control: left - {}, center - {}, right - {}".format(len(left_guns),len(center_guns),len(right_guns)))
print("Abortion: left - {}, center - {}, right - {}".format(len(left_abortion),len(center_abortion),len(right_abortion)))
print("Capitalism: left - {}, center - {}, right - {}".format(len(left_cap),len(center_cap),len(right_cap)))
print("Healthcare: left - {}, center - {}, right - {}".format(len(left_h),len(center_h),len(right_h)))
"""

def avg_embed(df, lst):
    x = embed([df.loc[i]['text'] for i in lst])
    return sum(x)/len(x)

def cos_sim(a,b):
    return np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))

abor = "It is one of the safest procedures in medicine."
ab = "It is a major cause of maternal death."
e = embed([abor])[0]
f = embed([ab])[0]

ind = 0
val = -2

for index, row in left_df.iterrows():
    a = cos_sim(row['embed'], e)
    if a >= val:
        ind = index
        val = a
        print(val, left_df.loc[ind]['text'])

ind = 0
val = -2
for index, row in right_df.iterrows():
    a = cos_sim(row['embed'], e)
    if a >= val:
        ind = index
        val = a
        print(val, right_df.loc[ind]['text'])