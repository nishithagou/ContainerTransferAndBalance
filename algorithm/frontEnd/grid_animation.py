import datetime
import tkinter as tk
import time


class container:
    def __init__(self, description, weight, x, y, toOffload=False):
        self.weight = weight
        self.description = description
        self.x = x
        self.y = y
        self.toOffload = toOffload

    def getDescription(self):
        return self.description

    def toString(self):
        return self.description + " (weight: " + str(self.weight) + ")" + " Coords: (" + str(self.x) + "," + str(self.y) + ")"

    def getWeight(self):
        return self.weight

    def isToBeOffloaded(self):
        return self.toOffload


#reads manifest and uploads container vals
def read_manifest(file):
    containers = []
    manifest = open(file, 'r')
    while True:
        line = manifest.readline()
        if not line:
            break
        line = line.strip()
        #name
        name=(line[18:])
        #x and y coords
        x=int(line[1:3])
        y=int(line[4:6])
        #weight
        w=int(line[10:15])
        containers.append(container(name,w,x,y))
    return containers

def signin(first_name, last_name, log_file):
    first_name = input("First Name: ")
    while first_name == "":
        print("Invalid name, please try again")
        first_name = input("First Name: ")
    last_name = input("Last Name: ")
    while last_name == "":
        print("Invalid name, please try again")
        last_name = input("Last Name: ")
    print("Hello " + first_name + " " + last_name + "\n")
    log_file.write(str(datetime.datetime.now()) + " " + first_name + " " + last_name + " signed in\n")
    return [first_name, last_name]

def signout(first_name, last_name, log_file):
    option = input("Enter c to add a commment to the log file. \n or \nEnter x to logout. \n Enter any other key to continue to the next step: ")
    if option == "c":
        comment = input("Please enter the text you would like to add to the log: ")
        log_file.write(str(datetime.datetime.now()) + " " + first_name + " " + last_name + " logged: " + comment + "\n")
        return [first_name, last_name]    
    elif option == "x":
        log_file.write(str(datetime.datetime.now()) + " " + first_name + " " + last_name + " signs out\n")
        return signin(first_name, last_name, log_file)
    else:
        return [first_name, last_name]






#***************************************ANIMATION PART************************************#

ROWS = 9
COLS = 12
SQUARE_SIZE = 50
WINDOW_WIDTH = COLS * SQUARE_SIZE * 2
WINDOW_HEIGHT = ROWS * SQUARE_SIZE * 2

running = True

def draw_grid(canvas, rows, cols, width, height, objects_list):
    if(running):
    
        labels = [None] * (rows * cols)
        #count = 0
        for obj in objects_list:
            #print(obj.description)
            #count+=1
            x, y = obj.y - 1, obj.x - 1
            if 0 <= x < cols and 0 <= y < rows:
                index = y * cols + x
                labels[index] = obj.description

        # Draw grid and labels
        for row in range(rows):
            for col in range(cols):
                x1 = col * width
                y1 = (rows - row - 1) * height
                x2 = x1 + width
                y2 = y1 + height
                index = row * cols + col
                if row == 8:  # If current cell is in top row
                    canvas.create_rectangle(x1, y1, x2, y2, fill='light gray', outline='black')
                    #label = tk.Label(canvas, text='buffer')
                    #label.place(x=x1+5, y=y1+5)
                elif(labels[index] != "NAN" and labels[index] != "UNUSED" ):
                    canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, outline='black')
                #print("Going to draw grid.")
                if labels[index]:
                    label = tk.Label(canvas, text=labels[index])
                    label.place(x=x1+5, y=y1+5)


