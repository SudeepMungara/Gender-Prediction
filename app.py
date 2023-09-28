import streamlit as st
import pandas as pd
import requests
import time
import os


st.title("Gender Predictor")
user_input = st.text_input("Please input names (comma-seperated):")
if st.button('Predict'):
    os.system('py src/genderClassifyAPI.py')
    input_data = {'Names':[name for name in user_input.split(',')]}
    response = requests.post('http://127.0.0.1:5000/gender_classifier/',json=input_data,verify=False)
    if response.status_code == 200:
        prediction = response.json()
        input = input_data.get('Names')
        op = {"Name":input,"Gender":prediction}
        with st.spinner('Loading Predictions:'):
            time.sleep(2)
        st.dataframe(data=pd.DataFrame(op),hide_index=True)