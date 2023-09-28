web: web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
streamlit: sh setup.sh && streamlit run app.py