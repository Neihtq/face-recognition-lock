import pyautogui
from sys import platform

print(platform)
if platform == "linux" or platform == "linux2":
    print("linux")
    pass
elif platform == "win32":
    print("windows")
    import ctypes
    ctypes.windll.user32.LockWorkStation()
else:
    print("mac")
    pass

