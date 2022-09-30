import math

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#####################################################
##           Plotter and Animation Class           ##
#####################################################

class Plotter:
    def __init__(self, r1, r2, r3, r4,
                 theta2_start, theta2_max_rot, 
                 theta4_start, theta4_max_rot,
                 start_x, start_y,
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
        self.points = []
        
        self.start_x = start_x
        self.start_y = start_y
        
        pass
    
    def generate_points(self) -> None:
        r1, r2, r3, r4 = self.r1, self.r2, self.r3, self.r4
        
        t2_current = self.t2_i
        t4_current = None
        
        while t2_current <= self.t2_f:
            Ax = 0
            Ay = 0
            Dx = r1
            Dy = 0
            Bx = r2 * math.cos(t2_current)
            By = r2 * math.sin(t2_current)
            
            AD = math.sqrt(r1**2 + r2**2 - 2*r1*r2*math.cos(t2_current))        # using cosine rule
            angle1 = math.acos((r1**2 + AD**2 - r2**2) / (2*r1*AD))             # using cosine rule
            if (By < 0):
                angle1 = -angle1
            angle2 = math.acos((r4**2 + AD**2 - r3**2) / (2*r4*AD))             # using cosine rule
            t4_current = 2*math.pi - (angle1 + angle2)

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
        
        def init():
            line.set_data([], [])
            return line, 
            
        def animate(i):
            thisx = [self.points[i][0], self.points[i][2], self.points[i][4], self.points[i][6], self.points[i][0]]
            thisy = [self.points[i][1], self.points[i][3], self.points[i][5], self.points[i][7], self.points[i][1]]
            line.set_data(thisx, thisy)
            return line, 
        
        anim = FuncAnimation(fig, animate, frames=len(self.points), init_func=init, interval=1, blit=True)
        anim.save("plot.gif", writer='Pillow')