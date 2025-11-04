pdata = {
    "version": 1.0,
    "cmdlist": {
        "quit": "Exit program",
        "help": "Show command list",
        "ext": "Run and Manage extensions",
        "data": "Manage SheelTool data"
    },
    "extensions": {},
    "extpath": [],
    "debugmode": True,
}

def savedata(confirmation:bool=True, sdata=None, hide=False, force=False):
    sdata = globals()["data"] if sdata is None else sdata
    import json
    try:
        if not confirmation or input("\nSave data? (y/n) > ").lower() == "y":
            if not hide:
                print("Saving data...")
            with open("pachtool_data.json", "w") as f:
                json.dump(sdata, f, indent=4)
        if not hide:
            print("Data correctly saved!")
    except KeyboardInterrupt:
        if not force:
            print("\nData save cancelled.")
        else:
            savedata(confirmation=confirmation, sdata=sdata, hide=hide, force=True)

def formatcmd(cmd:str):
    """
    Formats cmd into a dict with this structure:
        cmd: The command (single-word string)
        args: The arguments (list)
        flags: The flags (list, those are args that start with '-')
        longflags: The long flags (dict, those are args that start with '--', the key value is the value of the flag given by '=' and None if no value is given)

    Example: cp file1.txt file2.txt -r --verbose=1
        cmd: cp
        args: ["file1.txt", "file2.txt"]
        flags: ["r"]
        longflags: "verbose": "1"}
    """
    finalcmd = {"cmd": "", "args": [], "flags": [], "longflags": {}}
    splitcmd = cmd.lower().split(" ")
    finalcmd["cmd"] = splitcmd.pop(0)

    for word in splitcmd:
        if word.startswith("--"):
            if len(word.split("=")) > 2:
                print(f"Invalid argument: {word}")
            elif len(word.split("=")) == 2:
                finalcmd["longflags"][word.split(
                    "="[1])] = word.split("=")[0].replace("--", "1")
            else:
                finalcmd["longflags"][word] = 0
        elif word.startswith("-"):
            finalcmd["flags"].append(word.replace("-", "1"))
        else:
            finalcmd["args"].append(word)

    return finalcmd

def giveerror(type:str, error:str, cmd:str):
    """
    Give an error to the user.
        type: The type of error (arg_missing, arg_unknown)
        error: The info for that type
        cmd: The command that gave the error

    type = arg_missing:
        error: The argument that is missing (If empty, no argument is specified)
    type = arg_unknown:
        error: The argument that is unknown
    """
    if type == "arg_missing":
        print(f"ERROR: Missing argument{f' <{error}>' if error != '' else ''}: See '{cmd} help' to see arg list")
    elif type == "arg_unknown":
        print(f"ERROR: Unknown argument <{error}>: See '{cmd} help' to see arg list")
    else:
        raise Exception("Invalid error type!")

def loaddata():
    import os, json
    if os.path.isfile("shelltool_data.json") and input("Old data save detected, load data? (y/n) > ").lower() == "y":
        print("Loading data...")
        try:
            with open("shelltool_data.json", "r") as f:
                data = json.load(f)
            if len(pdata) > len(data):
                print("WARNING: Data is outdated! Adding missing data...")
                for i in pdata:
                    if i not in data:
                        data[i] = pdata[i]
                savedata(confirmation=False, sdata=data, hide=True, force=True)
            return data
        except json.decoder.JSONDecodeError:
            print("ERROR: Failed to load data, file is corrupted!\nLoading default data...")
            return pdata
        except Exception as e:
            print(f"ERROR: Failed to load data: {e}\nLoading default data...")
            return pdata
    else:
        return pdata

