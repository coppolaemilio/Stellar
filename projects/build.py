import json
import os, sys, subprocess

json_data=open('example.project.json')
data = json.load(json_data)
debug = True
indent = "    "

def Imports():
    imports = []
    for i in data["imports"]:
        imports.append( i + ' ' + data["imports"][i])
    imports.append("from odin import *")
    return imports

def Scripts():
    scripts = ["\n#Scripts ------------------------------"]
    for s in data["scripts"]:
        scripts.append("def " + s + "(argument0=None, arugment1=None, argument2=None):")

        with open(os.path.join("scripts", data["scripts"][s])) as f:
            content = f.read()
            current_data = indent + str(content)
            current_data = current_data.replace("\n", "\n"+ indent)

            scripts.append(current_data)

        scripts.append("")
    return scripts

def Sprites():
    sprites = ["\n#Sprites -------------------------------"]
    for s in data["sprites"]:
        sprites.append( s + " = create_sprite(\"" + data["sprites"][s] + "\")")

    return sprites

def Objects():
    objects = ["\n#Objects ------------------------------"]
    for o in data["objects"]:
        objects.append("class " + o + "(Object):")

        obj_json_data=open(os.path.join("objects", data["objects"][o]))
        obj_data = json.load(obj_json_data)
        for p in obj_data["properties"]:
            objects.append(indent + p + " = " + str(obj_data["properties"][p]))
        for e in obj_data["events"]:
            current_data = indent*2 + str(obj_data["events"][e])
            current_data = current_data.replace("\n", "\n"+ indent*2)
            if e == "create":
                objects.append(indent + "def event_create(self):")
                objects.append(current_data)
            if e == "step":
                objects.append(indent + "def event_step(self):")
                objects.append(current_data)
            if e == "draw":
                objects.append(indent + "def event_draw(self):")
                objects.append(current_data)

        objects.append("")
        obj_json_data.close()

    return objects

def Rooms():
    rooms = ["\n#Rooms --------------------------------"]
    for r in data["rooms"]:
        rooms.append("class " + r + "(Room):")

        room_json_data=open(os.path.join("rooms", data["rooms"][r]))
        room_data = json.load(room_json_data)
        for p in room_data["properties"]:
            rooms.append(indent + p + " = " + str(room_data["properties"][p]))
        for e in room_data["events"]:
            current_data = indent*2 + str(room_data["events"][e])
            current_data = current_data.replace("\n", "\n"+ indent*2)
            if e == "create":
                rooms.append(indent + "def create_event(self):")
                rooms.append(current_data)
            if e == "step":
                rooms.append(indent + "def event_step(self):")
                rooms.append(current_data)
            if e == "draw":
                rooms.append(indent + "def draw_event(self):")
                rooms.append(current_data)

        rooms.append("")
        room_json_data.close()


    return rooms

def GameLoop():
    return ["\n#Game Start ---------------------------\nstart_game(room_1)"]

json_data.close()

with open('main.py', 'w') as file:
    text = "#This file was generated with Stellar\n"

    parts = [Imports(), Scripts(), Sprites(), Objects(), Rooms(), GameLoop()]
    for part in parts:
        for line in part:
            text+= line + "\n"

    file.write(text)

if debug == True:
    if sys.platform=="win32":
        game = subprocess.Popen(["python", "main.py"], shell=True, 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
        out = game.stdout.read()
        print out
    else:
        os.system("python main.py")
    