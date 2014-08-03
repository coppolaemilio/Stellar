import os, sys, subprocess
eelbox = subprocess.Popen(["eel.exe", "main.eel"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out = eelbox.stdout.read()
print out