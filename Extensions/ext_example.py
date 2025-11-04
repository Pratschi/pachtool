# PachTool Extension /exttest/Pratschi/1.0.0/Extension Test Example/
# ^^^^^^^^^^^^^^^^^^ ^^^^^^^^ ^^^^^^^^ ^^^^^ ^^^^^^^^^^^^^^^^^^^^^^
#    Required for     Command  Author  Version       Name
#     Detection

"""
How does it work?
Pachtool detects if a python file is an extension by checking the first line.
It HAS to start with '# PachTool Extension' exactly.
Then, it requires the data between slashes, indicating all the information.
If a slash is missing, the extension will not load. (Even the last one)
"""

print("The Test Extension has been used!")

"""
The extension is pre-loaded with a variable called 'extargs'.
It contains all the arguments it was runned with.
extargs['args'] > Contains a list with the args (arg)
extargs['flags'] > Contains a list with the flags (-flag)
extargs['longflags'] > Contains a dict with the longflags (--longflag) and its value (--longflag=value)
    > NOTE: If a longflag wasn't assigned a value (--longflag), it defaults to 0 (integer)
"""

print(f"The Extension has been executed with this args in a list:\n{extargs['args']}\n")
print(f"And with this flags in another list:\n{extargs['flags']}\n")
print(f"And with this longflags in a dict:\n{extargs['longflags']}")
