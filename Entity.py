import socket
import hashlib
import rsa
import base64
from util import *
from CONST import *
from PROTOCOL import *


class Client:
    def __init__(self, game_port=CLIENT_GAME_PORT):
        self.username = ''
        self.password = ''
        self.game_addr = ''
        self.game_port = game_port
        self.is_login = False
        self.match_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_username_password(self, username, password):
        self.username = username
        self.password = Client.md5_encode(password)

    def login(self):
        self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self._send_login_msg()
        msg = self.match_socket.recv(DATA_PACK_MAX_SIZE)
        protocol, data = response_parser(secret_decode(msg))
        if protocol == STATUS_ALL[OK]:
            self.game_addr = data[CLIENT_ADDR]
            self.is_login = True
        elif protocol == STATUS_ALL[USERNAME_PASSWORD_WRONG]:
            print(f"ERROR: {STATUS_NAME[USERNAME_PASSWORD_WRONG]}")
        else:
            print(f"ERROR: {STATUS_NAME[SERVER_ERROR]}")

    def _send_match_msg(self, player_num: int):
        match_msg = ''
        self.match_socket.connect((MATCH_SERVER_ADDR, MATCH_SERVER_PORT))
        self.match_socket.send(secret_encode(request_encoder(MATCH_PROTOCOL, match_msg)))

    def _send_login_msg(self):
        user_info = {
            USERNAME: self.username,
            PASSWORD: self.password
        }
        login_msg = request_encoder(LOGIN_PROTOCOL, user_info)
        self.match_socket.send(secret_encode(login_msg))

    def _request_encode(self, ):
        pass

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

