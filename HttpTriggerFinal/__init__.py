import logging

import azure.functions as func

import json
import pandas as pd

#read our csv
df=pd.read_csv('HttpTriggerFinal/df_reco.csv')

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
        
        
    if userId>-1:
        rec=df.iloc[userId]["Recommandation"]
        return func.HttpResponse(rec)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully but there is no UserID",
             status_code=200
        )
