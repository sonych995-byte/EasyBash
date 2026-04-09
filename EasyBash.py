#!/usr/bin/env python3

import subprocess

def commandCheck(text):
    cmd = text.split()

    if len(cmd) == 0:
        return None

    easy_bash_commands = ["for", "rush", "exit"]


    if cmd[0] in easy_bash_commands:
        return cmd[0]
    else:
        return None


def for_easy_bash_command(text):
    cmd = text.split()

    if len(cmd) < 5:
        print("invalid syntax: for (file) in (path) (bash command)")
        return

    file_name = cmd[1]
    paths = cmd[3].split("|")
    bash_cmd = cmd[4]

    # สร้าง command
    bash_command = ""

    for path in paths:
        bash_command += f"cd {path} && "

    bash_command += f"{bash_cmd} {file_name}"

    print("Generated:", bash_command)

    # 🔥 execute จริง
    subprocess.run(bash_command, shell=True)

def rush_easy_bash_command(text):
    cmd = text.split()

    if len(cmd) < 3:
        print("invaild syntax: rush (path) (bash command)")
        return

    paths = cmd[1].split("|")
    bash_cmd = cmd[2]

    bash_command = ""

    for path in paths:
        bash_command += f"cd {path} && "

    bash_command += f"{bash_cmd}"

    print("Generated:", bash_command)

    subprocess.run(bash_command, shell=True)

# main loop
while True:
    text = input("easybash> ")

    easy_bash_command = commandCheck(text)

    if easy_bash_command == "for":
        for_easy_bash_command(text)

    elif easy_bash_command == "rush":
        rush_easy_bash_command(text)


    elif easy_bash_command == "exit":
        print("exit from easy bash")
        break

    else:
        print("unknown command")
