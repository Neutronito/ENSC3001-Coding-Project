#####################################################
##                 Solver Class                     #
#####################################################
class Solver:
    #Class constructor which can take in optional arguments (default to 0)
    #This can be used to construct a default class without needing manual inputs later on
    def __init__(self, arg1=0, arg2=0, arg3=0):
        self.arg1 = arg1 
        self.arg2 = arg2
        self.arg3 = arg3

    #reads input from the user to use as parameters
    #function blocks until a valid input is given
    def read_user_input(self):
        #accept user input through the terminal on the function to use, and the
        #x bounds of the function
        #Up to you to figure out how to store the function, and how to pass it to the
        #next functions
        print()

    #accepts the function and bounds parameters, executing calculations to determine the corresponding 4bar linkage
    #returns an integer array, giving the lengths of the linkages
    def execute_4bar_calculations(self):
        #How the parameters are taken depends on how the above function is done
        #also deal with and report negative error checking
        print()

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
        self.execute_4bar_calculations()
        self.print_results()

#####################################################
##                Main Execution                    #
#####################################################
if __name__ == "__main__":
    testSolver = Solver()
    testSolver.solve()

    testSolver.solve(True)  #Manual input
