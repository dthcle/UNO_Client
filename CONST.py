class CARD_COLOR:
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    UNIVERSAL = 'U'


CARD_COLOR_DICT = {
    CARD_COLOR.RED: '红',
    CARD_COLOR.BLUE: '蓝',
    CARD_COLOR.YELLOW: '黄',
    CARD_COLOR.GREEN: '绿',
    CARD_COLOR.UNIVERSAL: '黑'
}


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


CARD_CONTENT_DICT = {
    CARD_CONTENT.N_0: '0',
    CARD_CONTENT.N_1: '1',
    CARD_CONTENT.N_2: '2',
    CARD_CONTENT.N_3: '3',
    CARD_CONTENT.N_4: '4',
    CARD_CONTENT.N_5: '5',
    CARD_CONTENT.N_6: '6',
    CARD_CONTENT.N_7: '7',
    CARD_CONTENT.N_8: '8',
    CARD_CONTENT.N_9: '9',
    CARD_CONTENT.BLOCK: '×',
    CARD_CONTENT.REVERSE: '↙↗',
    CARD_CONTENT.ADD2: '+2',
    CARD_CONTENT.CHANGE: '⊕',
    CARD_CONTENT.ADD4: '+4'
}


CARD_CONTENT_DRAW_REVISE = {
    CARD_CONTENT.N_0: 1,
    CARD_CONTENT.N_1: 1,
    CARD_CONTENT.N_2: 1,
    CARD_CONTENT.N_3: 1,
    CARD_CONTENT.N_4: 1,
    CARD_CONTENT.N_5: 1,
    CARD_CONTENT.N_6: 1,
    CARD_CONTENT.N_7: 1,
    CARD_CONTENT.N_8: 1,
    CARD_CONTENT.N_9: 1,
    CARD_CONTENT.BLOCK: 2,
    CARD_CONTENT.REVERSE: 4,
    CARD_CONTENT.ADD2: 2,
    CARD_CONTENT.CHANGE: 2,
    CARD_CONTENT.ADD4: 2
}


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
CLIENT_GAME_PORT = 23000

# ENCODE
RSA = 'rsa'

# JSON KEY
J_USERNAME = 'username'
J_PASSWORD = 'password'
J_CLIENT_ADDR = 'client_addr'
J_CLIENT_PORT = 'client_port'
J_PLAYER_NUM = 'player_num'
J_DIRECTION = 'direction'
J_PLAYERS_LIST = 'players_list'
J_HAND_CARD_NUM_LIST = 'hand_card_num_list'
J_HAND_CARD = 'hand_card'
J_CARD_CODE = 'card_code'
J_GUIDE_COLOR = 'guide_color'
J_ERROR_CARD_CODE = 'error_card_code'
J_ALLOW_TO_DISCARD = 'allow_to_discard'
J_THE_FIRST_GUIDE = 'the_first_guide'
J_RSA_PUBLIC_KEY = 'rsa_public_key'
J_RSA_PRIVATE_KEY = 'rsa_private_key'

# CARD
CARD_COLOR_INDEX = 0
CARD_CONTENT_INDEX = 1

# CLIENT UI
UI_DISCARD_USER = '#'
UI_NORMAL_USER = '-'
FPS = FRAMES_PER_SECOND = 3

CARD_DRAW_LENGTH = 6
CARD_GAP = 3
CARD_COLOR_CENTER_GAP = 2

