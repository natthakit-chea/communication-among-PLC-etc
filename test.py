import omronfins.finsudp as finsudp
from omronfins.finsudp import datadef
import time
from multiprocessing import Process, Value, Manager, Lock
import socket

from plc_run import plc_flow, snap_order,login,mode_check
from Image2base64 import decode_fins_data


def main():
    var = Value('i', 0)
    manager = Manager()
    pic = manager.Value(str, '')

    if __name__ == '__main__':
        lock = Lock()
        plc = Process(target=snap_order, args=(var, pic))
        cam = Process(target=decode_fins_data, args=(var, pic))

        plc.start()
        cam.start()

        plc.join()
        cam.join()

if __name__ == '__main__':
    main()

# def decode_fins_data(data_tuple):
#     decoded_str = b''.join(data_tuple).decode('utf-8').rstrip('\x00')
#     return decoded_str

# fins = finsudp.FinsUDP(0, 170)
# ret = fins.open('192.168.10.1', 9600)  # Please change according to your PLC's address.
# fins.set_destination(dst_net_addr=0, dst_node_num=0, dst_unit_addr=0)
# ret, value = fins.read_mem_area(datadef.WR_BIT, 270, 0, 2, datadef.BIT)
# print('value ',value)



#Reading a word from Extended memory area's address 0.
# try:
#     ret, value = fins.read_mem_area(datadef.WR_BIT, 270, 0, 2, datadef.BIT)
#     print("connect",value)
    
# except:
#     print("cannot connect")

# i=0
# value = 0
# while True:
#     # if value == 0:
#     #     ret = fins.write_mem_area(datadef.WR_BIT, 260, 7, 1, (1, datadef.BIT))
#     #     time.sleep(2)
#     ret, value = fins.read_mem_area(datadef.WR_BIT, 270, 0, 1, datadef.BIT)
#     i=i+1
#     print(i, value)
#     time.sleep(1)
    
#     ret, value = fins.read_mem_area(datadef.DM_WORD, 2640, 0, 1, datadef.CHAR)
#     print(decode_fins_data(value))
#     print("connect",value)
#     time.sleep(1)