def move_box(canvas, box, coords_list):
    if not coords_list:
        return
    # starting vals
    x1, y1, x2, y2 = canvas.coords(box)
    width = x2 - x1
    height = y2 - y1

    # get current and next coordinates
    current_x, current_y = coords_list[0]
    next_x, next_y = coords_list[1] if len(coords_list) > 1 else coords_list[0]

    # calculate coordinates of line to move the box
    start_x = current_x * width + width / 2
    start_y = (8 - current_y - 1) * height + height / 2
    end_x = next_x * width + width / 2
    end_y = (8 - next_y - 1) * height + height / 2

    # this part helps the movement work smoother, ik it looks ugly
    line = canvas.create_line(start_x, start_y, end_x, end_y)

    #moving box
    for i in range(1, 101):
        # calculate new position of box
        x = start_x + (end_x - start_x) * i / 100
        y = start_y + (end_y - start_y) * i / 100
        canvas.coords(box, x - width / 2, y - height / 2, x + width / 2, y + height / 2)
        canvas.update()
        time.sleep(0.0000005)

    #go to next coord
    canvas.delete(line)
    canvas.after(0, lambda: move_box(canvas, box, coords_list[1:]))



#need to pass the list of containers as argument
def finalDraw(containerList):
    window = tk.Tk()
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canvas.pack()

    #testing with ShipCase1 file to see if boxes populate correctly
    x = read_manifest('ShipCase1.txt')
    coords_list = [(0, 0), (0, 1), (0,2), (0,0), (2,1), (2,2), (3,3)]
    draw_grid(canvas, 8, 12, 100, 100, containerList)

    # Create the box
    box = canvas.create_rectangle(0, 0, 100, 100, fill='red')

    #TODO: need to add the list of tuples for the container movement here
    move_box(canvas, box, coords_list)
    window.mainloop()


   

#**********************************************************command line interactions*****************************************************************
#the container coords have to be reversed, so x =>y and y =>x




coords_list = [[(0, 0), (0, 1), (0,2), (0,3)], 
               [(7,1), (8,1), (9,1)],
               [(0, 0), (0, 1), (0,2), (0,3)]]

log_file = open("logfile.txt", "a")
print("Hello welcome to Mr.Keogh's Port!!! \n")
print("Enter your first and last name to sign in. \n")
first_name = ""
last_name = ""
inputs = signin(first_name, last_name, log_file)
first_name = inputs[0]
last_name = inputs[1]
print("Hello " + first_name + " " + last_name)
#file = input("Please upload the manifest file: (type in the path to the file) ")
containers = read_manifest('ShipCase2.txt')
log_file.write(str(datetime.datetime.now()) + " Manifest " + 'ShipCase3.txt'+ " was opened, there are " + str(len(containers)) + " containers on the ship\n")
#print the initial ship configuration
print("This is your ship.")
window = tk.Tk()
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
#done_button = tk.Button(window, text="Step Completed", command=done_button_click, width = 15, height = 3)
#done_button.pack(side=tk.BOTTOM)

#logout_button = tk.Button(window, text="Logout", command=logout_button_click, width=14, height=3)
#logout_button.pack(side=tk.BOTTOM)

canvas.pack()
draw_grid(canvas, 9, 12, 100, 100, containers)
#print(coords_list[0])
box = canvas.create_rectangle(0, 0, 100, 100, fill='red')

operation = int(input("Please select which operation you would like to perform. 1. Load/Unload containers 2.Balance "))
toOff = []
toOn = []
if(operation == 1):
    print("You chose to load/unload containers.")
    off = input("Please enter the name of the containers you would like to unload. Press q when done. ")
    while(off != 'q'):
        toOff.append(off)
        off = input("Please enter the name of the containers you would like to unload. Press q when done. ")
    print(toOff)
    on = input("Please enter the name of the containers you would like to load.")
    while(on != 'q'):
        weight = input("Please enter the weight of that container. Press q when done ")
        on = input("Please enter the name of the containers you would like to unload. Press q when done. ")
        toOn.append(container(on,weight,0,0))
    print(toOn)

elif(operation == 2):
    print("You chose to balance the ship.")
else:
    #checking for invalid choice
    operation = input("Please select a valid option.")
    if(operation == 1):
        print("You chose to load/unload containers.")
    elif(operation == 2):
        print("You chose to balance the ship.")

print("This are the action step:")
for i in range(0,len(coords_list)):
    move_box(canvas, box, coords_list[i])
print("Done")









































