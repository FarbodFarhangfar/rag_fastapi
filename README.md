# rag_fastapi
NLP RAG (Retrieval-Augmented Generation) with FastAPI


this app work on FastAPI and docker compose

The NLP model is a combination of Retrieval-Augmented Generation and converstional chatbots
the nlp contains of three main parts, embedding the text, retrieving the context and generative model
the retriever uses BM25Retriever
the generator uses mistralai/Mixtral-8x7B-Instruct-v0.1

and there is a pdf extractor for specific pdf.


## instructions

if you want to change the model you need to change rag.py

the FastAPI is run on app.py

there is a config file and utils file that provide necessary configuration and tools


## run
'''
docker compose up --build 
'''