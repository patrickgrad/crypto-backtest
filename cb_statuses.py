import colorama
from colorama import Fore, Back, Style
import sys

DEBUG = 1   #set to 1 to enable debug mode, set to 0 to turn off debug mode

ERROR = "[ " + Fore.RED + "ERROR" + Fore.WHITE + " ] : "
SUCCESS = "[ " + Fore.GREEN + "SUCCESS" + Fore.WHITE + " ] : "
RUNNING = "[ " + Fore.GREEN + "RUNNING" + Fore.WHITE + " ] : "
WARNING = "[ " + Fore.YELLOW + "WARNING" + Fore.WHITE + " ] : "

def versioning():
    if('2.7.' not in sys.version):
        print(ERROR + 'Python version 2.7.xx required')
        return False

    if('0.3.' not in colorama.__version__):
        print(WARNING + 'install/upgrade colorama for aesthetic appeal')

    print(SUCCESS + 'crypto-backtest loaded')
    return True

if(not versioning()):
    quit()

colorama.init()
