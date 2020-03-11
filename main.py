import os
import getpass
from Entity import *
from util import *

client = Client()

while True:
    if client.is_login:
        print(
            f"   Welcome to back, {client.username}"
        )
    else:
        print(
            "   Welcome!"
        )
    print(
        "   Nice to see you! This is a popular board game, UNO!\n"
        "   \n"
        "                      Powered By Dthcle\n"
        "   Menu\n"
        f"   1. login with a registered account{'(you are logged in)' if client.is_login else ''}\n"
        "   (if you want a account, please contact me(dthcle@gmail.com)!)\n"
        "   \n"
        "   \n"
        "   0. exit\n"
        "   \n"
        "   select your choice:"
        , end='')
    choice = input()
    if choice == '1':
        os.system('cls')
        print(
            "   To Login Your Account\n"
            "   Please Input Your Username:"
            , end='')
        username = input()
        print(
            "   Please input Your Password:"
            , end='')
        password = input()
        # password = getpass.getpass()
        client.set_username_password(username, password)
        client.login()
    elif choice == '0':
        print("See you later...")
        exit(0)
    else:
        os.system('cls')
        print(
            "   Irregular input! Please try again!\n"
            , end='')

