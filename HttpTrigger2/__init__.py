import logging

import azure.functions as func

import json
import pandas as pd
import numpy as np
from operator import itemgetter
import random
import pickle

#read our csv
df=pd.read_csv('HttpTrigger2/df.csv')

#open our embedding
with open('HttpTrigger2/articles_embeddings.pickle','rb') as embedd:
    embedding=pickle.load(embedd)

# Start Functions
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
# End Functions
    



    
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')
        
        
    if userId:
        id=int(userId)
        recommandation=reco_base(id)
        rec = json.dumps(recommandation)
        return func.HttpResponse(rec)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully but there is no UserID",
             status_code=200
        )