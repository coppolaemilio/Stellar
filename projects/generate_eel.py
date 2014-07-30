import json
import os, sys, subprocess

json_data=open('example.project.json')
data = json.load(json_data)
debug = True
o = []

def Imports():
    imports = []
    for i in data["import"]:
        if data["import"][i]:
            imports.append('import "' + i + '" as ' + data["import"][i] + ';') 
        else:
            imports.append('import "' + i + '";')
    imports.append("")
    return imports

def Sprites():
    sprites = ["//Sprites -------------------------------"]
    for s in data["sprites"]:
        sprites.append('static ' + s + ' = add_sprite("' + data["sprites"][s] + '");')

    return sprites

def Objects():
    objects = ["//Objects -------------------------------"]
    objects.append("local objects = [];")
    index = 0
    for o in data["objects"]:
        objects.append("local " + o + " = table[")
        for event in data["objects"][o]:
            objects.append("procedure " + event + "(self){")
            objects.append(data["objects"][o][event] + "\n}")
        objects.append("] ;")

        objects.append("insert(objects, " + str(index) + ", " + o + ");")
        index+=1

    return objects

def Screen():
    screen = ["//Screen --------------------------------"]
    screen.append("local screen = SetVideoMode(" + str(data["window"]["width"]) + ", " + str(data["window"]["height"]) + ", 0, SWSURFACE);")
    screen.append("SetCaption(\"" + data["window"]["caption"] + "\", args[0]);")

    return screen

o.append(Imports())
o.append("export function main<args>{")
o.append(Screen())
o.append(Sprites())
o.append(Objects())


#LOOP
o.append("""    
    for local i = 0, sizeof objects - 1 {
            objects[i]:create_event();
        }
    while true
    mainloop:{
        while true{
            FillRect(nil, nil, MapColor(screen, 40,40,90));
            for local i = 0, sizeof objects - 1 {
                objects[i]:step_event();
                objects[i]:draw_event();
            }
            Flip();

            local ev = PollEvent();
            if not ev
                break;
            switch ev.type
              case KEYUP
                if ev.sym == KESCAPE
                    break mainloop;
              case QUIT
                break mainloop;
        }
    }
    return 0;
}""")

json_data.close()


indent = 0
def Indent(line):
    global indent
    line = ("\t" * indent)+line
    if line.endswith("{") or line.endswith("["):
        indent += 1
    elif line.endswith("}") or line.endswith("] ;"):
        indent -= 1
    return line

with open('main.eel', 'w') as file:
    text = "//This file was generated with Stellar\n"
    for line in o:
        if isinstance(line, list):
            for subline in line:
                text += Indent(subline) + "\n"
        else:
            text += Indent(line) + "\n"

    file.write(text)

if debug == True:
    eelbox = subprocess.Popen(["eel.exe", "main.eel"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = eelbox.stdout.read()
    print out