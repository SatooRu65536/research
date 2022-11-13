import sqlite3
import sys
import time


# ログファイルのパス
LOG_FILE_PATH = f'../log/simulator-2.log'
# データベースのパス
DB_PATH = '../db/simulator2.db'
# 処理の遅延
PROCESS_DELAY = 0.1
# 車の速さ
CAR_SPEED = 10
# 交差点混雑度を検索する時間範囲
CHECK_CONGESTION_RANGE = (-6, 3)
# 混雑と判断されない車の最大数
CONFLICT_NUM = 5
# 交差点到着予定時間を出す上での1台あたりの遅延
ARRIVAL_DELAY = 0.5
# 前方の車1台あたりの遅延
ENTRY_DELAY = 0.2
# 交差点を通過するまでの時間
CAR_PASSED_TIME = 2
# 信号機の時間
TRAFFIC_LIGHT_TIME = (10, 10, 10, 10)
# 黄色信号の時間
TRAFFIC_LIGHT_TIME_YELLOW = 2
# クライアントの時間差をランダムにした時の範囲
TIME_RANDOM_RANGE = (0, 5)
# クライアントデータ　
clients = [
    # 前の車との出発時間の差, スタート位置, ゴール位置
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 0, 'start_node': 'cross_009', 'goal_node': 'cross_004'},
    {'time': 2, 'start_node': 'cross_009', 'goal_node': 'cross_016'},
]
OUTPUT_SETTING = {
    '信号': True,
    '開始': False,
    '探索': False,
    '経路': False,
    '回避': False,
    '接続': True,
    '進入': True,
    '通過': True,
    '移動': False,
    '到着': True,
}


# 以下システム用

start_time = None
arrived_num = 0
is_stop_control = False
args = sys.argv
is_yellow = False
blue_traffic_light = 0
switch_traffic_light_time = 0


class Communication():
    def __init__(self):
        self.connect_clients = []
        self.entry_clients = []
        self.passed_clients = []
        self.client_data = {}

    def add_connect(self, car_id):
        conn = sqlite3.connect(f'{DB_PATH}', isolation_level=None)
        cur = conn.cursor()

        route = [d[0] for d in self.client_data[car_id]['data']]
        origin_cross = route[0]
        now_cross = route[1]
        dest_cross = route[2]

        self.connect_clients.append(car_id)

        # 来る方角を取得
        cur.execute(f'''
            SELECT direction FROM road_info
            WHERE cross_1="{now_cross}" AND cross_2="{origin_cross}"
        ''')
        origin = cur.fetchone()[0]

        # 行く方角を取得
        cur.execute(f'''
            SELECT direction FROM road_info
            WHERE cross_1="{now_cross}" AND cross_2="{dest_cross}"
        ''')
        dest = cur.fetchone()[0]
        cur.execute(f'''
            REPLACE INTO control VALUES (
            "{car_id}", "{now_cross}", {origin}, {dest}, "connect", {time.time()-start_time}
        )''')
        cprint(car_id, '接続', now_cross)

    def add_entry(self, car_id):
        self.entry_clients.append(car_id)
        cprint(car_id, '進入')

    def add_passed(self, car_id):
        conn = sqlite3.connect(f'{DB_PATH}', isolation_level=None)
        cur = conn.cursor()
        self.passed_clients.append(car_id)
        self.client_data[car_id]['data'].pop(0)
        cur.execute(f'DELETE FROM control WHERE car_id="{car_id}"')
        cprint(car_id, '通過')

    def add_client_data(self, car_id, data):
        self.client_data[car_id] = {
            'status': 'connect',
            'data': data
        }

    def get_client_data(self, car_id):
        return self.client_data[car_id]['data']

    def get_next_cross_data(self, car_id):
        return self.client_data[car_id]['data'][0]


def cprint(car_id, status, data=''):
    if status in OUTPUT_SETTING and OUTPUT_SETTING[status]:
        if status == '信号':
            print(f'{status}: {data}')
        else:
            print(f'{car_id}: {status} {data}')

        with open(LOG_FILE_PATH, 'a') as f:
            if status == '信号':
                f.write(f'{status}: {data}\n')
            else:
                f.write(f'{car_id}: {status} {data}\n')


comms = Communication()