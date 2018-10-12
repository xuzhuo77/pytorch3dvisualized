# -*- coding: utf-8 -*-
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
class camera:
    origin = [0.0,-1.0,0.0]
    length = 1.
    yangle = 0.
    zangle = 0.
    __bthree = False
    def __init__(this):
        this.mouselocation = [0.0,0.0]
        this.offest = 0.5
        this.zangle = 0. if not this.__bthree else math.pi
    def setthree(this,value):
        this.__bthree = value
        this.zangle = this.zangle + math.pi
        this.yangle = -this.yangle          
    def eye(this):
        return this.origin if not this.__bthree else this.direction()
    def target(this):
        return this.origin if this.__bthree else this.direction()
    def direction(this):
        if this.zangle > math.pi * 2.0 :
            this.zangle < - this.zangle - math.pi * 2.0
        elif this.zangle < 0. :
            this.zangle < - this.zangle + math.pi * 2.0
        len = 1. if not this.__bthree else this.length if 0. else 1.
        xy = math.cos(this.yangle) * len
        x = this.origin[0] + xy * math.sin(this.zangle)
        y = this.origin[1] + len * math.sin(this.yangle)
        z = this.origin[2] + xy * math.cos(this.zangle)        
        return [x,y,z]
    def move(this,x,y,z):
        sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)        
        xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
        if this.__bthree : 
            xstep = -xstep
            zstep = -zstep
        this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]  
        
    def rotate(this,z,y):
        this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
    def setLookat(this):
        ve,vt = this.eye(),this.target()
        #print ve,vt
        glLoadIdentity()
        gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)        
    def keypress(this,key,x,y):

        
        if key in (b'e', b'E'):
            this.move(0.,0.,1 * this.offest)
        if key in (b'a', b'F'):
            this.move(1 * this.offest,0.,0.)
        if key in (b'd', b'S'):
            this.move(-1 * this.offest,0.,0.)
        if key in (b'q', b'D'):
            this.move(0.,0.,-1 * this.offest)
        if key in (b'w', b'W'):
            this.move(0.,1 * this.offest,0.)
        if key in (b's', b'R'):
            this.move(0.,-1 * this.offest,0.)
        if key in (b'v', b'V'):
            #this.__bthree = not this.__bthree
            this.setthree(not this.__bthree)
        if key == GLUT_KEY_UP:
            this.offest = this.offest + 0.1
        if key == GLUT_KEY_DOWN:
            this.offest = this.offest - 0.1

            
        
    def zmove(this,button):
        if button==3:
            this.move(0.,0.,1 * this.offest)
        elif button==4:
            this.move(0.,0.,-1 * this.offest)
    def mouse(this,x,y):  
        rx = (x - this.mouselocation[0]) * this.offest * 0.01
        ry = (y - this.mouselocation[1]) * this.offest * -0.01
        this.rotate(rx,ry)
        
        this.mouselocation = [x,y]

