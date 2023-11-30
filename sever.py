from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import uvicorn
import time
app = FastAPI()

class test(BaseModel):
    pass

@app.post('/result1', status_code=200)
def send_data():
    data = {'result': 'success', 'pattern':'1234', 'status': 'OK', 'endPrint':0, 'statusPrinter':'start','statusInspection': 'OK'
            , 'endPrint': 0}
    return data

@app.post('/result2', status_code=200)
def send_data2():
    data = {'result': 'success', 'pattern':'1234', 'status': 'OK', 'endPrint':0, 'statusPrinter':'start','statusInspection': 'OK'
            , 'endPrint': 0}
    return data

@app.post('/img', status_code=200)
def send_data2():
    data = {'result': 'success'}
    return data

@app.get('/get1', status_code=200)
def get_data():
    data = {'result': 'success', 'pattern':'1234', 'status': 'OK', 'endPrint':0}
    time.sleep(0.5)
    return data

@app.get('/get2', status_code=200)
def get_data2():
    data = {'result': 'fail', 'pattern':'1234', 'status': 'NG', 'endPrint':1}
    time.sleep(0.5)
    return data



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
    
