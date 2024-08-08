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

def change_password(ip, port, username, old_password, new_password):
    try:
        # 创建 SSH 连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=old_password)

        # 构造 passwd 命令
        command = f'echo -e "{old_password}\\n{new_password}\\n{new_password}" | passwd'

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)

        # 输出结果
        time.sleep(1)  # 等待命令完成
        print(f"Output:\n{stdout.read().decode()}")
        print(f"Errors:\n{stderr.read().decode()}")

    except Exception as e:
        print(f"Failed to change password for {username}@{ip}:{port}: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python batchChangePassword.py {USERNAME} {OLD_PASSWORD} {NEW_PASSWORD}')
        exit(0)

    username = sys.argv[1]
    old_password = sys.argv[2]
    new_password = sys.argv[3]

    # 主程序
    for hostname, ip, port in servers:
        print(f"Changing password for {username} on {hostname} ({ip}:{port})...")
        change_password(ip, port, username, old_password, new_password)