from rw_plc import readplc, writeplc
import time 
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import requests
import numpy as np
from multiprocessing import Process, Value, Array, Lock
from datetime import datetime
import random


url_result1 = 'http://127.0.0.1:8000/result1'
url_result2 = 'http://127.0.0.1:8000/result2'
url_get1 = 'http://127.0.0.1:8000/get1'
url_get2 = 'http://127.0.0.1:8000/get2'

f = open('.venv/plc_config.json')
data = json.load(f)
address = data['plc_address']
data = data['plc_config']

# print(readplc('bt','login'))
# print(readplc('word', 'login'))
# response = requests.post(url=url, json={'username': readplc('word', 'login')})
# print(json.loads(response.text)['result'])

def login():
    print('start: ', readplc(data['login'][0]['confirm_userid']))
    if readplc(data['login'][0]['confirm_userid']) == 1:
        response = requests.post(url=url_result1, json={'username': readplc(data['login'][1]['text_userid'])}, timeout=1)
        if json.loads(response.text)['result'] == 'fail':
            # bug ยิงresponse ตลอดเวลา
            writeplc(data['login'][3]['response_userid_fail'])
            print('fail_login ',readplc(data['login'][3]['response_userid_fail']))
            return False
        else:
            writeplc(data['login'][2]['response_userid_success'])
            print('sucess_login ',readplc(data['login'][2]['response_userid_success']))
            return True
    else:
        return False

def mode_check():
    while True: # wait until click confrim
        if readplc(data['mode'][0]['confirm_mode']) == 0: # bug ใส่1 ใน memory ไม่ได้
            break
    response = requests.post(url=url_result1, json={'mode': 'Manual'})
    if readplc(data['mode'][1]['mode_auto']) == 1: # auto 
        response = requests.post(url=url_result1, json={'mode': 'Auto',
                                                'model': readplc(data['mode'][4]['text_model']),
                                                'quantity': readplc(data['mode'][5]['text_quantity']),
                                                })
        
    elif readplc(data['mode'][2]['mode_rework']) == 1: # rework
        response =requests.post(url=url_result1, json={'mode': 'Rework',
                                                'model': readplc(data['mode'][4]['text_model']),
                                                'serialNumber': readplc(data['mode'][6]['text_serialnumber']),
                                                })
        
    elif readplc(data['mode'][3]['mode_dummy']) == 1: # Dummy
        response =requests.post(url=url_result1, json={'mode': 'Dummy',
                                                'pattern': readplc(data['mode'][7]['text_pattern']),
                                                'quantity': readplc(data['mode'][5]['text_quantity']),})
    return response

def comfrim_model(choice,pattern):
    print('fail_mode: ', readplc(data['mode'][9]['response_mode_fail']))
    if choice == 'fail':
        writeplc(data['mode'][9]['response_mode_fail'])
        writeplc(data['mode'][10]['response_error_model'])
        writeplc(data['mode'][11]['response_error_quantity'])
        writeplc(data['mode'][12]['response_error_serialnumber'])
    elif choice == 'success':
        writeplc(data['mode'][8]['response_mode_success'])
        writeplc(data['mode'][13]['response_sucess_serialnumber'],pattern)
        print('sucess_mode : ',readplc(data['mode'][8]['response_mode_success']))
        print('sucess_serail : ',readplc(data['mode'][13]['response_sucess_serialnumber']))

def snap_order(var,pic):
    time.sleep(1)
    while True:
        # var.value = readplc(data['ocr'][0]['snap']) #w270.6=1
        var.value = random.choice([1,0])
        if var.value == 1:
            break
        # 
        time.sleep(0.1)
    while True:
        if True:
        #if readplc(data['printing_end'][0]['finish_printing']) == 1: #w270.7=1
            #stop snap
            if True:
            #if (readplc(data['ocr'][3]['ocr_position']) == 1)and ( readplc(data['ocr'][2]['ocr_camera']) == 1):

                if readplc(data['ocr'][2]['ocr_camera']) ==0:
                    requests.post(url=url_result2, json={'camera':"Camera Error"})
                    
                response = requests.post(url=url_result2, json={   'camera':readplc(data['ocr'][2]['ocr_camera']),#w270.8=1
                                                        'position':readplc(data['ocr'][3]['ocr_position']),#w270.11=1
                                                        'cusPartNo':readplc(data['data_ocr'][0]['cus_no']),
                                                        'densoPartNo':readplc(data['data_ocr'][1]['denso_no']),
                                                        'serialNumber':readplc(data['data_ocr'][2]['serial_no']),
                                                        'qrCode':readplc(data['data_ocr'][3]['qr_code']),
                                                        'threshold':readplc(data['data_ocr'][4]['threshold']),
                                                        'img':pic.value,
                                                                }, timeout=1)
                print({'camera':readplc(data['ocr'][2]['ocr_camera']),
                                                        'position':readplc(data['ocr'][3]['ocr_position']),
                                                        'cusPartNo':readplc(data['data_ocr'][0]['cus_no']),
                                                        'densoPartNo':readplc(data['data_ocr'][1]['denso_no']),
                                                        'serialNumber':readplc(data['data_ocr'][2]['serial_no']),
                                                        'qrCode':readplc(data['data_ocr'][3]['qr_code']),
                                                        'threshold':readplc(data['data_ocr'][4]['threshold']),
                                                        'img':len(pic.value),
                                                                })
                return response

