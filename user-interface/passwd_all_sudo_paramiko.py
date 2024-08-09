#!/data/zhaoyi/miniconda3/envs/tool/bin/python
import paramiko
import os, sys, time
from server_list import servers_global

def check_sudoer():
    id_list = os.popen('id').read()
    return 'sudo' in id_list

def change_password(ip, port, self_username, self_password, target_username, target_password):
    try:
        # 创建 SSH 连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=self_username, password=self_password)

        # 构造 passwd 命令
        command = f'echo -e "{self_password}\\n{target_password}\\n{target_password}" | sudo -S passwd {target_username}'

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
        print(f"[x] Fail: cannot change password for {target_username} on {ip}:{port}: {e}")
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
          r"|_|         -- controls password on LDS's servers" "\n"
          r"                               [sudoer's version]" "\n")
    self_username = os.popen('whoami').read().strip()
    print(f'[+] Hello, {self_username}!')
    
    if not check_sudoer():
        print('[x] you are not sudoers! aborted.')
        exit(0)
    print('[+] identity checked! hello, sudoer.')

    self_password = input(f'[>] {self_username}\'s password: ')
    mask = '*' * 8 + ' ' * (len(self_password) - 8)
    print(f'\x1b[1A[>] {self_username}\'s password: {mask}')

    target_username = input(f'[>] user who will change password: ')

    target_password = input(f'[>] {target_username}\'s new password: ')
    if target_password == '':
        target_password = 'lds_ustc@1958_' + os.urandom(8).hex()
    mask = '*' * 8 + ' ' * (len(target_password) - 8)
    print(f'\x1b[1A[>] {target_username}\'s new password: {mask}')
    
    print(f'[+] Please Check:\n'
          f'    Username: {target_username}\n'
          f'    His/Her new password: {target_password}')
    if input('[>] input `yes` to continue: ').lower() != 'yes':
        print('[+] Quit.')
        exit(0)

    for hostname, ip, port in servers_global:
        print()
        print(f"[+] Changing password for {target_username} on {hostname} ({ip}:{port})...")
        change_password(ip, port, self_username, self_password, target_username, target_password)