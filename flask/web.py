from flask import Flask, render_template, request, jsonify

from flask_cors import CORS, cross_origin
import json
import pandas as pd
import numpy as np
from operator import itemgetter
import random
import pickle


app= Flask(__name__)
cors = CORS(app) 
df=pd.read_csv('../data/df.csv')


#open our embedding
with open('../../../articles_embeddings.pickle','rb') as embedd:
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


@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/recommandation', methods=["POST"])
def reco():
    if request.method=='POST' :
        user = request.get_json(silent=True)
        id=user['userId']
        #user=json.dumps(user)
        #print(type(user))

        #id=user_id["id"]
        recommandation= reco_base(id)
        recom=json.dumps(recommandation)
        #listToStr = ' '.join([str(elem) for elem in recommandation])
        return recom

    



if __name__ == "__main__":
    app.run(debug=True)


