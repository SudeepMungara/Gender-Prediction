from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import re
import os
import uvicorn
import streamlit as st
import pandas as pd
import requests
import time

app = FastAPI()

class model_input(BaseModel):

    Names:list

gender_classifier_model = pickle.load(open('./pickle/gender_classification_model.pkl','rb'))
vector = pickle.load(open('./pickle/train_data_vector.pkl','rb'))

@app.post('/gender_classifier')
def gender_pred(input_parameters: model_input):

    gender = []
    input_data = input_parameters.json()
    input_dict = json.loads(input_data)
    input_name = input_dict['Names']
    regex = re.compile('[^a-zA-Z]')
    input_names = [name.lower() for name in input_name]
    input_names = [regex.sub('',name) for name in input_names]
    input_features = vector.transform(input_names)
    predicted_gender = gender_classifier_model.predict(input_features)
    for i in range(0,len(predicted_gender)):
      if predicted_gender[i] == 0:
        gender.append('Female')
      elif predicted_gender[i] == 1:
         gender.append('Male')
    return gender

st.title("Gender Predictor")
user_input = st.text_input("Please input names (comma-seperated):")
if st.button('Predict'):
    input_data = {'Names':[name for name in user_input.split(',')]}
    response = requests.post('http://localhost:5000/gender_classifier',json=input_data)
    if response.status_code == 200:
        prediction = response.json()
        input = input_data.get('Names')
        op = {"Name":input,"Gender":prediction}
        with st.spinner('Loading Predictions:'):
            time.sleep(2)
        st.dataframe(data=pd.DataFrame(op),hide_index=True)
        
if __name__ == '__main__':
   uvicorn.run(app,host='127.0.0.1',port=5000)