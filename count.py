import os

for file in os.listdir():
    try:
        with open(file):
            pass
    except:
        continue
    print(file[:-3])
    module = __import__("" + file[:-3])
