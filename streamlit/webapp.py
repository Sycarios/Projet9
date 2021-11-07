#Let's Import some librairies
import streamlit as st
import pandas as pd
import numpy as np
from operator import itemgetter
import random
import pickle
# Read ou csv
df=pd.read_csv('df.csv')


#open our embedding
with open('articles_embeddings.pickle','rb') as embedd:
    embedding=pickle.load(embedd)


def find_top_n_indices(data, top=5):
    indexed = enumerate(data)
    sorted_data = sorted(indexed, 
                         key=itemgetter(1), 
                         reverse=True) 
    return [d[0] for d in sorted_data[:top]] 

def recommendFromArticle(article_id, top):
    score = []
    for i in range(0, len(embedding)):
        if(article_id != i):
            cos_sim = np.dot(embedding[article_id], embedding[i])/(np.linalg.norm(embedding[article_id])*np.linalg.norm(embedding[i]))
            score.append(cos_sim)
    
    _best_scores = find_top_n_indices(score, top)
            
    return _best_scores

def reco_base(user_id):
    li=[]
    var=df.loc[user_id]['LIST_click_article_id']
    var = var.replace('[', '').replace(']', '').replace(',', '').split()
    x=[int(i)for i in var]
    x.reverse()  # Avoir les articles les plus récents en premier
    for article in x:
        li.append(random.choice(recommendFromArticle(article,10)))
        if len(li)==5:
            break
    return li 



st.title('Recommandation App')
st.image('image.png')

user_input=st.number_input('Enter the user_id')
submit=st.button('Recommandation')
if submit:
    answer=reco_base(user_input)
    st.text(answer)


#st.server.add_route('recom',recom_callback)
