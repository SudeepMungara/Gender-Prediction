from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import re
import os
import uvicorn


app = FastAPI()

class model_input(BaseModel):

    Names:list

gender_classifier_model = pickle.load(open('./pickle/gender_classification_model.pkl','rb'))
vector = pickle.load(open('./pickle/train_data_vector.pkl','rb'))

@app.post('/gender_classifier/')
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
        
if __name__ == '__main__':
   uvicorn.run(app,host='127.0.0.1',port=5000)