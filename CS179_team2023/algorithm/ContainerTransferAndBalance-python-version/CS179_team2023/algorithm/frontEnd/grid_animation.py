import tkinter as tk
import reader

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


#***************************************ANIMATION PART************************************#
#defining size vals for grid
ROWS = 8
COLS = 12
SQUARE_SIZE = 50
WINDOW_WIDTH = COLS * SQUARE_SIZE * 2
WINDOW_HEIGHT = ROWS * SQUARE_SIZE * 2


def draw_grid(canvas, rows, cols, width, height, objects_list):
    labels = [None] * (rows * cols)
    #count = 0
    for obj in objects_list:
        #print(obj.description)
        #count+=1
        x, y = obj.y - 1, obj.x - 1
        if 0 <= x < cols and 0 <= y < rows:
            index = y * cols + x
            labels[index] = obj.description
    #print("Count ", count)

    # Draw grid and labels
    for row in range(rows):
        for col in range(cols):
            x1 = col * width
            y1 = (rows - row - 1) * height
            x2 = x1 + width
            y2 = y1 + height
            index = row * cols + col
            canvas.create_rectangle(x1, y1, x2, y2, outline='black')
            if labels[index]:
                label = tk.Label(canvas, text=labels[index])
                label.place(x=x1+5, y=y1+5)


def move_box(canvas, box, coords_list):
    if not coords_list:
        return
    #starting vals
    x, y = coords_list[0]
    x1, y1, x2, y2 = canvas.coords(box)
    width = x2 - x1
    height = y2 - y1
    anotha_x1 = x * width
    anotha_y1 = (8 - y - 1) * height
    anotha_x2 = anotha_x1 + width
    anotha_y2 = anotha_y1 + height
    canvas.coords(box, anotha_x1, anotha_y1, anotha_x2, anotha_y2)
    canvas.update()
    canvas.after(1000, lambda: move_box(canvas, box, coords_list[1:]))


#need to pass the list of containers as argument
def finalDraw(containerList):
    window = tk.Tk()
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canvas.pack()

    #testing with ShipCase1 file to see if boxes populate correctly
    x = read_manifest('ShipCase1.txt')
    coords_list = [(0, 0), (0, 1), (0,2), (0,0)]
    draw_grid(canvas, 8, 12, 100, 100, containerList)

    # Create the box
    box = canvas.create_rectangle(0, 0, 100, 100, fill='red')

    #TODO: need to add the list of tuples for the container movement here
    move_box(canvas, box, coords_list)
    window.mainloop()

#calling the draw function



#command line interactions
print("Hello welcome to Mr.Keogh's Port!!! \n")
print("Please sign in \n")
firstName = input("Enter your first name: ")
lastName = input("Enter your last name: ")
print("Hello " + firstName + " " + lastName)
#file = input("Please upload the manifest file: (type in the path to the file) ")
containers = read_manifest('ShipCase3.txt')
#print the initial ship configuration
window = tk.Tk()
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()
draw_grid(canvas, 8, 12, 100, 100, containers)

##will add a button to close the pop up window but click the x for now to resume program

operation = int(input("Please select which operation you would like to perform. 1. Load/Unload containers 2.Balance "))
if(operation == 1):
    print("You chose to load/unload containers.")
elif(operation == 2):
    print("You chose to balance the ship.")
else:
    #checking for invalid choice
    operation = input("Please select a valid option.")
    if(operation == 1):
        print("You chose to load/unload containers.")
    elif(operation == 2):
        print("You chose to balance the ship.")
