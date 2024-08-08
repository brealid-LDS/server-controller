import paramiko
import getpass
import time
import sys


servers = [
    ('Han5', '210.45.70.63', 622),
    ('Sui1', '210.45.70.63', 1022),
    ('Sui2', '210.45.70.63', 922),
    ('Sui3', '210.45.70.63', 822),
    ('Sui4', '210.45.70.63', 522),
    ('Sui5', '210.45.70.63', 722),
    ('Tang1', '210.45.70.63', 422),
    ('Tang2', '210.45.70.63', 322),
    ('Tang3', '210.45.70.63', 1322),
    ('Song1', '210.45.70.63', 1122),
]

# servers = [
#     ('Local-CentOS-Test', '192.168.137.9', 22)
# ]

def connection_test(ip, port, username, password):
    try:
        # 创建 SSH 连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password)
        print(f"connected.")
        client.close()
    except Exception as e:
        print(f"failed.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python connectionTest.py {USERNAME} {PASSWORD}')
        exit(0)

    username = sys.argv[1]
    password = sys.argv[2]

    # 主程序
    for hostname, ip, port in servers:
        print(f"Test Connection for {username} on {hostname} ({ip}:{port})...")
        connection_test(ip, port, username, password)