from Tkinter import *
import os
root = Tk()
image = "1.bmp"
canv = 0
table = [[16777215 for col in range(802)] for row in range(602)]


def nop():
    print "nothing happened"

def end():
    global root
    root.destroy()

def rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

def put_pixel(x, y, r, g, b):
    global canv
    return canv.create_line(x, y, x + 1, y, fill = rgb(r, g, b))

def open_image():
    global image
    if not os.path.exists(image):
        print "No such file"
        return
    img = open(image, "rb")
    head = img.read(54)
    if not head:
        print "error"
        img.close()
        return
    width = ord(head[18]) + ord(head[19]) * 256
    height = ord(head[22]) + ord(head[23]) * 256
    t = width * 3 / 4 * 4
    if t < width * 3:
        t += 4
    t -= width * 3
    #global table
    for j in range(height, 0, -1):
        for i in range(1, width + 1):
            b = ord(img.read(1))
            g = ord(img.read(1))
            r = ord(img.read(1))
            put_pixel(i, j, r, g, b)
            table[j][i] = (r << 16) + (g << 8) + b
        for i in range(t):
            empty = img.read(1)
    img.close()

def make_str(x, num):
    s = ""
    for i in range(num):
        s += chr(x & 255)
        x >>= 8
    return s

def write_image():
    img = open("2.bmp", "wb")
    global canv
    width = canv.winfo_width() - 4
    height = canv.winfo_height() - 4
    t = width * 3 / 4 * 4
    if t < width * 3:
        t += 4
    size = 54 + t * height
    string = ""
    #===header===
    string += "BM"
    string += make_str(size, 4)
    string += make_str(0, 2)
    string += make_str(0, 2)
    string += make_str(54, 4)
    #===info header===
    string += make_str(40, 4)
    string += make_str(width, 4)
    string += make_str(height, 4)
    string += make_str(1, 2)
    string += make_str(24, 2)
    string += make_str(0, 4)
    string += make_str(size - 54, 4)
    string += make_str(3780, 4)
    string += make_str(3780, 4)
    string += make_str(0, 4)
    string += make_str(0, 4)
    #===data====
    #global table
    t -= width * 3
    for j in range(height, 0, -1):
        for i in range(1, width + 1):
            color = table[j][i]
            string += make_str(color, 3)
        for i in range(t):
            string += make_str(0, 1)
    #===end===
    img.write(string)
    img.close()
    

def pack_menu_list():
    global root
    m = Menu(root)
    root.config(menu = m)
    #===file===
    filemenu = Menu(m)
    m.add_cascade(label = "File", menu = filemenu)
    filemenu.add_command(label = "New", command = nop)
    filemenu.add_command(label = "Open...", command = open_image)
    filemenu.add_command(label = "Save As...", command = write_image)
    filemenu.add_separator()
    filemenu.add_command(label = "Exit", command = end)
    #===help===
    helpmenu = Menu(m)
    m.add_cascade(label = "Help", menu = helpmenu)
    helpmenu.add_command(label = "Help", command = nop)
    helpmenu.add_command(label = "About", command = nop)
    #===return===
    return m

def pack_tool_list():
    global root
    f = Frame(root, width = 100, height = 600)
    f.pack(side = "left")
    return f

def pack_main_table():
    c = Canvas(root,width = 800,height = 600,bg = "white")
    c.pack(side = "left")
    return c

def main():
    global root
    menu = pack_menu_list()
    tool = pack_tool_list()
    global canv
    canv = pack_main_table()
    root.mainloop()

main()
