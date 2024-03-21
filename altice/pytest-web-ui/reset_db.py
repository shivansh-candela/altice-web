from asyncio import subprocess
from subprocess import run, PIPE, Popen
import asyncio
import sys
import os

for f in os.listdir("pytest_web_ui/__pycache__"):
    if f != "__init__.py" and f != "__pycache__":
        os.remove(os.path.join("pytest_web_ui/__pycache__", f))


for f in os.listdir("resources/migrations/__pycache__"):
    if f != "__init__.py" and f != "__pycache__":
        os.remove(os.path.join("resources/migrations/__pycache__", f))

for f in os.listdir("resources/__pycache__"):
    if f != "__init__.py" and f != "__pycache__":
        os.remove(os.path.join("resources/__pycache__", f))

for f in os.listdir("resources/migrations"):
    if f != "__init__.py" and f != "__pycache__":
        os.remove(os.path.join("resources/migrations", f))

pipe1 = Popen("rm db.sqlite3",shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
(out,err) = pipe1.communicate()




