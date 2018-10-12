from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import  time
import sys
from mCamera import *
from netreader import outputsummary
from matplabimage import makeimage,colormap
RADIUS=1
cube_distance=2
normal_size=0.01
foce_size=0.02
foced_id=8
class Cube:
    def __init__(self,x,y,z,d,w,h,data):
        self.x=x
        self.y=y
        self.z=z
        self.d=d
        self.w=w
        self.h=h
        self.color=color
        self.beForceed=False      
        

def makeTreeData(summary):
    for layer in summary:
        #print(summary[i]["input_shape"])
        #(layer,summary[layer]['output_shape'],summary[layer]['nb_params'],)
        """
        if 'weight_shape' in summary[layer]:
            print(layer,summary[layer]['weight_shape'],summary[layer]['output_shape'])
            yield [3,summary[layer]['weight_shape'][-2],summary[layer]['weight_shape'][-1]]
        else:
            yield [3,3,3]
            #print(layer,False,summary[layer]['output_shape'])
        """
        o_size=summary[layer]['output_shape']
        if len(o_size)==4:
            yield o_size[-3:]
        else :
            yield [2,o_size[-1]/10,o_size[-1]/10]



class CubeData():
    def __init__(self,layer,weight_shape,output_shape,trainable,nb_params):
        self.layer=layer
        self.weight_shape=weight_shape
        self.output_shape=output_shape
        self.trainable=trainable
        self.nb_params=nb_params
        
def make_CubeData(summary):
    for layer in summary:
        #print(summary[i]["input_shape"])
        #(layer,summary[layer]['output_shape'],summary[layer]['nb_params'],)
        d=CubeData.__new__(CubeData)
        setattr(d,'layer',layer)
        for key,value in summary[layer].items():
            if key !='output':
                print('--',layer,key,value)
                
                setattr(d,key,value)
        yield d

def make_String(cubedatas,foced_id):
    fc=cubedatas[foced_id]
    line_new = "layer:{}   weight_shape:{}   output_shape:{}".format(
            fc.layer,
            None if not hasattr(fc,'weight_shape') else fc.weight_shape,
            str(fc.output_shape),
    )
    return line_new
    

        
    
def net_tree2(cubelist):
    d=0
    glEnable(GL_NORMALIZE);
    
    for i ,shape in enumerate(cubelist):
        x,y,z=shape
        color=color_Dict['foced'] if foced_id==i else color_Dict['normal'] 
        size=foce_size if foced_id==i else normal_size
        glPushMatrix();
        drawCube(i,
                 d,
                 0,0,
                 x,
                 y,
                 z,
                 size,
                 color
                 
                 )
        
        glPopMatrix();
        d+=x*0.01
        d+=1
        
        


outputSummary=outputsummary()
op_cube=list(makeTreeData(outputSummary))
cubedatas=list(make_CubeData(outputSummary))



#array=outputSummary['Conv2d-6']['output'].cpu().detach().numpy()[0][0]
#w,h=array.shape[-2:]

#makeimage(array)
#colormap=colormap(array)
color_Dict={'foced':(100.0, 0.0, 0.0),
            'normal':(0.0, 100.0, 0.0)}
class Foced:
    def __init__(self):
        self.curr_id=0
    def setNext(self,key):
        if key==1:
            self.curr_id+=1
        elif key==2:
            self.curr_id-=1
    def showDetal(self):
        pass
    
def setCharactersPos(x,y,string):
    
    glRasterPos2f(x, y)
    for c in string:
            # 输出文字
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
    

def drawCube(i,x,y,z,d,w,h,size,color):
    
    glColor3f(*color)
    glTranslatef(x,y,z);
    glScalef(d*size,w*size,h*size);
    
    glutWireCube(RADIUS);
    drawCharacter(str(i))
    
def drawCharacter(string):
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2f(1.0, 0.0)
    for c in string:
            # 输出文字
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))


def Draw():
    drawCube()
def Update():
    pass


window = 0

def drawPixels(w,h,pixeldata):
   glRasterPos2i(0, 0);
   glPixelZoom (2, 2);
   glDrawPixels(w, h,GL_BGR, GL_UNSIGNED_BYTE, pixeldata);


camera = camera()
#plane = common.plane(12,12,1.,1.)
def InitGL(width,height):
    glClearColor(0.1,0.1,0.5,0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0,float(width)/float(height),0.1,100.0)    
    camera.move(0.0,3.0,-5)    
    
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)     
    camera.setLookat()
    #plane.draw() 
    
    #drawPixels(w,h,array)
    
    glBegin(GL_LINES);		
    glVertex3f(-9.0,0.0,0.0);		
    glVertex3f(100.0,0.0,0.0);		
    glEnd();


    

    x,y,z=camera.origin
    setCharactersPos(x,y,make_String(cubedatas,foced_id))
    #drawCube(0,0,0,256,52,52)
    net_tree2(op_cube)
        # 定位文字
    #net_tree(10,10)
    #glCallList("2")
    #sph.draw()                         
    glutSwapBuffers()

def mouseButton( button, mode, x, y ):
    if button==4 or 3:
        camera.zmove(button)
    if button == GLUT_RIGHT_BUTTON:
        camera.mouselocation = [x,y]

def ReSizeGLScene(Width, Height): 
    glViewport(0, 0, Width, Height)        
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
def keypress(key,x,y):

        global foced_id
        if key in (b'e', b'E'):
            camera.move(0.,0.,1 * camera.offest)
        if key in (b'a', b'F'):
            camera.move(1 * camera.offest,0.,0.)
        if key in (b'd', b'S'):
            camera.move(-1 * camera.offest,0.,0.)
        if key in (b'q', b'D'):
            camera.move(0.,0.,-1 * camera.offest)
        if key in (b'w', b'W'):
            camera.move(0.,1 * camera.offest,0.)
        if key in (b's', b'R'):
            camera.move(0.,-1 * camera.offest,0.)
        if key in (b'v', b'V'):
            #this.__bthree = not this.__bthree
            camera.setthree(not camera.__bthree)
        if key == GLUT_KEY_UP:
            camera.offest = camera.offest + 0.1
        if key == GLUT_KEY_DOWN:
            camera.offest = camera.offest - 0.1
        if key==b'1':
            foced_id+=1
        if key==b'2':
            foced_id-=1
def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1366,768)
    glutInitWindowPosition(800,400)
    window = glutCreateWindow("opengl")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutMouseFunc( mouseButton )
    glutMotionFunc(camera.mouse)
    glutKeyboardFunc(keypress)

    glutSpecialFunc(keypress)
    InitGL(640, 480)
    glutMainLoop()

main()

