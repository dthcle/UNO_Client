import socket
import hashlib
import rsa
import os
import base64
import logging
import time
from util import *
from CONST import *
from PROTOCOL import *

logging.basicConfig(level=logging.INFO,
                    filename='client.log',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Client:
    def __init__(self, game_port=CLIENT_GAME_PORT):
        logging.info(f"Initiate the Client...")
        self.username = ''
        self.password = ''
        self.game_addr = ''
        self.game_port = game_port
        self.is_login = False
        self.match_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_server_socket = None
        self.game_server_addr = None
        logging.info(f"Initiate the Client complete!")

    def set_username_password(self, username, password):
        self.username = username
        self.password = Client.md5_encode(password)

    def login(self):
        logging.info(f"Connect to the match server......")
        self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self._send_login_msg()
        msg = self.match_socket.recv(DATA_PACK_MAX_SIZE)
        protocol, data = response_parser(secret_decode(msg))
        if protocol == STATUS_ALL[OK]:
            self.game_addr = data[J_CLIENT_ADDR]
            self.is_login = True
            logging.info(f"Login successfully!")
            self._init_socket()
            logging.info(f"Close the connection")
        else:
            print(f"ERROR: {STATUS_NAME[STATUS_ALL.index(protocol)]}")
            self._init_socket()

    def logout(self):
        logging.info(f"Logout.....")
        self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self._send_logout_msg()
        return

    def match(self, player_num: int):
        logging.info(f"Matching......")
        self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self._send_match_msg(player_num)
        msg = self.match_socket.recv(DATA_PACK_MAX_SIZE)
        protocol, data = response_parser(secret_decode(msg))
        if protocol == STATUS_ALL[OK]:
            self.game_socket.bind((self.game_addr, self.game_port))
            self.game_socket.listen(1)
            self.game_server_socket, self.game_server_addr = self.game_socket.accept()
            logging.info(f"Matching complete! Begin to start game......")
            self.game_start()
        else:
            print(f"ERROR: {STATUS_NAME[STATUS_ALL.index(protocol)]}")
            self._init_socket()

    def game_start(self):
        logging.info(f"Game Start!")
        msg = self.game_server_socket.recv(DATA_PACK_MAX_SIZE)
        logging.info(f"Get response from game server ({self.game_server_addr})")
        protocol, data = response_parser(secret_decode(msg))
        logging.info(f"内容为 {protocol}: {data}")
        if protocol == GAME_INIT_PROTOCOL:
            # 游戏开始前 向游戏服务器发送自己的用户名 使服务器知道 用户名 和 ip 的绑定关系
            self.game_server_socket.send(secret_encode(request_encoder(CHECK_USER_IDENTITY_PROTOCOL, {J_USERNAME: self.username})))
        else:
            print(f"ERROR: {STATUS_NAME[STATUS_ALL.index(protocol)]}")
        msg = self.game_server_socket.recv(DATA_PACK_MAX_SIZE)
        logging.info(f"Get response from game server ({self.game_server_addr})")
        protocol, data = response_parser(secret_decode(msg))
        logging.info(f"内容为 {protocol}: {data}")
        if protocol == GAME_START_PROTOCOL:
            os.system('cls')
            Game(self.username, data, self.game_server_socket).run()
        else:
            print(f"ERROR: {STATUS_NAME[STATUS_ALL.index(protocol)]}")

    def _send_match_msg(self, player_num: int):
        match_data = {J_CLIENT_PORT: CLIENT_GAME_PORT, J_PLAYER_NUM: str(player_num)}
        # self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self.match_socket.send(secret_encode(request_encoder(MATCH_PROTOCOL, match_data)))

    def _send_login_msg(self):
        user_info = {
            J_USERNAME: self.username,
            J_PASSWORD: self.password
        }
        login_msg = secret_encode(request_encoder(LOGIN_PROTOCOL, user_info))
        self.match_socket.send(login_msg)

    def _send_logout_msg(self):
        logout_msg = secret_encode(request_encoder(LOGOUT_PROTOCOL))
        self.match_socket.send(logout_msg)

    def _request_encode(self, protocol, data: dict):
        pass

    def _response_parse(self, response):
        pass

    def _init_socket(self, name='match'):
        if name == 'game':
            self.game_socket.close()
            self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif name == 'match':
            self.match_socket.close()
            self.match_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def md5_encode(password: str):
        """
        将输入字符串进行 MD5 加密，基本用于数据库中密码加密
        :param password: 输入的密码字符串
        :return: MD5 加密后的密码
        """
        md5_encoder = hashlib.md5()
        md5_encoder.update((PREFIX_SALT+password+SUFFIX_SALT).encode())
        return md5_encoder.hexdigest()


class Game:
    """
    游戏类，所有游戏内的操作都由这个类完成，包括 UI 的生成
    """
    def __init__(self, username, init_data: dict, sock: socket.socket):
        logging.info(f"Init game with data")
        # 当前用户名
        self.username = username
        # 与游戏服务器交互的套接字
        self.socket = sock
        # 当前游戏的进行方向(顺时针还是逆时针)
        self.direction = init_data[J_DIRECTION]
        # 当前玩家的手牌内容
        self.hand_card = init_data[J_HAND_CARD]
        # 当前对局中的玩家的用户名与位次
        self.players_list = init_data[J_PLAYERS_LIST]
        # 当前对局中各玩家的手牌数
        self.hand_card_num_list = init_data[J_HAND_CARD_NUM_LIST]
        # 当前玩家在对局中的位次
        self.self_index = self.players_list.index(self.username)
        # 是否轮到当前玩家出牌
        self.discard = init_data[J_ALLOW_TO_DISCARD]
        # 当前的引导牌
        self.guide = init_data[J_THE_FIRST_GUIDE]
        # 当前玩家的RSA公私钥
        self.public_key = rsa.PublicKey.load_pkcs1(init_data[J_RSA_PUBLIC_KEY])
        self.private_key = rsa.PrivateKey.load_pkcs1(init_data[J_RSA_PUBLIC_KEY])
        logging.info(f"Init game successfully")

    def run(self):
        # 循环绘画UI
        while True:
            self.draw()

            # 刷新率
            time.sleep(1/FPS)

    def draw(self):
        # "绘制"游戏界面
        os.system('cls')
        print("游戏对局中......")
        for each in range(len(self.players_list)-1):
            # index_tmp = clockwise_index_return(self.self_index, each, len(self.players_list))
            index_tmp = queue_index_return(self.self_index+1, each, len(self.players_list), self.direction)
            self.draw_players_info(index_tmp)
        self.draw_user_info()
        self.draw_warning()
        self.draw_user_operation()

    def draw_players_info(self, player_index):
        str_tmp = ''
        player_username = self.players_list[player_index]
        if self.discard == player_username:
            str_tmp += UI_DISCARD_USER
        else:
            str_tmp += UI_NORMAL_USER
        str_tmp += ' ' + player_username + ': ' + str(self.hand_card_num_list[player_index])
        print(str_tmp)

    def draw_user_info(self):
        # 绘制手牌
        # 初始化字符串
        string = ''
        # 占位字符串的初始化
        blank = ' '
        # 卡片头部
        for each in range(self.hand_card_num_list[self.self_index]):
            print(f"+{'-'*CARD_DRAW_LENGTH}+   ", end='')
        print('')
        # 头部数字(符号)
        for each in self.hand_card:
            print(f"|{CARD_CONTENT_DICT[each[CARD_CONTENT_INDEX]]}{blank*(CARD_DRAW_LENGTH-CARD_CONTENT_DRAW_REVISE[each[CARD_CONTENT_INDEX]])}|{blank*CARD_GAP}", end='')
        print('')
        # 卡片颜色
        for each in self.hand_card:
            print(f"|{blank*CARD_COLOR_CENTER_GAP}{CARD_COLOR_DICT[each[CARD_COLOR_INDEX]]}{blank*CARD_COLOR_CENTER_GAP}|{blank*CARD_GAP}", end='')
        print('')
        # 尾部数字(符号)
        for each in self.hand_card:
            print(f"|{blank*(CARD_DRAW_LENGTH-CARD_CONTENT_DRAW_REVISE[each[CARD_CONTENT_INDEX]])}{CARD_CONTENT_DICT[each[CARD_CONTENT_INDEX]]}|{blank*CARD_GAP}", end='')
        print('')
        # 卡片底部
        for each in range(self.hand_card_num_list[self.self_index]):
            print(f"+{'-'*CARD_DRAW_LENGTH}+   ", end='')
        print('')

    def draw_warning(self):
        pass

    def draw_user_operation(self):
        pass


class RSACrypto:
    """
    RSA加密解密的封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def encrypt(msg: str, pub_key, max_length=117):
        """
        通过公钥加密消息，并用base64将其编码成可见字符
        :param msg: 字符串消息明文
        :type: str
        :param pub_key: 公钥
        :param max_length: 最大一次加密长度(超过则进行分段加密)
        :return: 被base64编码后的密文
        :rtype: bytes
        """
        if len(msg) <= max_length:
            return base64.b64encode(rsa.encrypt(msg.encode(), pub_key))
        else:
            tmp_result = b''
            while msg:
                tmp_msg = msg[:max_length]
                msg = msg[max_length:]
                tmp_result += rsa.encrypt(tmp_msg.encode(), pub_key)
            return base64.b64encode(tmp_result)

    @staticmethod
    def decrypt(msg: bytes, pri_key, max_length=128):
        """
        先将编码后的消息用base64解码，然后用私钥解密
        :param msg: 被 base64 编码后的消息密文
        :type: bytes
        :param pri_key: 私钥
        :param max_length: 最大一次解密长度(超过则进行分段解密)
        :return: 消息明文
        :rtype: str
        """
        msg = base64.b64decode(msg)
        if len(msg) <= max_length:
            return rsa.decrypt(msg, pri_key).decode()
        else:
            tmp_result = ''
            while msg:
                tmp_msg = msg[:max_length]
                msg = msg[max_length:]
                tmp_result += rsa.decrypt(tmp_msg, pri_key).decode()
            return tmp_result

