import glob
files=glob.glob(".\*.py")
print(files)
print(files[-1])
print(files[-1].replace(".\\","").replace(".py",""))