from Tkinter import *
import math
import os
root = Tk()
image = "1.bmp"
canv = 0
table = [[0xffffff for col in range(802)] for row in range(602)]
visited = [[0 for col in range(602)] for row in range(802)]
queue = [[0 for col in range(2)] for row in range(480002)]
v = IntVar()
v.set(1)
state = 1
rv = StringVar()
rv.set("0")
gv = StringVar()
gv.set("0")
bv = StringVar()
bv.set("0")
frv = StringVar()
frv.set("255")
fgv = StringVar()
fgv.set("255")
fbv = StringVar()
fbv.set("255")
hx = []
hy = []
open_window = 0
save_window = 0
help_window = 0
about_window = 0
ov = StringVar()
ov.set("1.bmp")
sv = StringVar()
sv.set("2.bmp")
help_str = "1.Color\n*Color is represented by RGB value.\n*Each value is between 0 and 255.\n2.Paint\n*Use them like that in MSPaint.\n3.Warning\n*Filler is very slow, please use it carefully.\n4.Hint\n*For detailed help, please read report.pdf."
about_str = "PyPainter V1.2\nMade by Chu Wei\n2015.6.9"

def nop():
    print "nothing happened"

def end():
    global root
    root.destroy()

def rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

def put_pixel(x, y, r, g, b):
    global canv, table
    table[y][x] = (r << 16) + (g << 8) + b
    canv.create_line(x, y, x + 1, y, fill = rgb(r, g, b))

def open_image():
    global ov
    image = ov.get()
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
    global canv, table
    canv.destroy()
    canv = pack_main_table()
    table = [[0xffffff for col in range(802)] for row in range(602)]
    canv.bind("<Button-1>", paint_start)
    canv.bind("<B1-Motion>", paint_work)
    canv.bind("<ButtonRelease-1>", paint_end)
    canv.bind("<Double-Button-1>", poly_end)
    buf = img.read()
    ptr = -1
    #global table
    for j in range(height, 0, -1):
        for i in range(1, width + 1):
            b = ord(buf[ptr + 1])
            g = ord(buf[ptr + 2])
            r = ord(buf[ptr + 3])
            ptr += 3
            if table[j][i] != (r << 16) + (g << 8) + b:
                put_pixel(i, j, r, g, b)
            table[j][i] = (r << 16) + (g << 8) + b
        for i in range(t):
            ptr += 1
    img.close()
    global open_window
    open_window.destroy()
    open_window = 0

def make_str(x, num):
    s = ""
    for i in range(num):
        s += chr(x & 255)
        x >>= 8
    return s

def save_image():
    global sv
    image = sv.get()
    img = open(image, "wb")
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
    global table
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
    global save_window
    save_window.destroy()
    save_window = 0

def show_open_window():
    global open_window, ov
    if open_window != 0:
        open_window.destory()
    open_window = Toplevel()
    open_window.title("Open file")
    Label(open_window, text = "Input file name:").pack()
    Entry(open_window, textvariable = ov).pack()
    Button(open_window, text = "OK", command = open_image).pack()

def show_save_window():
    global save_window, sv
    if save_window != 0:
        save_window.destroy()
    save_window = Toplevel()
    save_window.title("Save file")
    Label(save_window, text = "Input file name:").pack()
    Entry(save_window, textvariable = sv).pack()
    Button(save_window, text = "OK", command = save_image).pack()

def end_help():
    global help_window
    if help_window != 0:
        help_window.destroy()
    help_window = 0

def show_help_window():
    global help_window
    if help_window != 0:
        help_window.destroy()
    help_window = Toplevel()
    help_window.title("Help")
    help_window.geometry("300x200")
    Label(help_window, text = "===Brief help===").pack()
    Label(help_window, text = help_str, justify = "left").pack()
    Button(help_window, text = "OK", command = end_help).pack()

def end_about():
    global about_window
    if about_window != 0:
        about_window.destroy()
    about_window = 0

def show_about_window():
    global about_window
    if about_window != 0:
        about_window.destroy()
    about_window = Toplevel()
    about_window.title("About")
    about_window.geometry("200x100")
    Label(about_window, text = about_str).pack()
    Button(about_window, text = "OK", command = end_about).pack()

def pack_menu_list():
    global root
    m = Menu(root)
    root.config(menu = m)
    #===file===
    filemenu = Menu(m)
    m.add_cascade(label = "File", menu = filemenu)
#    filemenu.add_command(label = "New", command = nop)
    filemenu.add_command(label = "Open...", command = show_open_window)
    filemenu.add_command(label = "Save...", command = show_save_window)
    filemenu.add_separator()
    filemenu.add_command(label = "Exit", command = end)
    #===help===
    helpmenu = Menu(m)
    m.add_cascade(label = "Help", menu = helpmenu)
    helpmenu.add_command(label = "Help", command = show_help_window)
    helpmenu.add_command(label = "About", command = show_about_window)
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

def clear_screen():
    global canv, root, table
    canv.destroy()
    canv = pack_main_table()
    table = [[0xffffff for col in range(802)] for row in range(602)]
    canv.bind("<Button-1>", paint_start)
    canv.bind("<B1-Motion>", paint_work)
    canv.bind("<ButtonRelease-1>", paint_end)
    canv.bind("<Double-Button-1>", poly_end)

