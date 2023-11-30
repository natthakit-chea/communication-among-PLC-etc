import omronfins.finsudp as finsudp
from omronfins.finsudp import datadef
import time 
from fastapi import FastAPI, Query, HTTPException
import requests
import json



# table = {'word':datadef.DM_WORD, 'bt':datadef.WR_BIT}
# read_bit= {
#     'login': (table['bt'], 270, 0, 1, datadef.BIT),
#     'check': (table['bt'], 270, 4, 1, datadef.BIT),
#     'mode': (table['bt'], 270, 1, 3, datadef.BIT), # tuple
# }

# read_word = {  'login': (table['word'], 2000, 0, 9, datadef.CHAR),
#                 'checkmode': (table['word'], 2000, 9, 1, datadef.CHAR),
#                 'model': (table['word'], 2020, 0, 2, datadef.CHAR),
#                 'quantity': (table['word'], 2030, 2, 2, datadef.CHAR),
#                 'serial': (table['word'], 2040, 0, 3, datadef.CHAR),
#                 'pattern': (table['word'], 2060, 0, 1, datadef.CHAR),
#                 }

# write_bit = {  'login_sucess': (table['bt'], 260, 1, 1, (1, datadef.BIT)),
#                 'login_fail': (table['bt'], 260, 2, 1, (1, datadef.BIT)),
#                 'choose_mode_fail': (table['bt'], 260, 4, 1, (1, datadef.BIT)),
#                 'choose_mode_success': (table['bt'], 260, 3, 1, (1, datadef.BIT)),
#                 'model_fail': (table['bt'], 261, 0, 1, (1, datadef.BIT)),
#                 'quantity_fail': (table['bt'], 261, 1, 1, (1, datadef.BIT)),
#                 'serial_fail': (table['bt'], 261, 2, 1, (1, datadef.BIT)),}

# write_word = {  'login': (table['word'], 2000, 0, 9, datadef.CHAR),
#               'pattern': (table['word'], 2300, 0, 2, datadef.CHAR),}

# with open('plc_config.json', 'r') as f:
#   data = json.load(f)
f = open('.venv/plc_config.json')
data = json.load(f)
address = data['plc_address']
data = data['plc_config']
  
fins = finsudp.FinsUDP(0, 170)
ret = fins.open(address, 9600)
fins.set_destination(dst_net_addr=0, dst_node_num=0, dst_unit_addr=0)
             
                          
def decode_fins_data(data_tuple):
    decoded_str = b''.join(data_tuple).decode('utf-8').rstrip('\x00')
    return decoded_str

def readplc(var):
    # Please change according to your PLC's address.
    if var['table'] == 'w':
        ret, value = fins.read_mem_area(datadef.WR_BIT, var['row'], var['col'], var['byte'], datadef.BIT)
        return value
    elif var['table'] == 'd':
        ret, value = fins.read_mem_area(datadef.DM_WORD, var['row'], var['col'], var['byte'], datadef.CHAR)
        return decode_fins_data(value)
    
def writeplc(var,val = 1):
    if var['table'] == 'w':
        v = 1*val
        ret = fins.write_mem_area(datadef.WR_BIT, var['row'], var['col'], var['byte'], (v, datadef.BIT))
    elif var['table'] == 'd':
        ret = fins.write_mem_area(datadef.DM_WORD, var['row'], var['col'], var['byte'], (val, datadef.STR))
        

if __name__ == '__main__':
    print(readplc(data['mode'][4]['text_model']))
    print(type(address))
    a = data['login'][0]['confirm_userid']
    print( readplc(a))
    print(data['mode'][13]['response_sucess_serialnumber'])
    writeplc(data['mode'][13]['response_sucess_serialnumber'])
    # print(readplc(data['plc_config']['login'][0]['confirm_userid']))

