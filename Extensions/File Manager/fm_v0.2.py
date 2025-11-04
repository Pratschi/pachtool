# PachTool Extension /fm/Pratschi/0.2/Pratchi's File Manager/

print("Loading File Manager...")
import os, json

currpath = os.getcwd()

while True:
    cmd = input(f"\n[FM] {currpath} ~ ")
    if cmd.startswith("cd"):
        if len(cmd.split(" ")) == 1:
            currpath = os.getcwd()
        else:
            if cmd.split(" ")[1] == "..":
                currpath = os.path.dirname(currpath)
            elif (cmd.split(" ")[1].startswith("/") or cmd.split(" ")[1].startswith("\\")) and os.path.isdir(cmd.split(" ")[1]):
                currpath = cmd.split(" ")[1]
            elif os.path.isdir(os.path.join(currpath, cmd.split(" ")[1])):
                currpath = os.path.join(currpath, cmd.split(" ")[1])
            elif os.path.isfile(os.path.join(currpath, cmd.split(" ")[1])):
                print(f"[FM] ERROR: {cmd.split(' ')[1]} Is a file!")
            else:
                print(f"[FM] ERROR: {cmd.split(' ')[1]} Folder doesn't exist!")
    elif cmd.startswith("ls"):
        if len(cmd.split(" ")) > 1:
            if os.path.exists(os.path.join(currpath, cmd.split(" ")[1])):
                for i in os.listdir(os.path.join(currpath, cmd.split(" ")[1])):
                    print(f"    {i}{' (Folder)' if os.path.isdir(os.path.join(currpath, i)) else ''}")
            elif os.path.isfile(os.path.join(currpath, cmd.split(" ")[1])):
                print(f"[FM] ERROR: {os.path.join(currpath, cmd.split(' ')[1])} Is a file!")
            else:
                print(f"[FM] ERROR: {os.path.join(currpath, cmd.split(' ')[1])} Folder doesn't exist!")
        else:
            for i in os.listdir(currpath):
                print(f"    {i}{' (Folder)' if os.path.isdir(os.path.join(currpath, i)) else ''}")
    elif cmd.startswith("quit"):
        break
    else:
        print("[FM] ERROR: Unknown command!")
