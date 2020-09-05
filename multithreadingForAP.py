import threading
import time
import sys
from source.qrcode import start_scanning

# 1. run login thread and bluetooth unlock thread


# 2. bluetooth unlock and close login and bluetooth unlock thread; run scan qr command line and bluetooth lock thread

# run scan qr command line and bluetooth lock thread

# Engineer leave car; close qr command line and bluetooth lock thread;  back to 1


# 3. Login and close login and bluetooth unlock thread; run customer menu thread

# run customer menu thread

# Customer lock or return car; close customer menu thread; back to 1.

stage1 = True

def do_something():
    print ("Wait for bluetooth")


def sleep():
    if(input() != None):
        global stage1
        stage1 = False


# start customer menu thread
def start_customer_menu():
    customerMenu = threading.Thread(target= do_something)
    customerMenu.start()

# start bluetooth lock thread
def start_bluetooth_lock():
    bluetoothLock = threading.Thread(target= sleep)
    bluetoothLock.start()
    bluetoothLock.join()
# start qr command line

# start bluetooth unlock thread

# start login thread


while stage1:
    start_customer_menu()
    start_bluetooth_lock()
    time.sleep(1)


# close customer menu thread

# close bluetooth lock thread

# close qr command line

# close bluetooth unlock thread

# close login thread