# killjobs.py Documentation

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Bulk Killing](#bulk-killing)
  - [Killing All Processes](#killing-all-processes)
- [Arguments](#arguments)
- [Examples](#examples)
- [Disclaimer](#disclaimer)

## Introduction
`killjobs.py` is a utility script designed to facilitate the killing of processes for the current user on a Unix-like system. The script allows you to kill individual processes, group and handle multiple instances of the same command together, or kill all processes for the user.

## Requirements
To use `killjobs.py`, you need to have Python installed on your Unix-like system. The script also utilizes common Unix utilities such as `ps`, `kill`, and requires subprocess and argparse modules from Python standard library.

## Usage

### Basic Usage
To use `killjobs.py`, run the script without any arguments to be prompted for each process whether you would like to kill it:
```bash
python killjobs.py
```

### Bulk Killing
If you want to group and handle multiple instances of the same command together, use the `-bulk` argument:
```bash
python killjobs.py -bulk
```
You will be prompted to kill all processes for each command group.

### Killing All Processes
To kill all processes for the user, excluding the SSH session, use the `-all` argument:
```bash
python killjobs.py -all
```
This argument will not prompt for confirmation for each process.

## Arguments
- `-bulk`: Group and handle multiple instances of the same command together.
- `-all`: Kill all processes for the user, excluding the SSH session.

## Examples
Kill individual processes with confirmation prompts:
```bash
python killjobs.py
```

Kill processes in bulk, grouped by command, with confirmation prompts:
```bash
python killjobs.py -bulk
```

Kill all user's processes without confirmation prompts:
```bash
python killjobs.py -all
```

## Disclaimer
Use `killjobs.py` with caution as it can terminate critical processes, which may lead to system instability or data loss. Always ensure you have saved your work and understand the implications of terminating processes on your system.

Note: This script must be run with appropriate permissions to kill the intended processes. In some cases, you might need to run it with elevated privileges using `sudo`, depending on the ownership of the processes you wish to kill.
Markdown documentation has been created: ('killjobs', '.py').md