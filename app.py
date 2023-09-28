import streamlit as st
import pandas as pd
import requests
import time
import os


st.title("Gender Predictor")
user_input = st.text_input("Please input names (comma-seperated):")

service_url = os.getenv("SERVICE_URL")

if st.button('Predict'):
    if service_url:
        input_data = {'Names':[name.strip() for name in user_input.split(',')]}
        try:
            response = requests.post(service_url+'/gender_classifier',json=input_data)
            if response.status_code == 200:
                prediction = response.json()
                input = input_data.get('Names')
                op = {"Name":input,"Gender":prediction}

                with st.spinner('Loading Predictions:'):
                    time.sleep(2)

                st.dataframe(data=pd.DataFrame(op),hide_index=True)
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error while making the request: {e}")
    else:
        st.error("SERVICE_URL environment variable is not set.")