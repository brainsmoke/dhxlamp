
import select, termios, tty, sys, os

reset_settings = None
rawfile = None

def start():
    global rawfile, reset_settings
    if not rawfile:
        rawfile = os.fdopen(sys.stdin.fileno(), 'r', 0)
        reset_settings = termios.tcgetattr(rawfile)
        tty.setcbreak(rawfile.fileno())

def stop():
    global reset_settings, rawfile
    if rawfile:
        termios.tcsetattr(rawfile, termios.TCSADRAIN, reset_settings)
        rawfile.close()
        rawfile = None

def getc(timeout = None):
    if select.select([rawfile], [], [], timeout) == ([rawfile], [], []):
        return rawfile.read(1)
    return None

