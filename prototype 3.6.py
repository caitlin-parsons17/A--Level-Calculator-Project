



# libraries
from guizero import *
import sympy as sp

# window GUI setup
main = App("calculator", height=600, width=350)
screen_value = ""
ans = ""
# variables to keep track of store and shift procedures
shift_pressed = False
store_mode = False

A=0
B=0
C=0
D=0

#Functions
def displaychar(num): #displays character when typed
    global display_text, screen_value
    num = str(num)
    screen_value += num
    display_text.value = screen_value
    
def delete_char(): # removes most recently typed character
    global screen_value
    screen_value = screen_value[:-1]
    display_text.value = screen_value
    
def clear_all(): # clears the display
    global screen_value
    screen_value = ""
    display_text.value = screen_value

def on_enter(button): #responds to mouse hovering over a button
    button.bg = "lightblue"

def on_leave(button): # responds to mouse leaving a button
    button.bg = "white"

def update_button_labels(): # called when shift is pressed
    if shift_pressed: # changes buttons appearance according to shift
        factor.text= "diff"
        expand.text= "int"
        sin.text="csc"
        cos.text="sec"
        tan.text="cot"
        log.text="10"
        naturallog.text="e"
        root.text="∛"
        letterx.text= "π"
    else:
        factor.text = "factr"
        expand.text = "exp"
        sin.text = "sin"
        cos.text = "cos"
        tan.text = "tan"
        log.text = "log"
        naturallog.text = "ln"
        root.text = "√"
        letterx.text = "𝑥"

def toggle_shift(): 
    global shift_pressed
    shift_pressed = not shift_pressed
    update_button_labels()

def toggle_store():
    global store_mode
    store_mode = not store_mode
    
def save_variables(): 
    variables = {'A': A,
                 'B': B,
                 'C': C,
                 'D': D}
    with open('variables.txt', 'w') as file:
        for key, value in variables.items():
            file.write(f"{key}={value}\n")

