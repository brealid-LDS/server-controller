#!/data/zhaoyi/miniconda3/envs/tool/bin/python
import os, sys, pty, time, subprocess, re

def extract_missing_modules(error_string):
    pattern = r"ModuleNotFoundError: No module named '([^']+)'"
    missing_modules = re.findall(pattern, error_string)
    return missing_modules

def get_stdout_terminal(fd = None):
    if fd is None:
        if os.isatty(sys.stdout.fileno()):
            # 获取当前 stdout 的文件描述符
            fd = sys.stdout.fileno()
        else:
            fd = -1
    if fd != -1:
        return os.ttyname(fd)
    else:
        return "PIPE"

def cuda_ver():
    try:
        output = os.popen("nvidia-smi").read()
        for line in output.split('\n'):
            if 'CUDA Version' in line:
                ver = line.strip('|').split()[-1]
        validate_ver = ['11.8', '11.3', '11.0', '10.2', '10.1']
        for v in validate_ver:
            if ver >= v:
                return v
        return ver
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error occurred: {e.output}")
    except FileNotFoundError:
        raise ValueError("nvidia-smi not found. Ensure that NVIDIA drivers are installed.")


def try_install_module(module):
    if module == 'torch':
        _cuda_ver = cuda_ver()
        print('====> [WARN] torch 包不会自动安装! 存在依赖风险! 建议手动复制命令安装')
        print(f'====> 建议的安装命令 (二选一): ')
        print(f'====>     conda install pytorch torchvision torchaudio pytorch-cuda={_cuda_ver} -c pytorch -c nvidia')
        print(f'====>     pip install -U torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu{_cuda_ver.replace(".", "")}')
        return -1

    conda_required = ['torch_scatter']
    mapping_moduleName = {
        'yaml': 'pyyaml',
        'sklearn': 'scikit-learn',
        'sklearn_extra': 'scikit-learn-extra',
        'Crypto': 'pycryptodome',
        'pwn': 'pwntools',
        'moses': 'cython==0.29.17 && pip install pomegranate==0.12 && pip install molsets', # pomegranate must compiled with cython
        'torch_scatter': 'pyg pytorch-cluster pytorch-scatter -c pyg'
    }
    if module in conda_required:
        installer = 'conda install -y'
    else:
        installer = 'pip install'
    package_name = mapping_moduleName.get(module, module)
    cmd = f'{installer} {package_name}'
    print(f'====> 尝试安装 {module}: {cmd}')
    return os.system(cmd)


def run_command_with_pty(command):
    pid, fd = pty.fork()

    if pid == 0:
        print('====> 子进程 stdout 输出设备:', get_stdout_terminal())
        os.execvp(command[0], command)
    else:
        output = ''
        print('====> 运行命令:', command)
        start_time = time.time()
        while True:
            try:
                buf = os.read(fd, 1024).decode('utf-8')
                if buf:
                    print(buf, end='')
                    output += buf
            except OSError as e:
                break
        _, res = os.waitpid(pid, 0)

        timedelta = time.time() - start_time
        if res:
            print(f'====> [FAIL] 程序异常退出! 返回值: {res}. 耗时 {timedelta:.3f} s')
        else:
            print(f'====> 程序正常终止. 耗时 {timedelta:.3f} s')
            return

        try_solve_attempt = False
        attempt_fail = False

        # 处理 ModuleNotFoundError
        missing_module = extract_missing_modules(output)
        if len(missing_module) != 0:
            print(f'====> 检测到 python 缺失库! 正在执行自动重新安装')
            try_solve_attempt = True

            for module in missing_module:
                if try_install_module(module) != 0:
                    attempt_fail = True

        if try_solve_attempt:
            if not attempt_fail:
                print('====> 尝试重新执行命令')
                run_command_with_pty(command)
            else:
                print('====> 尝试解决问题失败, 程序终止运行, 等待手动解决')

if __name__ == '__main__':
    command = sys.argv[1:]
    if len(command) == 0:
        print('====> [FAIL] Usage: smatlyRun <cmd> [<cmd arg1> ...]')
        exit(0)
    print('====> 当前 stdout 输出设备:', get_stdout_terminal())
    run_command_with_pty(command)