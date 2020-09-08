import multiprocessing
import time
import sys
import cv2

# 1. run login thread and bluetooth unlock thread

engineerEntering = False

customerEntering = False

# 2. bluetooth unlock and close login and bluetooth unlock thread; run scan qr command line and bluetooth lock thread

# run scan qr command line and bluetooth lock thread

# Engineer leave car; close qr command line and bluetooth lock thread;  back to 1


# 3. Login and close login and bluetooth unlock thread; run customer menu thread

# run customer menu thread

# Customer lock or return car; close customer menu thread; back to 1.

def do_something(quit, foundit):
    while not quit.is_set():
        # find bluetooth engineer
    
    

def sleep(quit, foundit):
    while not quit.is_set():
        for x in range(1000):
            if x == 1001:
                foundit.set()
                break
    print("done for sleep")

quit = multiprocessing.Event()
foundit = multiprocessing.Event()


bluetoothLock = multiprocessing.Process(target= sleep, args= (quit, foundit))
bluetoothLock.start()
# start customer menu thread
customerMenu = multiprocessing.Process(target= do_something, args=(quit, foundit))
customerMenu.start()

foundit.wait()
quit.set()

# start bluetooth lock thread

# start qr command line

# start bluetooth unlock thread

# start login thread


# close customer menu thread

# close bluetooth lock thread

# close qr command line

# close bluetooth unlock thread

# close login thread