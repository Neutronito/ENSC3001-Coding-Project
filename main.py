from sympy.abc import x
import sympy.parsing.sympy_parser as parser
import math

#####################################################
##                 Solver Class                     #
#####################################################
class Solver:
    #Class constructor which can take in optional arguments (default to 0)
    #This can be used to construct a default class without needing manual inputs later on
    #Note, all angles are in radians
    def __init__(self, func="2*x", x_min=1, x_max=2,
                    theta2_start=0, theta2_max_rot=0,
                    theta4_start=0, theta4_max_rot=0):
        self.func = parser.parse_expr(func)
        self.x_min = x_min
        self.x_max = x_max
        self.theta2_start   = theta2_start
        self.theta2_max_rot = theta2_max_rot       
        self.theta4_start   = theta4_start
        self.theta4_max_rot = theta4_max_rot
        
        self.x_points = [0, 0, 0, 0]  # Array to store precision points found given Chebyshev spacing
        self.y_points = [0, 0, 0]        # Array to store corresponding y-points from above x-points

    #reads input from the user to use as parameters
    #function blocks until a valid input is given
    def read_user_input(self):
        #accept user input through the terminal on the function to use, and the
        #x bounds of the function
        #Up to you to figure out how to store the function, and how to pass it to the
        #next functions

        print("This function accepts the following inputs and uses them to calculate the lengths of the appropriate four bar linkage.")
        print("\n1: \t The function \t\t\t\t\t E.g. 2*x + 3")
        print("2: \t The lower and upper x boundary \t\t E.g. 1.2 12.5")
        print("3: \t The rotation of the input link, in degrees \t E.g. 30")
        print("4: \t The rotation of the output link, in degrees \t E.g. 60")
        print("\n")

        #parse the function
        while (True):
            function_input = input("Enter the function. Please note, you MUST include all multiplications using the * symbol, and do not include y=\n")
            try:
                self.func = parser.parse_expr(function_input)
                break
            except:
                print("Error, your equation was invalid. Did you forget to remove the = sign, or include all the *?\n")
                

        #parse the x bounds
        while (True):
            function_bounds = input("Enter the lower and upper x boundaries (respectively) as two number seperated by a whitespace\n")
            split_bounds = function_bounds.split(" ")
            try:
                self.x_min = float(split_bounds[0])
                self.x_max = float(split_bounds[1])

                if (self.x_max > self.x_min):
                        break
                print("Error, the upper bound must be bigger than the lowerbound\n")
            except: 
                print("Error, please input only numerical values, ensuring the two values are seperated by a whitespace\n")
        
        #parse input angle range
        while (True):
            input_rotation = input("Enter the rotation of the input link, in degrees\n")
            try:
                self.theta2_max_rot = math.radians(float(input_rotation))
                break
            except:
                print("Error, please input only numerical values. Do not include any whitespaces.\n")

        #parse output angle range
        while (True):
            output_rotation = input("Enter the rotation of the output link, in degrees\n")
            try:
                self.theta4_max_rot = math.radians(float(output_rotation))
                break      
            except:
                print("Error, please input only numerical values. Do not include any whitespaces.\n")


    #accepts the function and bounds parameters, executing calculations to determine the corresponding 4bar linkage
    #returns an integer array, giving the lengths of the linkages
    def execute_4bar_calculations(self):
        #How the parameters are taken depends on how the above function is done
        #also deal with and report negative error checking
        
        self.find_chebyshev_spacing()
        self.find_corresponding_y_points()
        print()
        
    # Applies Chebyshev spacing formula to determine 3 precision points
    def find_chebyshev_spacing(self):
        n = 3
        self.x_points[3] = self.x_max
        
        for j in range(2, -1, -1):   # Counts backwards in sequence 2, 1, 0
            cos_term = math.cos((2*(j+1) - 1) * math.pi / (2*n))
            first_term = 0.5 * (self.x_points[j+1] + self.x_min)
            second_term = 0.5 * (self.x_points[j+1] - self.x_min) * cos_term
            result = first_term - second_term
            self.x_points[j] = result 
        
        print("Given lower bound of x0 = %f, and upper bound of x4 = %f" % (self.x_min, self.x_max))
        print("Following precision points found:")
        print("x1=%f, x2=%f, x3=%f" % tuple(self.x_points[0:3]))
        print()
        return
    
    def find_corresponding_y_points(self):        
        for i in range(0, 3):
            x_val = self.x_points[i]
            self.y_points[i] = self.func.subs(x, x_val)
            
        print("Following corresponding y-points found:")
        print("y1=%f, y2=%f, y3=%f" % tuple(self.y_points[0:3]))
        print()
        return
        
    #prints out the results of the calculations
    #takes the integer array of lengths as parameter
    def print_results(self):
        #print the results out to the terminal
        #can draw a graph or some other fancy shit too
        print()

    #method which when called will perform all steps of solving the linkage, and then outputting results
    #will take manual inputs if specified, otherwise uses values from object definition
    def solve(self, manual=False):
        if manual: 
            self.read_user_input()
            
        print("Function entered is:")
        print("y = " + str(self.func))
        print()
        
        self.execute_4bar_calculations()
        self.print_results()

#####################################################
##                Main Execution                    #
#####################################################
if __name__ == "__main__":
    

    testSolver = Solver()
    testSolver.solve(True)

    
    # Examples of input
    # testSolver = Solver(func="x**(0.5)+9")        # How to enter a function from script - ALWAYS INCLUDE MULTIPLICATION SIGNS
    
    
    # testSolver.solve(manual = True)  # Enter True argument for manual input
