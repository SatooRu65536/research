# 自動車側の仮のプログラム

import json
import socket
import time
import random
import sys

IPADDR: str = "127.0.0.1"
PORT: int = 0

with open('./port.txt', 'r') as f:
    PORT = int(f.read())
print('PORT:', PORT)

CAR_ID = 'car_' + str(random.randint(10000, 99999))

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))
args = sys.argv


def get_encode_to_send(status, tag_id, destination) -> bytes:
    data: dict = {'car_id': str(CAR_ID), 'status': status, 'tag_id': tag_id, 'destination': destination}
    data_json: str = json.dumps(data)
    data_encode: bytes = data_json.encode('utf-8')

    return data_encode


def get_decode_data(data) -> dict:
    data_decode: str = data.decode('utf-8')
    data_py_obj: dict = json.loads(data_decode)

    return data_py_obj


def communication() -> None:
    if len(args) == 3:
        tag_id = f'tag_{args[1]}_connect_000_id'
        destination = args[2]
    else:
        tag_id = 'tag_n_connect_000_id'
        destination = 1
        print()

    # 接続報告-送信
    print('< connect')
    send_data: bytes = get_encode_to_send('connect', tag_id, destination)
    sock.send(send_data)

    # 指示-受信
    get_data: dict = get_decode_data(sock.recv(1024))
    print('>', get_data)

    if get_data['operate'] == 'stop':
        # 進入指示-受信
        get_data = get_decode_data(sock.recv(1024))
        print('>', get_data)

    print('交差点通過中...')
    time.sleep(1)

    # 通過済報告-送信
    send_data: bytes = get_encode_to_send('passed', 'tag_s_connect_000_id', destination)
    sock.send(send_data)
    print('< passed')


def main() -> None:
    communication()


if __name__ == '__main__':
    print('⚡ tmp_client.py start')
    main()