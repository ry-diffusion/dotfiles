from os import rename
from random import randint


try:
    def getch():
        from msvcrt import getch
        return getch().decode("utf-8")
except ImportError:
    # Credits: https://github.com/joeyespo/py-getch/blob/master/getch/getch.py
    def getch() -> str:
        """
        Gets a single character from STDIO.
        """
        import sys
        import tty
        import termios

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def confirm(prompt: str = "") -> bool:
    print(prompt, flush=True, end=" [y/n]: ")
    
    confirmed = getch().lower() == "y"
    if confirmed:
        print("YES!", end="")
    else:
        print("NO!", end="")
    return confirmed


def backup_and_remove(target: str):
    rename(target, target + f"-sup-{randint(0, 100)}-bak")
