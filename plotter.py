import math
import numpy as np
import sympy as sym
from sympy.abc import x

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import collections  as mc
from collections import deque
plt.style.use('seaborn-pastel')

#####################################################
##           Plotter and Animation Class           ##
#####################################################

class Plotter:
    def __init__(self, r1, r2, r3, r4, fsn_results,
                 theta2_start, theta2_max_rot, 
                 theta4_start, theta4_max_rot,
                 theta2_angular_speed=1,
                 time_increment=0.05,
                 ) -> None:
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.t1 = 0
        self.t2_i = theta2_start
        self.t2_f = theta2_start + theta2_max_rot
        self.t4_i = theta4_start
        self.t4_f = theta4_start + theta4_max_rot
        self.w2   = theta2_angular_speed
        self.time_inc = time_increment
        self.K = fsn_results
        self.points = []
        
        pass
    
    def generate_points(self) -> None:
        r1, r2, r3, r4 = self.r1, self.r2, self.r3, self.r4
        
        t2_current = self.t2_i
        t4_current = None
        
        while t2_current <= self.t2_f:
            #print("current angle is ", math.degrees(t2_current))
            
            Ax = 0
            Ay = 0
            Dx = r1
            Dy = 0
            Bx = r2 * math.cos(t2_current)
            By = r2 * math.sin(t2_current)
            
            AD = math.sqrt(r1**2 + r2**2 - 2*r1*r2*math.cos(t2_current))        # using cosine rule
            angle1 = math.acos((r1**2 + AD**2 - r2**2) / (2*r1*AD))     # using cosine rule
            if (By < 0):
                angle1 = -angle1
            angle2 = math.acos((r4**2 + AD**2 - r3**2) / (2*r4*AD))     # using cosine rule
            t4_current = 2*math.pi - (angle1 + angle2)
            
            # Use Freudensteins:
            # eq = sym.Eq(self.K[0]*math.cos(t2_current) + self.K[1]*sym.cos(x) + self.K[2], sym.cos(t2_current - x))
            # t4_current = max(sym.solve(eq, x))
            # print("solved one")
            
            # g = math.acos((r3**2+r4**2-r1**2-r2**2+2*r1*r2*math.cos(t2_current)) / (2*r3*r4))
            # t4_current = 2*math.atan((r2*math.sin(t2_current)+r3*math.sin(g)) / (r4-r1+r2*math.cos(t2_current)-r3*math.cos(g)))
            
            Cx = Dx - r4 * math.cos(t4_current)
            Cy = -r4 * math.sin(t4_current)
            
            result = [Ax, Ay, Bx, By, Cx, Cy, Dx, Dy]
            self.points.append(result)
            
            t2_current += self.w2 * self.time_inc
        pass
    
    def animate_linkage(self):
        fig = plt.figure()
        ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))
        ax.set_aspect('equal')
        ax.grid(visible=True, color='grey', linestyle='-', linewidth=1)
        
        line, = ax.plot([], [], 'o-', lw=2)
        trace, = ax.plot([], [], '.-', lw=1, ms=2)
        history_x, history_y = deque(maxlen=len(self.points)), deque(maxlen=len(self.points))
        #c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        
        def init():
            line.set_data([], [])
            return line,
            
        def animate(i):
            thisx = [self.points[i][0], self.points[i][2], self.points[i][4], self.points[i][6], self.points[i][0]]
            thisy = [self.points[i][1], self.points[i][3], self.points[i][5], self.points[i][7], self.points[i][1]]
            
            if i == 0:
                history_x.clear()
                history_y.clear()
                
            history_x.appendleft((thisx[2] + thisx[1]) / 2)
            history_y.appendleft((thisy[2] + thisy[1]) / 2)
            
            line.set_data(thisx, thisy)
            trace.set_data(history_x, history_y)
            return line, trace,
        
        anim = FuncAnimation(fig, animate, frames=len(self.points), init_func=init, interval=1, blit=True)
        anim.save("plot.gif", writer='Pillow')
        
        
    
if __name__ == "__main__":
    # fig = plt.figure()
    # ax = fig.add_subplot(autoscale_on=False, xlim=(0, 4), ylim=(-2, 2))
    # ax.set_aspect('equal')
    # ax.grid(visible=True, color='r', linestyle='-', linewidth=2)
    
    # line, = ax.plot([], [], lw=3)
    # plt.gca().set_aspect("equal")

    # def init():
    #     line.set_data([], [])
    #     return line,
    # def animate(i):
    #     x = np.linspace(0, 4, 1000)
    #     y = np.sin(2 * np.pi * (x - 0.01 * i))
    #     line.set_data(x, y)
    #     return line,

    # anim = FuncAnimation(fig, animate, init_func=init,
    #                             frames=200, interval=20, blit=True)


    # anim.save('sine_wave.gif', writer='PillowWriter')
    pass