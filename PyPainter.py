from Tkinter import *
import os
root = Tk()
image = "1.bmp"
canv = 0

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
    head = []
    if not os.path.exists(image):
        print "No such file"
        return
    img = open(image, "rb")
    head = img.read(54)
    if not head:
        print "error"
        img.close()
        return
    length = ord(head[18]) + ord(head[19]) * 256
    width = ord(head[22]) + ord(head[23]) * 256
    print length, width
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
    filemenu.add_command(label = "Save As...", command = nop)
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
    f.pack(side="left")
    return f

def pack_main_table():
    c = Canvas(root,width=800,height=600,bg="white")
    c.pack(side="left")
    return c

def main():
    global root
    menu = pack_menu_list()
    tool = pack_tool_list()
    global canv
    canv = pack_main_table()
    root.mainloop()

main()
