import os
import time
from Entity import Client


# 菜单可以使用栈来实现返回操作
def ui_menu(client: Client):
    """

    :param client:
    :return:
    """
    menu_option_name = ['Login with a registered account', 'Match a game', 'setting']
    menu_option_func = [func_login, func_match, func_setting]
    menu_choice = [str(each+1) for each in range(len(menu_option_name))]
    login_fun = [1, 2]
    no_login_fun = [0, 2]
    available_option = []
    print(
        "   \n"
        "   Nice to see you! This is a popular board game, UNO!\n"
        "   \n"
        "                      Powered By Dthcle\n"
        "   Menu")

    if client.is_login:
        for each in range(len(login_fun)):
            print('\t' + str(each+1) + '.' + menu_option_name[login_fun[each]])
            available_option.append(menu_option_func[login_fun[each]])
    else:
        for each in range(len(no_login_fun)):
            print('\t' + str(each+1) + '.' + menu_option_name[no_login_fun[each]])
            available_option.append(menu_option_func[no_login_fun[each]])
    print(
        "   \n"
        "   \t0. Exit\n"
        "   Please input your choice:"
        , end='')
    choice = input()
    try:
        choice = int(choice)
    except ValueError:
        os.system('cls')
        print(
            "   Irregular input!\n"
            , end='')
        return

    if choice <= len(available_option):
        available_option[choice-1](client)
    elif choice == '0':
        print("See you later...")
        time.sleep(3)
        exit(0)
    else:
        os.system('cls')
        print(
            "   Irregular input!")
        return


def func_login(client: Client):
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
    client.set_username_password(username, password)
    client.login()


def func_match(client: Client):
    os.system('cls')
    print(
        "   Please input how many players you want to play with(include yourself)\n"
        "   (0 to exit)\n"
        "   How many? Number: "
        , end='')
    player_num = input()
    try:
        player_num = int(player_num)
    except ValueError:
        os.system('cls')
        print(
            "   Irregular input!\n"
            , end='')
        return

    client.match(player_num)


def func_setting(client: Client):
    pass
