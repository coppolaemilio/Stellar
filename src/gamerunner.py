import os
import shutil
import platform
import subprocess

from PyQt4 import QtGui, QtCore

class GameRunner(object):
    def __init__(self, dirname, fname):
        self.dirname = dirname
        self.fname = fname
        print self.dirname
        self.template_file = os.path.join(self.dirname, "..","Data","SGE", "gametemplate.py")
        self.obj_template_file = os.path.join(self.dirname,"..", "Data","SGE", "objecttemplate.py")


        self.createandrun()
        
    def createandrun(self):
        if not len(os.listdir(os.path.join(self.dirname,"Rooms"))) > 0:
            QtGui.QMessageBox.warning(self, "Error", "A game must have at least one room to run.",QtGui.QMessageBox.Ok)
            return
        #Writes the information needed on the main file
        sgesprites=[]
        sgeobjects=[]
        sgerooms=[]
        objectsprite=""
        if len(os.listdir(os.path.join(self.dirname,"Sprites"))) > 0:
            src=os.path.join(self.dirname,"Sprites")
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if (os.path.isfile(full_file_name)):
                    if not ('.ini' in full_file_name):
                        full_file_name = os.path.splitext(os.path.basename(full_file_name))
                        print (str(full_file_name[0]))
                        sgesprites.append(full_file_name[0])
        if len(os.listdir(os.path.join(self.dirname,"Backgrounds"))) > 0:
            src=os.path.join(self.dirname,"Backgrounds")
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if (os.path.isfile(full_file_name)):
                    if not ('.ini' in full_file_name):
                        full_file_name = os.path.splitext(os.path.basename(full_file_name))
                        print (str(full_file_name[0]))
                        sgesprites.append(full_file_name[0])
        if len(os.listdir(os.path.join(self.dirname,"Objects"))) > 0:
            src=os.path.join(self.dirname,"Objects")
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if (os.path.isfile(full_file_name)):
                    objinfo = open(full_file_name, "r")
                    objinfolines = objinfo.readlines()
                    for line in objinfolines:
                        if ('<Sprite>' in line):
                            line = line.replace("\n",">")
                            line = line.split(">")
                            objectsprite=line[1]
                            objinfolines = [w.replace('<Sprite>', "#") for w in objinfolines]
                        elif ('<init>' in line):
                            objectsprite.replace("\n", "")
                            finalline = "    def __init__(self, x, y, player=0):"+"\n        super("+file_name[:-3]+", self).__init__(x, y, 5, '"+objectsprite+"', collision_precise=True)\n        self.player = player"
                            objinfolines = [w.replace('<init>',finalline.replace("\r", "")) for w in objinfolines]
                        elif ('<Class>' in line):
                            objinfolines = [w.replace('<Class>', "class "+file_name[:-3]+"(sge.StellarClass):") for w in objinfolines]
                        #EVENTS##################################
                        elif ('<Events>' in line):
                            objinfolines = [w.replace('<Events>', "") for w in objinfolines]
                        elif ('<EventCreate>' in line):
                            objinfolines =[w.replace('<EventCreate>', "def event_create(self):") for w in objinfolines]
                        elif ('<EventStep>' in line):
                            objinfolines =[w.replace('<EventStep>', "def event_step(self, time_passed):") for w in objinfolines]
                        #ACTIONS##################################
                        elif ('<Actions>' in line ):
                            objinfolines = [w.replace('<Actions>', "") for w in objinfolines]
                        elif ('<AddActionScript>' in line ):
                            line = line.replace("\n","")
                            line = line.split(">")
                            if (os.path.isfile(os.path.join(self.dirname,"Scripts",line[1]+".py"))):
                                scriptinfo = open(os.path.join(self.dirname,"Scripts",line[1]+".py"), "r")
                                scriptinfolines = scriptinfo.read()
                                scriptinfolines = scriptinfolines.replace("\n","\n        ")
                                objinfolines = [w.replace('<AddActionScript>'+line[1], scriptinfolines) for w in objinfolines]
                            else:
                                QtGui.QMessageBox.warning(self, "Error on object "+file_name+" Action.", 'The script named "'+line[1]+'" does not exist.',QtGui.QMessageBox.Ok)
                                return
                        elif ('<AddActionComment>' in line):
                            objinfolines = [w.replace('<AddActionComment>', "#") for w in objinfolines]
                    
                    sgeobjects.append(objinfolines)
        if len(os.listdir(os.path.join(self.dirname,"Rooms"))) > 0:
            src=os.path.join(self.dirname,"Rooms")
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if (os.path.isfile(full_file_name)):
                    roominfo = open(full_file_name, "r")
                    roominfolines = roominfo.read()
                    #roominfolines = roominfolines.replace("\n","\n        ")
                    sgerooms.append(roominfolines)


        objinfo.close()
        roominfo.close()
        #Opens and read the template           
        template = open(self.template_file, "r")
        lines = template.readlines()
        template.close()

        #Add the information collected to the template
        f = open(os.path.join(self.dirname,self.fname), 'w')
        for line in lines:  
            if ('# Load sprites' in line ):
                f.write('# Load sprites\n')
                for sprite in sgesprites:
                    f.write(""+sprite+"_sprite = sge.Sprite('"+sprite+"', transparent=True)\n")
                
            elif('# Add Stellar objects' in line):
                for sobject in sgeobjects:
                    for dobject in sobject:
                        f.write("\n"+dobject)
            elif('# Rooms' in line):
                for sroom in sgerooms:
                    f.write("\n"+sroom)
                    
            else:
                f.write(line)
               
        f.close()

        tmpdir = os.getcwd()
        os.chdir(self.dirname)
        if platform.system() == 'Windows':
            subprocess.Popen(["C:\Python27\python.exe", self.fname]).communicate()
        else:
            os.system('python '+self.fname)
        os.chdir(tmpdir)
