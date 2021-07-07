try:
    import shutil
    import os
    from typing import Optional
    import uvicorn
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi import FastAPI,Body,Request,File,UploadFile
    from typing import ContextManager
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    import json
    import urllib.parse
    import numpy as np
    import csv
    import requests
    import codecs
    from pathlib import Path 
    from io import StringIO
except Exception as e: print("some package is missing" + str(e))

app = FastAPI()



origins = [

    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
@app.get("/")
def read_root():
    return {"Hello World"}

@app.post("/submitform")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfile")
# async def create_upload_file(file: UploadFile = File(...)):
async def create_upload_file(csv_file: UploadFile = File(...)):
    try:
        with open(f'{csv_file.filename}',"wb") as buffer:
            csvfile=shutil.copyfileobj(csv_file.file,buffer)
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CACHE_DIR=os.path.join(BASE_DIR,'fastapi')
        
        nameoffile=csv_file.filename
        dataset=os.path.join(CACHE_DIR,nameoffile)
        

        df=pd.read_csv(dataset,delimiter = ',')
        df.fillna("",inplace=True)
        data=df.to_dict(orient='records')

        client = pymongo.MongoClient("mongodb+srv://dheerajkumarblr:"+ urllib.parse.quote("dheerajdk@234") +"@cluster0.zeviv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        
        db=client["techpath"]
        mongores=db.csvfile.insert_many(data)
        result = df.to_json(orient="records")
        return {"filename": csv_file.filename,"csvdata":result}
    
    except Exception as e: 
        return {str(e)}
        print("code error" + str(e))
    
    

    








@app.get("/")
async def main():
    return {"message": "Hello World"}
