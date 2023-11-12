#!/Users/jim/anaconda3/envs/sb/bin/python

from datetime import datetime as dt

def main():
    text = "This is a test"
    with open("test.txt","a") as f:
        f.write(f'the time is: {dt.now()}')
    f.close()
    