def make_line(x1, y1, x2, y2):
    global canv, table, rv, gv, bv
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    elif x1 == x2 and y1 > y2:
        y1, y2 = y2, y1
    r = eval(rv.get())
    g = eval(gv.get())
    b = eval(bv.get())
    color = (r << 16) + (g << 8) + b
    canv.create_line(x1, y1, x2, y2, fill = rgb(r, g, b))
    if abs(x1 - x2) <= abs(y1 - y2):
        if y1 == y2:
            y = y1
            x = x1
            table[y][x] = color
        elif y1 < y2:
            for y in range(y1, y2 + 1):
                x = (y - y1 + 0.0) / (y2 - y1) * (x2 - x1) + x1
                x = int(round(x))
                table[y][x] = color
        else:
            for y in range(y2, y1 + 1):
                x = (y - y1 + 0.0) / (y2 - y1) * (x2 - x1) + x1
                x = int(round(x))
                table[y][x] = color
    else:
        for x in range(x1, x2 + 1):
            y = (x - x1 + 0.0)/ (x2 - x1) * (y2 - y1) + y1
            y = int(round(y))
            table[y][x] = color

def make_rectangle(x1, y1, x2, y2):
    global canv, table, rv, gv, bv, frv, fgv, fbv
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    r = eval(rv.get())
    g = eval(gv.get())
    b = eval(bv.get())
    color = rgb(r, g, b)
    fr = eval(frv.get())
    fg = eval(fgv.get())
    fb = eval(fbv.get())
    fill_color = rgb(fr, fg, fb)
    canv.create_rectangle(x1, y1, x2, y2, outline = color, fill = fill_color)
    lc = (r << 16) + (g << 8) + b
    fc = (fr << 16) + (fg << 8) + fb
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if x == x1 or x == x2 or y == y1 or y == y2:
                table[y][x] = lc
            else:
                table[y][x] = fc

def make_oval(x1, y1, x2, y2):
    global canv, table, rv, gv, bv, frv, fgv, fbv
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    r = eval(rv.get())
    g = eval(gv.get())
    b = eval(bv.get())
    color = rgb(r, g, b)
    fr = eval(frv.get())
    fg = eval(fgv.get())
    fb = eval(fbv.get())
    fill_color = rgb(fr, fg, fb)
    canv.create_oval(x1, y1, x2, y2, outline = color, fill = fill_color)
    lc = (r << 16) + (g << 8) + b
    fc = (fr << 16) + (fg << 8) + fb
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    a = (x2 - x1) / 2.0
    b = (y2 - y1) / 2.0
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            t = (x - cx) ** 2 / a ** 2 + (y - cy) ** 2 / b ** 2
            if t < 1:
                table[y][x] = fc
    for k in range(10000):
        theta = k / 10000.0 * math.pi * 2
        x = cx + a * math.cos(theta)
        x = int(round(x))
        y = cy + b * math.sin(theta)
        y = int(round(y))
        table[y][x] = lc

def flood_fill(x0, y0, r, g, b):
    global visited, queue
    visited = [[0 for col in range(802)] for row in range(602)]
    d = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    c0 = table[y0][x0]
    queue[0] = [x0, y0]
    p = 0
    q = 0
    count = 0
    while p <= q:
        for i in range(4):
            x = queue[p][0] + d[i][0]
            y = queue[p][1] + d[i][1]
            if x < 1 or x > 800 or y < 1 or y > 600 or visited[x][y] or table[y][x] != c0:
                continue
            visited[x][y] = 1
            q += 1
            queue[q][0] = x
            queue[q][1] = y
            put_pixel(x, y, r, g, b)
            count += 1
            if (count & 1023) == 0:
                canv.update()
        p += 1

def check_state(event):
    global v, state
    if v.get() != state:
        state = v.get()
        hx = []
        hy = []

def paint_start(event):
    x = event.x
    y = event.y
    global hx, hy, frv, fgv, fbv
    if v.get() == 1:
        hx = []
        hy = []
        hx.append(x)
        hy.append(y)
    elif v.get() == 2:
        hx = [x]
        hy = [y]
    elif v.get() == 3:
        hx.append(x)
        hy.append(y)
    elif v.get() == 4:
        hx = [x]
        hy = [y]
    elif v.get() == 5:
        hx = [x]
        hy = [y]
    elif v.get() == 6:
        r = eval(frv.get())
        g = eval(fgv.get())
        b = eval(fbv.get())
        flood_fill(x, y, r, g, b)

