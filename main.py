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
from io import StringIO


app = FastAPI()


origins = [

    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
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
async def handle_form(file:UploadFile=File(...)):
    content = await file.read()
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfile")
async def create_upload_file(csv_file: UploadFile = File(...)):
    data=csv_file.file
    data=csv.reader(codecs.iterdecode(data,'utf-8'),delimiter='\t')
    header=data.__next__()
    df=pd.DataFrame(data,columns=header)

    

    return df







@app.get("/")
async def main():
    return {"message": "Hello World"}
