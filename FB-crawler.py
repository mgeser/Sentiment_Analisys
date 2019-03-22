import facebook as fb
from textblob import TextBlob
import requests
import numpy as np
import pandas as pd
import re

corpus = []
datasets = []

graph = fb.GraphAPI(access_token="Input_your_Facebook-Dev_token_here")

# KATA KUNCI SEARCH
key = '2019GantiPresiden'
# LIMIT PENCARIAN (page, post, comment)
limit = 5
# REQUEST
req = "/search?q=%s&type=page&limit=%s"%(key, limit)

pages = graph.request(req)
pagelist = pages['data']

# dapatkan 5 post dari masing-masing page
for page in pagelist:
    posts = graph.request('/%s/posts?%s'%(page['id'], limit))
    postslist = posts['data']
    # dapatkan 5 comment dari masing-masing post
    for post in postslist:
        comments = graph.request('/%s/comments?%s'%(post['id'], limit))
        commentlist = comments['data']
        # dapatkan detail(text) dari masing-masing comment
        for comment in commentlist:
            # print comment['message']
            comment_clean = re.sub('[^a-zA-Z]', ' ', comment['message'])
            comment_clean = comment_clean.lower()
            corpus.append(comment_clean)
           
            #message = TextBlob(comment['message'])
            #datasets.append([comment['message'], message.sentiment.polarity])

# print hasil

for data in corpus:
    if(TextBlob(data).sentiment.polarity <= 0):
        sentiment = 'negative'
    else: sentiment = 'positive'

    datasets.append([data, sentiment])

array = np.array(datasets)
#np.savetxt('hasil.csv', array, delimiter=',')
print array
df = pd.DataFrame(array)
df.to_csv('hasil.csv')
