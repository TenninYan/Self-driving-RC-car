import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
       import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

while True:
    getch = _Getch()
    x = getch()
    a = str(x)

   # if (int(x) == 1):
   #     print "\n"
   #     print 'correct'
   #     print x
   # else:
   #     print "\n"
   #     print 'wrong'
   #     print x
   #
   #
   # a=raw_input(' please input > ')

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
