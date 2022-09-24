from cmath import pi
import math
import sys
from sympy.abc import x, y
import sympy as sym
import sympy.parsing.sympy_parser as parser

import copy

import plotter

#####################################################
##                   Solver Class                  ##
#####################################################
class Solver:
    #Class constructor which can take in optional arguments (default to 0)
    #This can be used to construct a default class without needing manual inputs later on
    def __init__(self, func="sin(x)", x_min=math.pi/4, x_max=3*math.pi/4,
                    theta2_start=7*math.pi/12, theta2_max_rot=math.pi/2,
                    theta4_start=4*math.pi/3, theta4_max_rot=math.pi/2):
        self.func = parser.parse_expr(func)
        self.x_min = x_min
        self.x_max = x_max
        self.theta2_start   = theta2_start
        self.theta2_max_rot = theta2_max_rot       
        self.theta4_start   = theta4_start
        self.theta4_max_rot = theta4_max_rot
        
        self.x_points = [0, 0, 0]        # Array to store precision points found given Chebyshev spacing
        self.y_points = [0, 0, 0]        # Array to store corresponding y-points from above x-points
        
        self.func_theta2 = None
        self.func_theta4 = None
        
        self.theta2_vals = [0, 0, 0]
        self.theta4_vals = [0, 0, 0]
        
        self.fsn_results = [0, 0, 0]     # Array to store 3 freudenstein results, K1, K2 and K3
        
        self.lengths = [0, 0, 0, 0]      # Array to store solved linkage dimensions

        self.silent_flag = False         # Option for silent execution, true yields no prints

        self.optimise_results = True    # Option to calculation optimised results, true will optimise
        self.use_grashof_inequality = False # Option to satisfy Grashof inequality when determining lengths   (DO NOT USE)
        self.ensure_linkage_validity = True
        self.minimum_range = 0           # The minimum range the answers must have to terminate exeuction early

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

        #parse input angle starting value
        while (True):
            input_rotation_start = input("Enter the start angle of the input link, in degrees. If no value is given, 0 is used as a default.\n")
            if (len(input_rotation_start) == 0):
                break
            
            try:
                self.theta2_start = math.radians(float(input_rotation_start))
                break
            except:
                print("Error, please input only numerical values. Do not include any whitespaces.\n")

        #parse output angle starting value
        while (True):
            output_rotation_start = input("Enter the start angle of the output link, in degrees. If no value is given, 0 is used as a default.\n")
            if (len(output_rotation_start) == 0):
                break
            
            try:
                self.theta4_start = math.radians(float(output_rotation_start))
                break
            except:
                print("Error, please input only numerical values. Do not include any whitespaces.\n")

        #request whether the user wishes for silent print or not
        while (True):
            print_option = input("Do you wish to enable the silent flag? Please type in true for silent execution, and false for verbose execution.\n")

            if print_option.lower() in ['true', '1', 't', 'y', 'yes']:
                self.silent_flag = True
                break
            
            elif print_option.lower() in ['false', '0', 'f', 'n', 'no']:
                self.silent_flag = False
                break

            else:
                print('Error, your input was not understood. Please try again.\n')

        #request whether to optimise results
        while(True):
            optimise_option = input("Do you want to calculate optimal results? In this mode, the program will iterate over many angles and find the result with the smallest range of linkage lengths. WARNING, this can be expensive. Please type in true or false\n")

            if optimise_option.lower() in ['true', '1', 't', 'y', 'yes']:
                self.optimise_results = True
                break
            
            elif optimise_option.lower() in ['false', '0', 'f', 'n', 'no']:
                self.optimise_results = False
                break

            else:
                print('Error, your input was not understood. Please try again.\n')

        #request minimum range if optimisation was enabled
        if (self.optimise_results):
            while(True):
                optimise_option = input("Since you enabled optimised results, please specify a minimum range for the linkage lengths. A higher range can improve execution speed, as the program will terminate as soon as it finds a valid result. Please enter a positive integer to define the miniumum range.\n")
            
                try:
                    input_number = int(optimise_option)
                    if input_number < 0:
                        print("Error, you must input a non negative integer.\n")
                    else:
                        self.minimum_range = input_number
                        break

                except:
                    print("Error, please input only numerical values, as an integer. Do not include any whitespaces.\n")
                

    #accepts the function and bounds parameters, executing calculations to determine the corresponding 4bar linkage
    #returns an integer array, giving the lengths of the linkages
    def execute_4bar_calculations(self) -> None:
        #How the parameters are taken depends on how the above function is done
        #also deal with and report negative error checking

        #These calculations only need to be done once
        self.find_chebyshev_spacing()
        self.find_corresponding_y_points()

        #loop through starting theta 2 angle to start + 360
        start_angle_2 = self.theta2_start
        current_range = math.inf
        optimal_lengths = [0, 0, 0, 0]
        finished_early = False

        start_angle_4 = self.theta4_start
        for x in range(0, 360, 5):
            self.theta2_start = start_angle_2 + math.radians(x)
            
            #loop through starting theta 4 angle to start + 360
            
            for y in range(0, 360, 5):
                self.theta4_start = start_angle_4 + math.radians(y)

                self.linear_mapping_x_to_theta2()
                self.linear_mapping_y_to_theta4()
                self.determine_corresponding_angles()
                self.solve_freudenstein()
                self.solve_linkage_dimensions()

                #check if all values are positive
                found_negative = False    
                for length in self.lengths:
                    if (length < 0):
                        found_negative = True
                 
                       
                # Check Grashof inequality (optional)
                grashof_satisfied = True
                if (self.use_grashof_inequality):
                    ordered = sorted(self.lengths)
                    grashof_satisfied = (ordered[2] + ordered[3] < ordered[0] + ordered[1])
                    
                
                # Check linkage dimensions form valid 4-bar linkage in starting angle
                valid_linkage = True   
                if (self.ensure_linkage_validity):
                    diagonal = math.sqrt(self.lengths[0]**2 + self.lengths[1]**2 - 2*self.lengths[0]*self.lengths[1]*math.cos(self.theta2_start))        # using cosine rule                 
                    valid_linkage = (diagonal + self.lengths[3]) > self.lengths[2]
                    
                #This solution has all positive lengths so we consider it
                if (not found_negative and grashof_satisfied and valid_linkage):
                    
                    #check to see if we should be trying to optimise results
                    if (self.optimise_results):
                        #check to see if its better than what we have
                        biggest_val = max(self.lengths)
                        smallest_val = min(self.lengths)

                        new_range = biggest_val - smallest_val

                        #our result has a smaller range, so its better
                        if new_range < current_range:
                            current_range = biggest_val
                            optimal_lengths = copy.deepcopy(self.lengths)
                            
                            #check if we are below minimum range, if so we should stop
                            if (current_range < self.minimum_range):
                                finished_early = True
                                break

                    else:
                        optimal_lengths = copy.deepcopy(self.lengths)
                        finished_early = True
                        break
            
            if (finished_early):
                break


        
        print("Final Linkage dimensions calculated as follows:")
        print("R1 = %.5f\nR2 = %.5f\nR3 = %.5f\nR4 = %.5f" % tuple(optimal_lengths))
        print()            
        pass
        
    # Applies Chebyshev spacing formula to determine 3 precision points
    def find_chebyshev_spacing(self) -> None:
        n = 3
                
        for j in range(3, 0, -1):   # Counts backwards in sequence 3, 2, 1
            cos_term = math.cos((2*j - 1) * math.pi / (2*n))
            first_term = 0.5 * (self.x_max + self.x_min)
            second_term = 0.5 * (self.x_max - self.x_min) * cos_term
            result = first_term - second_term
            self.x_points[j-1] = result 
        
        if self.silent_flag is False:
            print("Given lower bound of x0 = %f, and upper bound of x4 = %f" % (self.x_min, self.x_max))
            print("Following precision points found:")
            print("x1=%f, x2=%f, x3=%f" % tuple(self.x_points[0:3]))
            print()
        pass
    
    # Substitutes x points into the mathematic function to determine corresponding y points
    def find_corresponding_y_points(self) -> None:        
        for i in range(0, 3):
            x_val = self.x_points[i]
            self.y_points[i] = self.func.subs(x, x_val)

        if self.silent_flag is False: 
            print("Following corresponding y-points found:")
            print("y1=%f, y2=%f, y3=%f" % tuple(self.y_points[0:3]))
            print()
        pass
        
    def linear_mapping_x_to_theta2(self) -> None:
        a, b = sym.symbols("a, b")
        angle1 = self.theta2_start
        angle2 = self.theta2_start + self.theta2_max_rot
        
        eq1 = sym.Eq(a*self.x_min + b, angle1)
        eq2 = sym.Eq(a*self.x_max + b, angle2)
        result = sym.solve([eq1, eq2], (a, b))
        self.func_theta2 = sym.lambdify(x, x*result[a] + result[b])
        
        if self.silent_flag is False:
            print("Linearly mapped x to theta2 (truncated values):")
            print("Theta2 = %.3f * x + %.3f" % (result[a], result[b]))
            print()
        pass
        
    def linear_mapping_y_to_theta4(self) -> None:
        c, d = sym.symbols("c,d")
        angle1 = self.theta4_start
        angle2 = self.theta4_start + self.theta4_max_rot
        y_min = self.func.subs(x, self.x_min)
        y_max = self.func.subs(x, self.x_max)
        
        eq1 = sym.Eq(c*y_min + d, angle1)
        eq2 = sym.Eq(c*y_max + d, angle2)
        result = sym.solve([eq1, eq2], (c, d))
        self.func_theta4 = sym.lambdify(y, y*result[c] + result[d])
        
        if self.silent_flag is False:
            print("Linearly mapped y to theta4 (truncated values):")
            print("Theta4 = %.3f * y + %.3f" % (result[c], result[d]))
            print()
        pass
    
    def determine_corresponding_angles(self) -> None:
        for i in range(3):
            self.theta2_vals[i] = self.func_theta2(self.x_points[i])
            self.theta4_vals[i] = self.func_theta4(self.y_points[i])
        
        if self.silent_flag is False:
            print("Linearly mapped theta values determined:")
            print("Theta2 values:", self.theta2_vals)
            print("Theta4 values:", self.theta4_vals)
            print()
        pass
    
    def solve_freudenstein(self) -> None:
        a,b,c = sym.symbols('a, b, c')
        eq1 = sym.Eq(a*sym.cos(self.theta2_vals[0]) + b*sym.cos(self.theta4_vals[0]) + c, sym.cos(self.theta2_vals[0] - self.theta4_vals[0]))
        eq2 = sym.Eq(a*sym.cos(self.theta2_vals[1]) + b*sym.cos(self.theta4_vals[1]) + c, sym.cos(self.theta2_vals[1] - self.theta4_vals[1]))
        eq3 = sym.Eq(a*sym.cos(self.theta2_vals[2]) + b*sym.cos(self.theta4_vals[2]) + c, sym.cos(self.theta2_vals[2] - self.theta4_vals[2]))
        result = sym.solve([eq1, eq2, eq3], (a, b, c), real=True)
        self.fsn_results[0] = result[a]
        self.fsn_results[1] = result[b]
        self.fsn_results[2] = result[c]

        if self.silent_flag is False:
            print("Freudenstein calculates K1 as %.3f, K2 as %.3F and K3 as %.3f" % tuple(self.fsn_results))
            print()
        pass
    
    # Solves for the dimensions of all linkages, assuming R1 = 1m
    def solve_linkage_dimensions(self) -> None:
        r1 = 1                          
        r4 = r1 / self.fsn_results[0]
        r2 = r1 / self.fsn_results[1]
        
        k = sym.symbols("k")
        r3_list = sym.solve((k**2 - r1**2 -r2**2 - r4**2) / (2*r2*r4) - self.fsn_results[2], k, real=True, rational=False)  # Returns a list with positive and negative result
        r3 = max(r3_list)
        
        self.lengths = [r1, r2, r3, r4]
        
        if self.silent_flag is False:
            print("Linkage dimensions calculated as follows:")
            print("R1 = %.5f\nR2 = %.5f\nR3 = %.5f\nR4 = %.5f" % tuple(self.lengths))
            print()
        pass
    
    #prints out the results of the calculations
    #takes the integer array of lengths as parameter
    def print_results(self):
        #print the results out to the terminal
        #can draw a graph or some other fancy shit too
        
        print("starting angles are:")
        print(math.degrees(self.theta2_start) % 360)
        print(math.degrees(self.theta4_start) % 360)
        r1, r2, r3, r4 = tuple(self.lengths)
        Plot = plotter.Plotter(r1, r2, r3, r4, self.fsn_results, 
                               self.theta2_start, self.theta2_max_rot, self.theta4_start, self.theta4_max_rot)
        Plot.generate_points()
        Plot.animate_linkage()
        
        return

    #method which when called will perform all steps of solving the linkage, and then outputting results
    #will take manual inputs if specified, otherwise uses values from object definition
    def solve(self, manual=False) -> None:
        if manual: 
            self.read_user_input()

        if self.silent_flag is False:  
            print("Function entered is:")
            print("y = " + str(self.func))
            print()
        
        #some testing
        self.optimise_results = True
        self.silent_flag = True
        self.minimum_range = 3

        self.execute_4bar_calculations()
        self.print_results()
        pass

#####################################################
##                Main Execution                    #
#####################################################
if __name__ == "__main__":
    
    # This one is from the workshop
    # testSolver = Solver(func="x**(-2)", 
    #                     x_min=1, x_max=2,
    #                     theta2_start=7*math.pi/12, theta2_max_rot=math.pi/3,
    #                     theta4_start=4*math.pi/3, theta4_max_rot=math.pi/2)
    
    testSolver = Solver(func="sin(x)", 
                        x_min=math.pi/4, x_max=3*math.pi/4,
                        theta2_start=7*math.pi/12, theta2_max_rot=2*math.pi/3,
                        theta4_start=4*math.pi/3, theta4_max_rot=math.pi/3)
    
    # testSolver = Solver(func="ln(x)/ln(10)", 
    #                     x_min=1, x_max=2,
    #                     theta2_start=7*math.pi/12, theta2_max_rot=2*math.pi,
    #                     theta4_start=4*math.pi/3, theta4_max_rot=math.pi/3)
    
    testSolver.solve()


    
    # Examples of input
    # testSolver = Solver(func="x**(0.5)+9")        # How to enter a function from script - ALWAYS INCLUDE MULTIPLICATION SIGNS
    
    
    # testSolver.solve(manual = True)  # Enter True argument for manual input
