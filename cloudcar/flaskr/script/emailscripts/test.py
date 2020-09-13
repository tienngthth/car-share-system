from sendmail import *
import sys
try:
    send_mail(str(sys.argv[1]))
    print(sys.argv[1])
except: print("No car ID provided")
mail = send_mail("5")
mail.send()
