import subprocess
import os

def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    result = subprocess.run(f"pgrep -u {username} | wc -l", shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    def get_descendants(pid):
        out = subprocess.run(['ps', '--ppid', str(pid), '-o', 'pid=', '--no-headers'], capture_output=True, text=True)
        pids = [int(p) for p in out.stdout.split()]
        all_pids = pids.copy()
        for p in pids:
            all_pids.extend(get_descendants(p))
        return all_pids

    all_pids = [root_pid] + get_descendants(root_pid)
    if not all_pids:
        return 0.0
    pid_list = ','.join(str(p) for p in all_pids)
    result = subprocess.run(['ps', '-p', pid_list, '-o', '%mem=', '--no-headers'], capture_output=True, text=True)
    total = 0.0
    for line in result.stdout.splitlines():
        if line.strip():
            total += float(line.strip())
    return total


if __name__ == '__main__':
    user = os.getenv('USER') or os.getenv('USERNAME')
    print(f"Процессов у {user}: {process_count(user)}")
    print(f"Память дерева PID 1: {total_memory_usage(1):.2f}%")