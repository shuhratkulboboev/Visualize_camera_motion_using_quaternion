"""
PyTeapot module for drawing rotating cube using OpenGL as per
quaternion or yaw, pitch, roll angles received over serial port.
"""
import pandas as pd
import OpenGL
import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import time
useSerial = True # set true for using serial for data transmission, false for wifi
useQuat = True  # set true for using quaternions, false for using y,p,r angles
global_step = 0


df=pd.read_csv("C:/Users/User/OneDrive/Desktop/english courses/trajectory/PyTeapot-Quaternion-Euler-cube-rotation-master/Orientation.csv")
df=df.iloc[:,[1,2,3,4,5]]
Z=df.iloc[:,1]
Y=df.iloc[:,2]
X=df.iloc[:,3]
W=df.iloc[:,4]
t=df.iloc[:,0]

results=[]

for i in range(len(Z)):
    result = "w"+str(W[i])+'wa'+str(X[i])+"ab"+str(Y[i])+"bc"+str(Z[i])+"c"+"\n"
    results.append(result)

end = len(results)
print(end)
start_time = time.time()
def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    pygame.time.wait(5000)
    pygame.time.delay(5000)
    screen = pygame.display.set_mode((1280, 960), video_flags)
    pygame.display.set_caption("PyTeapot IMU orientation visualization")
    resizewin(1280, 960)
    init()
    frames = 0
    #ticks = pygame.time.get_ticks()
    lock = pygame.time.Clock()
    FPS =100
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        if(useQuat):
            [w, nx, ny, nz] = read_data()
        else:
            [yaw, pitch, roll] = read_data()
        if(useQuat):
            draw(w, nx, ny, nz)
        else:
            draw(1, yaw, pitch, roll)
        pygame.display.flip()
        lock.tick(FPS)
        frames += 1
    print("fps: %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    if(useSerial):
        result.close()


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def cleanSerialBegin():
    if(useQuat):
        try:
            line = result.readline().decode('UTF-8').replace('\n', '')
            w = float(line.split('w')[1])
            nx = float(line.split('a')[1])
            ny = float(line.split('b')[1])
            nz = float(line.split('c')[1])
        except Exception:
            pass
    else:
        try:
            line = result.readline().decode('UTF-8').replace('\n', '')
            yaw = float(line.split('y')[1])
            pitch = float(line.split('p')[1])
            roll = float(line.split('r')[1])
        except Exception:
            pass

def read_data():
    global global_step
    global start_time
    if end == global_step :
        print(time.time()-start_time)
        print((time.time()-start_time)/len(results))
        quit()
    if(useSerial):
        
        line = results[global_step]
        # print(line)
        global_step += 1
    else:
        # Waiting for data from udp port 5005
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        line = data.decode('UTF-8').replace('\n', '')
        # print(line)
                
    if(useQuat):
        w = float(line.split('w')[1])
        nx = float(line.split('a')[1])
        ny = float(line.split('b')[1])
        nz = float(line.split('c')[1])
        return [w, nx, ny, nz]
    else:
        yaw = float(line.split('y')[1])
        pitch = float(line.split('p')[1])
        roll = float(line.split('r')[1])
        return [yaw, pitch, roll]


def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    
    drawText((-2.6, 1.6, 2), "Module to visualize quaternion or Euler angles data", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    if(useQuat):
        [yaw, pitch , roll] = quat_to_ypr([w, nx, ny, nz])
        drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
        glRotatef(2 * math.acos(w) * 180.00/math.pi, -1*nx, nz, ny)
    else:
        yaw = nx
        pitch = ny
        roll = nz
        drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
        glRotatef(roll, 0.00, 0.00, 1.00)
        glRotatef(pitch, 1.00, 0.00, 0.00)
        glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
 
    glColor3f(0.0,1.0,0.0)
    glVertex3f( 0.3, 0.3,-0.3)
    glVertex3f(-0.3, 0.3,-0.3)  ##blue
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f( 0.3, 0.3, 0.3) 
 
    glColor3f(1.0,0.0,0.0)
    glVertex3f( 0.3,-0.3, 0.3)
    glVertex3f(-0.3,-0.3, 0.3)
    glVertex3f(-0.3,-0.3,-0.3)
    glVertex3f( 0.3,-0.3,-0.3) 
 
    glColor3f(1.0,1.0,0.0)
    glVertex3f( 0.3, 0.3, 0.3)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(-0.3,-0.3, 0.3)
    glVertex3f( 0.3,-0.3, 0.3)
 
    glColor3f(1.0,1.0,0.0)
    glVertex3f( 0.3,-0.3,-0.3)
    glVertex3f(-0.3,-0.3,-0.3)
    glVertex3f(-0.3, 0.3,-0.3)
    glVertex3f( 0.3, 0.3,-0.3)
 
    glColor3f(0.0,0.0,1.0)
    glVertex3f(-0.3, 0.3, 0.3) 
    glVertex3f(-0.3, 0.3,-0.3)
    glVertex3f(-0.3,-0.3,-0.3) 
    glVertex3f(-0.3,-0.3, 0.3) 
 
    glColor3f(1.0,0.0,0.0)
    glVertex3f( 0.3, 0.3,-0.3) 
    glVertex3f( 0.3, 0.3, 0.3)
    glVertex3f( 0.3,-0.3, 0.3)
    glVertex3f( 0.3,-0.3,-0.3)

    glEnd()
    
    glBegin(GL_LINES)

    glColor3f (1.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(-2.0, 0.0, 0.0)
        
    glColor3f (0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, -2.0, 0.0)
       
    glColor3f (1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, -2.0)
    glEnd()

def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def quat_to_ypr(q):
    yaw   = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.asin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll  = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw   *= 180.0 / math.pi
    yaw   -= -0.13  # Declination at Chandrapur, Maharashtra is - 0 degress 13 min
    roll  *= 180.0 / math.pi
    return [yaw, pitch, roll]


if __name__ == '__main__':
    main()
