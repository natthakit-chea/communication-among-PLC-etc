from multiprocessing import Process, Value, Manager, Lock
from plc_run import plc_flow
from Image2base64 import decode_fins_data

def main():
    var = Value('i', 0)
    manager = Manager()
    pic = manager.Value(str, '')

    if __name__ == '__main__':
        lock = Lock()
        plc = Process(target=plc_flow, args=(var, pic))
        #cam = Process(target=decode_fins_data, args=(var, pic))

        plc.start()
        #cam.start()

        plc.join()
        #cam.join()

if __name__ == '__main__':
    main()
