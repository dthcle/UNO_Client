import json
import rsa
from CONST import *


def request_encoder(protocol: str, data: dict):
    """
    将即将发送给服务器的数据编码成 json 字符串
    :param protocol: 操作名称
    :param data: 数据包
    :return: 编码完成的瞬狙
    """
    tmp = {
        "request": protocol,
        "data": data
    }
    return json.dumps(tmp)


def response_parser(json_data: str):
    """
    将服务器返回的结果解析为 python 对象
    :param json_data: 原 json 字符串
    :return: 解析完成的数据，包含一个 状态 和一组 数据
    """
    tmp = json.loads(json_data)
    protocol = tmp["response"]
    data = tmp["data"]
    return protocol, data


def secret_encode(msg, encode_fun=None, key=None):
    """
    将待发送的信息加密
    :param msg: 需要加密的信息内容
    :param encode_fun: 加密算法，默认为无(None)
    :param key: 加密算法的密钥
    :return: 加密后的信息
    :rtype: bytes
    """
    tmp_msg = ''
    if not encode_fun:
        tmp_msg = msg.encode()
    elif encode_fun == RSA:
        tmp_msg = rsa.encrypt(msg, key)

    return tmp_msg


def secret_decode(msg, encode_fun=None, key=None):
    """
    将收到的加密信息解密
    :param msg: 已被加密的信息
    :param encode_fun: 解密算法
    :param key: 加密算法解密的密钥
    :return: 解密后的信息
    :rtype: str
    """
    tmp_msg = ''
    if not encode_fun:
        tmp_msg = msg.decode()
    elif encode_fun == RSA:
        tmp_msg = rsa.decrypt(msg, key)

    return tmp_msg



