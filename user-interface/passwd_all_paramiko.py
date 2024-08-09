#!/data/zhaoyi/miniconda3/envs/tool/bin/python
import paramiko
import os, sys, time
from server_list import servers_global

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
        time.sleep(0.5)  # 等待命令完成
        stdout = stdout.read().decode()
        stderr = stderr.read().decode()
        
        if 'passwd:' in stderr:
            result = stderr.split('passwd:')[-1].strip()
        else:
            result = stdout.split('passwd:')[-1].strip()
            
        if 'successfully' not in result:
            raise Exception(result)
        print(f'[+] Success: {result}')

    except Exception as e:
        print(f"[x] Fail: cannot change password for {username}@{ip}:{port}: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    if len(sys.argv) != 1:
        help()
        exit(0)

    print('=' * 80)
    print(r"                                 _         _ _" "\n"
          r"                                | |       | | |" "\n"
          r" _ __   __ _ ___ _____      ____| |   __ _| | |" "\n"
          r"| '_ \ / _` / __/ __\ \ /\ / / _` |  / _` | | |" "\n"
          r"| |_) | (_| \__ \__ \\ V  V / (_| | | (_| | | |" "\n"
          r"| .__/ \__,_|___/___/ \_/\_/ \__,_|  \__,_|_|_|" "\n"
          r"| |" "\n"
          r"|_|         -- controls password on LDS's servers" "\n")
    username = os.popen('whoami').read().strip()
    print(f'[+] Hello, {username}!')

    old_password = input(f'[>] {username}\'s current password: ')
    mask = '*' * 8 + ' ' * (len(old_password) - 8)
    print(f'\x1b[1A[>] {username}\'s current password: {mask}')

    new_password = input(f'[>] {username}\'s new password: ')
    mask = '*' * 8 + ' ' * (len(new_password) - 8)
    print(f'\x1b[1A[>] {username}\'s new password: {mask}')
    
    if old_password == new_password:
        print('[x] The password is the same as the old one!')
        print('[x] Aborted.')
        exit(0)

    for hostname, ip, port in servers_global:
        print()
        print(f"[+] Changing password for {username} on {hostname} ({ip}:{port})...")
        change_password(ip, port, username, old_password, new_password)