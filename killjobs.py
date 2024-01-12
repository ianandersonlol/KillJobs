import subprocess
import argparse
import os
import getpass
from collections import defaultdict

def get_truncated_username(full_username):
    """Truncate the username to match the format used by ps aux."""
    truncated_length = 8
    if len(full_username) > truncated_length:
        return full_username[:truncated_length - 1] + "+"
    return full_username

def get_processes(truncated_user):
    """Get a list of running processes for the current user using the ps command."""
    print("Fetching processes for user:", truncated_user)
    proc = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    lines = out.decode().split('\n')
    user_processes = [line.split() for line in lines[1:] if line and line.split()[0].startswith(truncated_user)]
    print(f"Found {len(user_processes)} processes for user {truncated_user}")
    return user_processes

def kill_process(pid):
    """Kill a process by PID."""
    try:
        os.kill(int(pid), 9)
        print(f"Killed process {pid}.")
    except ProcessLookupError:
        print(f"Process {pid} not found.")
    except Exception as e:
        print(f"Error killing process {pid}: {e}")

def should_ignore_command(command):
    """Determine if the command should be ignored."""
    ignore_list = ['--user', '', 'killjobs.py', 'aux']
    if command in ignore_list or '@pts/' in command:
        return True
    return False

def kill_all_processes(processes, self_pid, ssh_ppid):
    """Kill all processes in the list, except the script and SSH parent process."""
    for process in processes:
        if len(process) > 1 and process[1] not in [self_pid, ssh_ppid]:
            kill_process(process[1])

def main(bulk, all_processes, truncated_user):
    processes = get_processes(truncated_user)
    self_pid = str(os.getpid())
    ssh_ppid = str(os.getppid())  # Parent process, likely the SSH session

    if all_processes:
        kill_all_processes(processes, self_pid, ssh_ppid)
    elif bulk:
        grouped_processes = group_processes(processes)
        for command, pids in grouped_processes.items():
            if not should_ignore_command(command):
                response = input(f"Do you want to kill all processes for command '{command}'? [y/N]: ")
                if response.lower() == 'y':
                    for pid in pids:
                        kill_process(pid)
    else:
        for process in processes:
            if len(process) > 1:
                pid, command = process[1], ' '.join(process[11:])
                if not should_ignore_command(command):
                    response = input(f"Do you want to kill process {pid} for command '{command}'? [y/N]: ")
                    if response.lower() == 'y':
                        kill_process(pid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kill running processes for the current user.")
    parser.add_argument("-bulk", action="store_true", help="Group and handle multiple instances of the same command together.")
    parser.add_argument("-all", action="store_true", help="Kill all processes for the user, excluding the SSH session.")
    args = parser.parse_args()

    full_username = getpass.getuser()
    truncated_user = get_truncated_username(full_username)
    main(args.bulk, args.all, truncated_user)