def plc_flow(var,pic):
    while True:
        login_test = login()
        if login_test == True:
            continue
        else:
            print('hfhh')
            # chooose mode
            while True:
                response1 = mode_check()
                print('hfhh')
                result = json.loads(response1.text)['result']
                pattern = json.loads(response1.text)['pattern']
                
                # choose mode fail
                if result == 'fail':
                    comfrim_model(result,pattern)
                    continue
                elif result == 'success':
                    print('success')
                    # check mode success
                    comfrim_model(result,pattern)
                    break

            #send print to backend
            while True:
                #w270.5=1
                response = requests.post(url=url_result2, json={'printing':readplc(data['continue_printing'][0]['confirm_continue_printing'])})
                # get print from backend
                if json.loads(response.text)['statusPrinter'] == 'stop':
                    print('fail')
                    writeplc(data['printing'][0]['print_running'], 0)#w260.5=0
                    #requests.post(url=webhook_url, json={'status': 'Printer Fail'})
                    break
                    #raise Exception("Status printing fail")
                else:
                    writeplc(data['printing'][0]['print_running'],1)#w260.5=1
                    print('printing_start : ',readplc(data['printing'][0]['print_running']))

                #start snap
                response_snap = snap_order(var,pic)
                #  check information
                if json.loads(response_snap.text)['statusInspection'] == 'OK':
                    if json.loads(response_snap.text)['endPrint'] == 0:
                        if json.loads(response_snap.text)['statusPrinter'] == 'stop':
                            writeplc(data['printing'][0]['print_running'],0)#w260.5=0
                            writeplc(data['ocr'][1]['ocr_finish'],1)#w260.6=1
                            requests.post(url=url_result2, json={'status': 'Printer Fail'})
                            break #return to login
                        else:
                            writeplc(data['printing'][0]['print_running'],1)#w260.5=0
                            writeplc(data['ocr'][1]['ocr_finish'],1)#w260.6=1

                    elif json.loads(response_snap.text)['endPrint'] == 1:
                        writeplc(data['printing'][0]['print_running'],0)#w260.5=0
                        writeplc(data['ocr'][1]['ocr_finish'],1)#w260.6=1
                        writeplc(data['printing_end'][1]['printing_complete'],1)#w260.7=1
                        ## ไม่ครบ
                        option = readplc(data['printing_end'][2]['next_set_user_end'])
                        if option[0] == 1:
                            requests.post(url=url_result2, json={'endOption': 'next'})
                        if option[1] == 1:
                            requests.post(url=url_result2, json={'endOption': 'end'})
                        

                #NG occur
                elif json.loads(response_snap.text)['statusInspection'] == 'NG':
                    writeplc(data['printing'][0]['print_running'],0)#w260.5=0
                    writeplc(data['ocr'][1]['ocr_finish'],0)#w260.6=1
                    writeplc(data['printing_end'][1]['printing_complete'],json.loads(response_snap.text)['endPrint'])#w260.7=1

                    writeplc(data['data_ocr'][5]['error_duplicate'],1)#w261.4=1
                    writeplc(data['data_ocr'][6]['ocr_error'],1)#w261.5=1
                    writeplc(data['data_ocr'][7]['ocr_code_error'],1)#w261.6=1
        break      

if __name__ == '__main__':
    login()



                    
                
                  
                
                

                
                
                
                        
                    
                    
                

                
            
                    

                
            
            
            
            
            
            
            
        
