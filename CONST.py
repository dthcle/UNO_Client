class CARD_COLOR:
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    UNIVERSAL = 'U'


class CARD_CONTENT:
    N_0 = '0'
    N_1 = '1'
    N_2 = '2'
    N_3 = '3'
    N_4 = '4'
    N_5 = '5'
    N_6 = '6'
    N_7 = '7'
    N_8 = '8'
    N_9 = '9'
    BLOCK = '10'
    REVERSE = '11'
    ADD2 = '12'
    CHANGE = '13'
    ADD4 = '14'


class CARD_CODE:
    # 获取卡牌的编号(颜色, 内容)
    @staticmethod
    def get_card_code(color, content):
        return color, content


# QUANTITY
DATA_PACK_MAX_SIZE = 2048

# MD5 SALT
PREFIX_SALT = 'prefix_salt'
SUFFIX_SALT = 'suffix_salt'

# SERVER
MATCH_SERVER_ADDR = "127.0.0.1"
MATCH_SERVER_PORT = 20000

# CLIENT
CLIENT_GAME_ADDR = ""
CLIENT_GAME_PORT = 22000

# ENCODE
RSA = 'rsa'

# JSON KEY
USERNAME = 'username'
PASSWORD = 'password'
CLIENT_ADDR = 'client_addr'
ACCEPT_PORT = 'accept_port'
PLAYER_NUM = 'player_num'
