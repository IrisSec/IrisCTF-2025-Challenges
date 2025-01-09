# flag stored at 'flag' in current dir

import builtins

all_builtins = dir(builtins)
filtered_builtins = {name: getattr(builtins, name) for name in all_builtins if len(name) <= 4}
filtered_builtins.update({'print': print})

whitelist = "<ph[(cobras.den)]+~"
security_check = lambda s: any(c not in whitelist for c in s) or len(s) > 1115 or s.count('.') > 1

print('Good luck!')
while True:
    cmd = input("Input: ")
    if security_check(cmd):
        print("No dice!")
    else:
        try:
            eval(f"print({cmd})", {"__builtins__": filtered_builtins})
        except SyntaxError as e:
            print(f"Syntax error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")