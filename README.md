# Simple Python Summarizer Web App

This a small web app that does an extractive summary from a txt file using nltk. React is used for the frontend and FastAPI for the backend with an OpenAPI POST endpoint,

To run the server you will need conda with the conda-forge channel. In the root folder run:
```
conda config --add channels conda-forge
conda init
conda activate env
conda create --name env --file requirements.txt
python -m nltk.downloader punkt_tab # Download needed nltk files
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8888
```

In the frontend folder run:
```
npm i
npm run dev
```
