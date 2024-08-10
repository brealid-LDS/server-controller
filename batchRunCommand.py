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

def run_commmand(ip, port, username, PASSWORD, command):
    try:
        # 创建 SSH 连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=PASSWORD)

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        time.sleep(1)  # 等待命令完成

        # 输出结果
        stdout = stdout.read().decode()
        stderr = stderr.read().decode()
        if stdout.strip():
            print(f"[+] stdout:\n{stdout}")
        if stderr.strip():
            print(f"[+] stderr:\n{stderr}")

        client.close()
    except Exception as e:
        print(f"[x] Failed to run command on {username}@{ip}:{port}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python batchRunCommand.py {USERNAME} {PASSWORD}')
        exit(0)

    username = sys.argv[1]
    password = sys.argv[2]

    # 主程序
    while True:
        print('=' * 80)
        print('[+] input command that you want to run on all servers')
        print('    (type `exit` to quit program)')
        cmd = input('[>] ')
        if cmd == 'exit':
            print('Bye.')
            break
        for hostname, ip, port in servers:
            print(f"[.] Running command on {hostname} ({username}@{ip}:{port})...")
            run_commmand(ip, port, username, password, cmd)