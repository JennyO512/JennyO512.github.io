#Your project must be implemented in Python
#must have a main function
    #main function must be in a file called project.py
#three or more additional functions
    #Your 3 required custom functions other than main must
    # also be in project.py and defined at the same
    # indentation level as main
    #not nested under any classes or functions
#must be accompanied by tests that can be executed with pytest
    #must be in a file called test_project.py
    #test_ (test_custom_function, for example, where custom_function
    # is a function you’ve implemented in project.py).

#You are welcome to implement additional classes and
    # functions as you see fit beyond the minimum requirement.
#Must have a requirements.txt listing PIP



def main():
    #get the users input
    weight = float(input("Enter your weight in (lbs): "))
    height = float(input("Enter your height in (inches): "))



    height_converted = convert_height(height) #converting the height from the user into a variable i am using later
    pounds_converted = calcuate_weight(weight)

    bmi = weight/(height**2) * 703

    print()
    print(f"🌎 Your BMI is: {bmi:.2F} 🌎 ")
    print()

    #weightonEarth = float(input("Enter Your Weight on Earth: "))
    weightonMoon = round((weight*1.622)/9.81,2)
    moonpounds = weightonMoon * 2.205
    print(f"🚀 But you are only {moonpounds:.2f} pounds on the moon 🚀 ")
    print()




def convert_height(n2): #<--this function calculates the height * height
    h2 = float(n2**2)
    return h2


def calcuate_weight(n1):   #<--this function just assigns the weight a value to use later
    w = int(n1)
    return w


def cal_bmi(n3): #<--this function just returns the calc of the other 2 functions.
    bmi = round(n3)
    return bmi


if __name__== "__main__":
    main()