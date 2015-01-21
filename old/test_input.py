import sys

while 1:
    a=raw_input(' please input > ')
    if a=="q":
        sys.exit()
    elif a=="\x1b[A" or a=="w" or a=="k":
        print "Up pressed!"
    elif a=='\x1b[B' or a=="s" or a=="j":
         print "Down pressed!"
    elif a=='\x1b[C' or a=="d" or a=="l":
        print "Right pressed!"
    elif a=='\x1b[D' or a=="a" or a=="h":
        print "Left pressed!"
    else:
         print "Unknown"