def load_variables(): # called each time the program starts
    try:
        with open('variables.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                if key in ['A', 'B', 'C', 'D']:
                    globals()[key]=float(value)
    except FileNotFoundError:
        print("Variables file not found.")
        

def handle_button_press(value): 
    global shift_pressed, screen_value, store_mode

    if store_mode:
        if value in ["A", "B", "C", "D"]:
            globals()[value] = screen_value
            save_variables()
            display_text.value = "Stored to" + value
        store_mode = False
        return

    if shift_pressed: 
        if value == "factr": # if differentiate or integrate are pressed
            perform_operation("differentiate")
        elif value == "exp":
            perform_operation("integrate")
        elif value == "log(": # otherwise, typed shift characters
            screen_value += "10"
        elif value == "ln(":
            screen_value += "e"
        elif value == "sin(":
            screen_value +="csc("
        elif value == "cos(":
            screen_value += "sec("
        elif value == "tan(":
            screen_value += "cot("
        elif value == "√(":
            screen_value += "∛("
        elif value == "𝑥":
            screen_value += "π"
        display_text.value = screen_value
    else:
        if value == "factr": # if factorise or expression are pressed
            perform_operation("factorize")
        elif value == "exp":
            perform_operation("expand")
        else:
            displaychar(value) # otherwise typed characters


def replace_chars(): # translates the symbols used into a python expression
    global screen_value
    variable_values = {"A": A, "B": B, "C": C, "D":D}
    for var, value in variable_values.items():
        screen_value = screen_value.replace(var, str(value))
    replacementchars = [["^", "**"],["𝑥", "x"],["×", "*"],["÷", "/"],["√", "sqrt"],["∛" , "cbrt"],["ANS", ans]]
    for i in range (len(replacementchars)):
        if replacementchars [i][0] in screen_value:
            screen_value = screen_value.replace (replacementchars[i][0] , replacementchars[i][1])

def perform_operation(operation_type):
    global screen_value, ans
    if not screen_value:
        return
    replace_chars()
    if len(screen_value) > 100: #limits the length of the input
        screen_value = "Error: Expression too long"
        display_text.value = screen_value
    try:
        x = sp.symbols('x')
        expr = sp.sympify(screen_value)
        if operation_type == 'differentiate':
            result = sp.diff(expr, x)
        elif operation_type == 'integrate':
            result = sp.integrate(expr, x)
        elif operation_type == 'expand':
            result = sp.expand(expr)
        elif operation_type == 'factorize':
            result = sp.factor(expr)
        else:
             result = sp.N(expr.subs(x, 0))
        screen_value = str(result)
        if len(screen_value) > 22: # limits the size of the output
            screen_value = "Error: Result is too long."
            display_text.value = screen_value
            return
        ans = screen_value
        display_text.value = screen_value
    except sp.SympifyError: # gives specific error messages
        screen_value = "Syntax Error"
        display_text.value = screen_value
    except ValueError:
        screen_value = "Inappropriate Value"
        display_text.value = screen_value
    except Exception:
        screen_value = "Unexpected Error"
        display_text.value = screen_value


def create_button(parent, command, text, grid): # uses OOP to create buttons
    box = Box(parent, layout="grid", grid=grid)
    button = PushButton(box, command=command, text=text, grid=grid)
    button.bg = "white"
    box.when_mouse_enters = lambda: on_enter(button) #all buttons inheret hover effect
    box.when_mouse_leaves = lambda: on_leave(button)
    return button

#GUI for screen
spacer = Text(main, text="")
screen_box = Box(main, border=True, height=100, width=200, )
display_text = Text(screen_box, align="left")

#GUI for buttons
spacer2 = Text(main, text="")
extras_box = Box(main, layout="grid")

#top functional buttons
shift = create_button(extras_box, lambda: toggle_shift(), "shift", [0, 0])
store = create_button(extras_box, lambda: toggle_store() , "STO", [1,0])

# top buttons
factor = create_button(extras_box, lambda: handle_button_press("factr"), "factr", [0, 1])
expand = create_button(extras_box, lambda: handle_button_press("exp"), "exp", [1, 1])
sin = create_button(extras_box, lambda: handle_button_press("sin("), "sin", [2, 1])
cos = create_button(extras_box, lambda: handle_button_press("cos("), "cos", [3, 1])
tan = create_button(extras_box, lambda: handle_button_press("tan("), "tan", [4, 1])

log = create_button(extras_box, lambda: handle_button_press("log("), "log", [0, 2])
naturallog = create_button(extras_box, lambda: handle_button_press("ln("), "ln", [1, 2])
root = create_button(extras_box, lambda: handle_button_press("√("), "√", [2, 2])
indicie = create_button(extras_box, lambda: handle_button_press("^"), "^", [3, 2])
letterx = create_button(extras_box, lambda: handle_button_press("𝑥"), "𝑥", [4, 2])

# letter buttons
variable_a = create_button(extras_box, lambda: handle_button_press("A"), "A", [0,3])
variable_b = create_button(extras_box, lambda: handle_button_press("B"), "B", [1,3])
variable_c = create_button(extras_box, lambda: handle_button_press("C"), "C", [2,3])
variable_d = create_button(extras_box, lambda: handle_button_press("D"), "D", [3,3])



spacer3 = Text(main, text="")



# bottom buttons
numbers_box = Box(main, layout="grid")
one = create_button(numbers_box, lambda: displaychar(1),"1",[0, 0])
two = create_button(numbers_box, lambda: displaychar(2),"2",[1, 0])
three = create_button(numbers_box,lambda: displaychar(3),"3", [2, 0])
plus = create_button(numbers_box,lambda: displaychar("+"),"+",[3, 0])
minus = create_button(numbers_box,lambda: displaychar("-"),"-",[4, 0])
four = create_button(numbers_box, lambda:displaychar(4) , "4", [0, 1])
five = create_button(numbers_box, lambda: displaychar(5), "5", [1, 1])
six = create_button(numbers_box, lambda: displaychar(6), "6", [2, 1])
multiply =create_button(numbers_box, lambda: displaychar("×"), "×", [3, 1])
divide =create_button(numbers_box, lambda: displaychar("÷"), "÷", [4, 1])
seven = create_button(numbers_box, lambda: displaychar(7), "7", [0, 2])
eight = create_button(numbers_box, lambda: displaychar(8), "8", [1, 2])
nine = create_button(numbers_box, lambda: displaychar(9), "9", [2, 2])
less = create_button(numbers_box, lambda: displaychar("<"), "<", [3, 2])
greater = create_button(numbers_box, lambda: displaychar("."), ".", [4, 2])
ansbutton = create_button(numbers_box, lambda: displaychar("ANS"), "ANS", [5, 2])
zero = create_button(numbers_box, lambda: displaychar(0), "0", [0, 3])
openbracket = create_button(numbers_box, lambda: displaychar("("), "(", [1, 3])
closebracket = create_button(numbers_box, lambda: displaychar(")"), ")", [2, 3])



#bottom functional buttons
equals = create_button(numbers_box, lambda: perform_operation("equals"), "=", [3, 3])
delete = create_button(numbers_box, delete_char, "DEL", [4, 3])
allclear = create_button(numbers_box, clear_all, "AC", [5, 3])


main.display() # opens the app
load_variables() # loads stored variables