def main():
    print("\nLoading PachTool...")
    import os
    extensions = {}
    unknown_used = False
    unknown_show = False    
    data = loaddata()
    print(f"\nPachTool v{data['version']} {'[DEBUG MODE] ' if data['debugmode'] else ''}- Made by Pratschi\ngithub.com/Pratschi/PachTool | replit.com/@Pratschi/PachTool")
    while True:
        if not unknown_used:
            unknown_show = False
        cmd = formatcmd(input("\nPachTool > "))
        unknown_used = False

        if cmd["cmd"] == "quit":
            savedata(confirmation=True, sdata=data, hide=False, force=True)
            exit(0)
        elif cmd["cmd"] == "help":
            print("\nCommand list:")
            for i in data["cmdlist"]:
                print(f"    {i} | {data['cmdlist'][i]}")
        elif cmd["cmd"] == "ext":
            if len(cmd["args"]) == 0:
                giveerror("arg_missing", "", "ext")
            elif cmd["args"][0] == "help":
                print("\nExtensions Available Args:")
                print("    help                | Show this help")
                print("    list                | List all extensions")
                print("    install <path>      | Install a extension from file")
                print("    uninstall <ext>     | Uninstall a extension")
                print("    run <ext>           | Run an extension")
                print("    reload <ext>        | Reload extensions (Can be multiple, if not specified, reloads all)")
                print("    rename <ext> <name> | Rename an extension")
                print("    info <ext>          | Show info about an extension")
                print("    addtopath <ext>     | Use an extension as a main command")
            elif cmd["args"][0] == "reload":
                print("Reloading extensions...")
                if len(cmd["args"]) == 1:
                    for i in data["extensions"]:
                        try:
                            with open(data["extensions"][i]["file"], "r") as f:
                                firstline = f.readline().strip()
                                content = f.read()
                                data["extensions"][i]["name"] = firstline.split("/")[4]
                                data["extensions"][i]["version"] = firstline.split("/")[3]
                                data["extensions"][i]["author"] = firstline.split("/")[2]
                                data["extensions"][i]["file"] = firstline.split("/")[1]
                                data["extensions"][i]["code"] = content
                        except FileNotFoundError:
                            data["extensions"].pop(i)
                else:
                    for i in cmd["args"][1:]:
                        if i not in data["extensions"]:
                            print(f"""ERROR: Extension '{i}' not found!""")
                            continue
                        try:
                            with open(extensions[i]["file"], "r") as f:
                                data["extensions"][i]["code"] = f.read()
                                data["extensions"][i]["version"] = f.readline().strip().split("/")[3]
                                data["extensions"][i]["author"] = f.readline().strip().split("/")[2]
                                data["extensions"][i]["file"] = f.readline().strip().split("/")[1]
                        except FileNotFoundError:
                            data["extensions"].pop(i)
                print("Extensions reloaded!")
            elif cmd["args"][0] == "list":
                print("Extensions list:")
                for i in data["extensions"]:
                    print(
                        f"    {data['extensions'][i]['name']} Version {data['extensions'][i]['version']} | Author: {data['extensions'][i]['author']} | Installed from: {data['extensions'][i]['file']}"
                    )
            elif cmd["args"][0] == "run":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if cmd["args"][1] not in data["extensions"]:
                    print(f"""ERROR: Extension '{cmd["args"][1]}' not found!""")
                    continue
                try:
                    print(f"Loading extension {cmd['args'][1]}...")
                    print(f"\n\n{data['extensions'][cmd['args'][1]]['name']} Version {data['extensions'][cmd['args'][1]]['version']} (Author: {data['extensions'][cmd['args'][1]]['author']})")
                    try:
                        exec(data["extensions"][cmd["args"][1]]["code"], {"__name__": "__main__", "extargs": {"args": cmd["args"], "flags": cmd["flags"], "longflags": cmd["longflags"]}})
                    except KeyboardInterrupt:
                        print(f"\nExited extension {cmd['args'][1]}.")
                    except Exception as e:
                        print(f"\nAn error occured while running extension '{cmd['args'][1]}'\nERROR: {e}")
                except Exception as e:
                    print(f"""ERROR: Failed to run extension '{cmd["args"][1]}': {e}""")
            elif cmd["args"][0] == "install":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if not os.path.isfile(cmd["args"][1]):
                    print(f"ERROR: {cmd['args'][1]} file doesn't exist!")
                    continue
                elif not cmd["args"][1].endswith(".py"):
                    print(f"ERROR: {cmd['args'][1]} is not a compatible extension file!")
                print(f"Installing extension {cmd['args'][1]}...")
                with open(cmd["args"][1], "r") as f:
                    firstline = f.readline().strip()
                    content = f.read()
                    if firstline.startswith("# PachTool Extension") and len(firstline.split('/')) == 6:
                        print("Loading extension code...")
                        data["extensions"][firstline.split("/")[1].lower().replace(" ", "_")] = {
                            "file": cmd["args"][1],       
                            "name": firstline.split("/")[4],
                            "author": firstline.split("/")[2],
                            "version": firstline.split("/")[3],
                            "code": content
                        }
                        print(f"\n\nINSTALLED: {firstline.split('/')[4]} Version {firstline.split('/')[3]}\nAuthor: {firstline.split('/')[2]}\n\nCan be executed using 'ext run {firstline.split('/')[1]}'")
                    else:
                         print(f"ERROR: {cmd['args'][1]} is not a compatible extension file!")
            elif cmd["args"][0] == "uninstall":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if cmd["args"][1] not in data["extensions"]:
                    print(f"""ERROR: Extension '{cmd["args"][1]}' not found!""")
                    continue
                print(f"Uninstalling extension {cmd['args'][1]}...")
                data["extensions"].pop(cmd["args"][1])
                print(f"Extension {cmd['args'][1]} uninstalled!")
            elif cmd["args"][0] == "rename":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if cmd["args"][1] not in data["extensions"]:
                    print(f"""ERROR: Extension '{cmd["args"][1]}' not found!""")
                    continue
                if len(cmd["args"]) == 2:
                    print("Missing argument <newname>: See 'extensions help' to see arg list")
                    continue
                print(f"Renaming extension {cmd['args'][1]} to {cmd['args'][2]}...")
                data["extensions"][cmd["args"][2]] = data["extensions"].pop(cmd["args"][1])
                print(f"Extension {cmd['args'][1]} renamed to {cmd['args'][2]}!")
            elif cmd["args"][0] == "info":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if cmd["args"][1] not in data["extensions"]:
                    print(f"""ERROR: Extension '{cmd["args"][1]}' not found!""")
                    continue
                print(f"\n\n{data['extensions'][cmd['args'][1]]['name']} Version {data['extensions'][cmd['args'][1]]['version']}\nAuthor: {data['extensions'][cmd['args'][1]]['author']}\nInstalled from: {data['extensions'][cmd['args'][1]]['file']}")
            elif cmd["args"][0] == "addtopath":
                if len(cmd["args"]) == 1:
                    print("Missing argument <extension>: See 'extensions help' to see arg list")
                    continue
                if cmd["args"][1] not in data["extensions"]:
                    print(f"""ERROR: Extension '{cmd["args"][1]}' not found!""")
                    continue
                print(f"Adding extension {cmd['args'][1]} to path...")
                data["extpath"].append(cmd["args"][1])
                print(f"Extension {cmd['args'][1]} added to path!\nCan be executed by using just '{cmd['args'][1]}'")
            else:
                giveerror("arg_unknown", "cmd", "ext")
        elif cmd["cmd"] == "data":
            if len(cmd["args"]) == 0:
                giveerror("arg_missing", "", "data")
            elif cmd["args"][0] == "help":
                print("\nData Available Args:")
                print("    help   | Show this help")
                print("    save   | Save data to shelltool_data.json")
                print("    update | Add new data keys")
                print("    reset  | Reset data to default")
            elif cmd["args"][0] == "reset":
                print("Resetting data...")
                data = pdata
                savedata(confirmation=False, sdata=data, hide=True, force=True)
            elif cmd["args"][0] == "update":
                print("Updating data...")
                for i in pdata:
                    if i not in data:
                        data[i] = pdata[i]
                savedata(confirmation=False, sdata=data, hide=True, force=True)
            elif cmd["args"][0] == "save":
                savedata(confirmation=False, sdata=data, hide=True, force=True)
        elif cmd["cmd"] in data["extpath"]:
            if data["debugmode"]:
                exec(data["extensions"][cmd["cmd"]]["code"], {"__name__": "__main__", "extargs": {"args": cmd["args"], "flags": cmd["flags"], "longflags": cmd["longflags"]}})
            else:
                try:
                    exec(data["extensions"][cmd["cmd"]]["code"], {"__name__": "__main__", "extargs": {"args": cmd["args"], "flags": cmd["flags"], "longflags": cmd["longflags"]}})
                except KeyboardInterrupt:
                    print(f"\nExited extension {cmd['cmd']}.")
                except Exception as e:
                    print(f"\nAn error occured while running extension '{cmd['cmd']}'\nERROR: {e}")
        else:
            if not unknown_show:
                print("Unknown command!")
            else:
                print("Unknown command! Use 'help' to see all commands.")
            unknown_show, unknown_used = True, True

if __name__ == "__main__":
    import sys
    if not pdata["debugmode"] or "--debug" in sys.argv:
        try:
            main()
        except KeyboardInterrupt:
            print()
            savedata(confirmation=True, sdata=pdata if "data" not in globals() else data, hide=False, force=True)
            exit(0)
        except Exception as e:
            print(f"An unkown error occured!\nERROR: {e}")
    else:
        main()
