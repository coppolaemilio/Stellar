#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
#
# This file is part of Stellar.
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar. If not, see <http://www.gnu.org/licenses/>.


#"""
#Known bugs:
#    - if an event only contains coments the game will not run.
#"""

import os
import shutil
import platform
import subprocess
import ConfigParser

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
                    config = ConfigParser.RawConfigParser()
                    config.read(full_file_name)
                    sprite = config.get('data', 'sprite')
                    
                    sgeobjects.append(["\nclass "+file_name[:-4]+"(sge.StellarClass):"])
                    sgeobjects.append(["    def __init__(self, x, y, player=0):"])
                    sgeobjects.append(["        super("+file_name[:-4]+", self).__init__(x, y, 5, sprite='"+sprite+"', collision_precise=True)"])

                    if config.has_section("EventCreate") and len(config.options("EventCreate"))!= 0:
                        sgeobjects.append(["    def event_create(self):"])
                        self.addactions("EventCreate", config, sgeobjects)
                        
                    if config.has_section("EventStep") and len(config.options("EventStep"))!= 0:
                        sgeobjects.append(["    def event_step(self, time_passed):"])
                        self.addactions("EventStep", config, sgeobjects)
                    
        if len(os.listdir(os.path.join(self.dirname,"Rooms"))) > 0:
            src=os.path.join(self.dirname,"Rooms")
            src_files = os.listdir(src)
            for file_name in src_files:
                full_file_name = os.path.join(src, file_name)
                if (os.path.isfile(full_file_name)):
                    roominfo = open(full_file_name, "r")
                    roominfolines = roominfo.read()
                    roominfolines = roominfolines.replace("\r","")
                    sgerooms.append(roominfolines)

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

    def addactions(self, event, configuration, sgeobjects):
        config = configuration
        for option in config.options(event):
            command = config.get(event, option)
            if "comment" in option:
                sgeobjects.append(['        #'+command])
            elif "variable" in option:
                sgeobjects.append(['        '+command])
            elif "runscript" in option:
                print "aca"
                if (os.path.isfile(os.path.join(self.dirname,"Scripts",command+".py"))):
                    scriptinfo = open(os.path.join(self.dirname,"Scripts",command+".py"), "r")
                    scriptinfolines = scriptinfo.read()
                    scriptinfolines = scriptinfolines.replace("\n","\n        ")
                    scriptinfolines = scriptinfolines.replace("\r","")
                    sgeobjects.append(["        "+scriptinfolines])
                    scriptinfo.close()
