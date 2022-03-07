import os


print(os.path.abspath(__file__))
dir = os.path.abspath(os.curdir)
dir = os.path.split(__file__)
path = dir[0]
print(dir)
print(path)
os.remove(path + '/vacancy.txt')