def paint_work(event):
    x = event.x
    y = event.y
    global hx, hy, canv, rv, gv, bv, frv, fgv, fbv
    if len(hx) == 0:
        return
    if v.get() == 1:
        make_line(hx[0], hy[0], x, y)
        hx[0] = x
        hy[0] = y
    elif v.get() == 2:
        r = eval(rv.get())
        g = eval(gv.get())
        b = eval(bv.get())
        color = rgb(r, g, b)
        canv.delete("tmp")
        canv.create_line(x, y, hx[0], hy[0], fill = color, tags = "tmp")
    elif v.get() == 3:
        r = eval(rv.get())
        g = eval(gv.get())
        b = eval(bv.get())
        color = rgb(r, g, b)
        canv.delete("tmp")
        if len(hx) == 1:
            hx.append(x)
            hy.append(y)
            canv.create_line(x, y, hx[0], hy[0], fill = color, tags = "tmp")
        else:
            n = len(hx)
            hx[n - 1] = x
            hy[n - 1] = y
            canv.create_line(x, y, hx[n - 2], hy[n - 2], fill = color, tags = "tmp")
    elif v.get() == 4:
        r = eval(rv.get())
        g = eval(gv.get())
        b = eval(bv.get())
        color = rgb(r, g, b)
        fr = eval(frv.get())
        fg = eval(fgv.get())
        fb = eval(fbv.get())
        fill_color = rgb(fr, fg, fb)
        canv.delete("tmp")
        canv.create_rectangle(x, y, hx[0], hy[0], outline = color, fill = fill_color, tags = "tmp")
    elif v.get() == 5:
        r = eval(rv.get())
        g = eval(gv.get())
        b = eval(bv.get())
        color = rgb(r, g, b)
        fr = eval(frv.get())
        fg = eval(fgv.get())
        fb = eval(fbv.get())
        fill_color = rgb(fr, fg, fb)
        canv.delete("tmp")
        canv.create_oval(x, y, hx[0], hy[0], outline = color, fill = fill_color, tags = "tmp")

def paint_end(event):
    x = event.x
    y = event.y
    global hx, hy
    if len(hx) == 0:
        return
    if v.get() == 1:
        make_line(hx[0], hy[0], x, y)
        hx = []
        hy = []
    elif v.get() == 2:
        canv.delete("tmp")
        make_line(hx[0], hy[0], x, y)
        hx = []
        hy = []
    elif v.get() == 3:
        canv.delete("tmp")
        n = len(hx)
        if n < 2:
            hx = []
            hy = []
            return
        make_line(hx[n - 1], hy[n - 1], hx[n - 2], hy[n - 2])
    elif v.get() == 4:
        canv.delete("tmp")
        if x == hx[0] or y == hy[0]:
            make_line(hx[0], hy[0], x, y)
        else:
            make_rectangle(hx[0], hy[0], x, y)
        hx = []
        hy = []
    elif v.get() == 5:
        canv.delete("tmp")
        if x == hx[0] or y == hy[0]:
            make_line(hx[0], hy[0], x, y)
        else:
            make_oval(hx[0], hy[0], x, y)
        hx = []
        hy = []

def poly_end(event):
    global v
    if v.get() != 3:
        return
    global hx, hy
    n = len(hx)
    if n > 1:
        make_line(hx[0], hy[0], hx[n - 1], hy[n - 1])
    hx = []
    hy = []

def main():
    global root
    menu = pack_menu_list()
    tool = pack_tool_list()
    global v, rv, gv, bv
    color_table = Frame(tool, width = 90, height = 100, bd = 4, relief = "groove")
    color_table.pack()
    Label(color_table, text = "==Line color config==\nred value:").pack()
    Entry(color_table, textvariable = rv).pack()
    Label(color_table, text = "green value:").pack()
    Entry(color_table, textvariable = gv).pack()
    Label(color_table, text = "blue value:").pack()
    Entry(color_table, textvariable = bv).pack()
    
    global frv, fgv, fbv
    fill_table = Frame(tool, width = 90, height = 100, bd = 4, relief = "groove")
    fill_table.pack()
    Label(fill_table, text = "==Fill color config==\nred value:").pack()
    Entry(fill_table, textvariable = frv).pack()
    Label(fill_table, text = "green value:").pack()
    Entry(fill_table, textvariable = fgv).pack()
    Label(fill_table, text = "blue value:").pack()
    Entry(fill_table, textvariable = fbv).pack()
    
    global canv
    canv = pack_main_table()
    model = Frame(tool, width = 90, height = 100, bd = 4, relief = "groove")
    model.pack()
    Radiobutton(model, text = "Pencil", variable = v, value = 1).grid(sticky = W)
    Radiobutton(model, text = "Line", variable = v, value = 2).grid(sticky = W)
    Radiobutton(model, text = "Polygon", variable = v, value = 3).grid(sticky = W)
    Radiobutton(model, text = "Rectangle", variable = v, value = 4).grid(sticky = W)
    Radiobutton(model, text = "Oval", variable = v, value = 5).grid(sticky = W)
    Radiobutton(model, text = "Filler", variable = v, value = 6).grid(sticky = W)
    Button(tool, text = "Clear", command = clear_screen).pack()
    Button(tool, text = "Quit", command = end).pack()
    tool.update()
    tool.bind("<Leave>",check_state)
    canv.bind("<Button-1>", paint_start)
    canv.bind("<B1-Motion>", paint_work)
    canv.bind("<ButtonRelease-1>", paint_end)
    canv.bind("<Double-Button-1>", poly_end)
    root.mainloop()

main()
