import tkinter as tk
from tkinter import filedialog, colorchooser

from PIL import Image, ImageTk, ImageFont, ImageDraw
from matplotlib import font_manager

image = None
ready_image = None
canvas_image = None
# default size of an image
image_size = (1000, 1000)

watermark_text_dict = {}

# find all fonts installed in your computer
system_fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
system_fonts = sorted(system_fonts)

# default font for watermark text
sys_text_font = system_fonts[10]

# default font size for watermark text
font_size = 10

# make a font for watermark text
text_font = ImageFont.truetype(sys_text_font, font_size)

# default watermark text cords: (x, y)
text_x_pos = 0
text_y_pos = 0

# default color for watermark text
text_color = (0, 0, 0)

text_opacity = 255

mark_text = "default text"

max_text_size = 200

text_width = 0
text_height = 0

text_center = []


def read_image():
    global image, image_size, text_center, text_y_pos, text_x_pos, text_width, text_height, canvas_image

    img_path = filedialog.askopenfilename()
    if img_path != "":
        with Image.open(img_path) as picture:
            image = picture.convert("RGBA")
            tk_image = ImageTk.PhotoImage(image)
            cnv_image.config(width=image.size[0], height=image.size[1])

            canvas_image = cnv_image.create_image(0, 0, anchor="nw", image=tk_image)
            image_size = image.size

            cnv_image.config(scrollregion=(0, 0, image_size[0], image_size[1]))
            y_scrollbar.config(command=cnv_image.yview)
            x_scrollbar.config(command=cnv_image.xview)
            cnv_image.config(
                xscrollcommand=x_scrollbar.set,
                yscrollcommand=y_scrollbar.set
            )

            enable_buttons()
            text_width, text_height = ImageDraw.Draw(image).textsize(mark_text, text_font)
            text_center = (image_size[0] / 2, image_size[1] / 2)

            text_x_pos = text_center[0] - text_width / 2
            text_y_pos = text_center[1] - text_height / 2

            from_height = 0 - image_size[1] / 2 - text_height / 2
            to_height = image_size[1] / 2 + text_height / 2
            scl_set_Y.config(from_=from_height, to=to_height)
            scl_set_Y.set(0)

            from_width = 0 - image_size[0] / 2 - text_width / 2
            to_width = image_size[0] / 2 + text_width / 2
            scl_set_X.config(from_=from_width, to=to_width)
            scl_set_X.set(0)

            scl_opacity.set(text_opacity)

            display_image()


def save_image():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        ready_image.save(save_path)


def enable_buttons():
    ent_set_text.config(state=tk.NORMAL)
    btn_change_color.config(state=tk.NORMAL)
    scl_size.config(state=tk.NORMAL)
    scl_set_X.config(state=tk.NORMAL)
    scl_set_Y.config(state=tk.NORMAL)
    scl_opacity.config(state=tk.NORMAL)
    btn_save_image.config(state=tk.NORMAL)


def set_watermark_font_size(*args):
    global font_size, text_font, text_width, text_height, text_x_pos, text_y_pos
    font_size = int(args[0])
    text_font = ImageFont.truetype(sys_text_font, font_size)
    text_width, text_height = ImageDraw.Draw(image).textsize(mark_text, text_font)
    text_x_pos = text_center[0] - text_width / 2
    text_y_pos = text_center[1] - text_height / 2

    from_height = 0 - image_size[1] / 2 - text_height / 2
    to_height = image_size[1] / 2 + text_height / 2
    scl_set_Y.config(from_=from_height, to=to_height)

    from_width = 0 - image_size[0] / 2 - text_width / 2
    to_width = image_size[0] / 2 + text_width / 2
    scl_set_X.config(from_=from_width, to=to_width)
    scl_opacity.set(text_opacity)

    display_image()


def set_watermark_x_pos(*args):
    global text_x_pos, text_center

    text_x_pos = int(args[0]) + image_size[0] / 2 - text_width / 2
    text_center = (text_x_pos + text_width / 2, text_y_pos + text_height / 2)

    display_image()


def set_watermark_y_pos(*args):
    global text_y_pos, text_center

    text_y_pos = int(args[0]) + image_size[1] / 2 - text_height / 2
    text_center = (text_x_pos + text_width / 2, text_y_pos + text_height / 2)

    display_image()


def set_watermark_text_color():
    global text_color

    text_color = colorchooser.askcolor()[0]

    display_image()


def set_watermark_opacity(*args):
    global text_opacity

    text_opacity = int(args[0])

    display_image()


def set_watermark_text(*args):
    global mark_text

    mark_text = ent_set_text.get()

    display_image()


def display_image():
    global ready_image
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", image_size, (255, 255, 255, 0))

    d = ImageDraw.Draw(txt)
    r, g, b = text_color
    r = int(r)
    g = int(g)
    b = int(b)

    d.text((text_x_pos, text_y_pos), mark_text,
           font=text_font, fill=(r, g, b, text_opacity))

    ready_image = Image.alpha_composite(image, txt)
    out = ImageTk.PhotoImage(ready_image)
    cnv_image.itemconfig(canvas_image, image=out)
    cnv_image.image = out


# set window
window = tk.Tk()
window.title("Image Watermarking Desktop Application")
window.columnconfigure(0, minsize=50, weight=50)
window.columnconfigure(1, minsize=100, weight=1)
window.rowconfigure(0, minsize=50, weight=1)

# image frame
frm_image = tk.Frame(master=window, bg='#4A7A8C')
frm_image.grid(row=0, column=0, sticky="nsew", )

# place for image
cnv_image = tk.Canvas(master=frm_image, relief=tk.SUNKEN,
                      borderwidth=4, scrollregion=(0, 0, 500, 500), )

# image scrollbars
x_scrollbar = tk.Scrollbar(master=frm_image, orient="horizontal", )
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

y_scrollbar = tk.Scrollbar(master=frm_image, orient="vertical", )
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

cnv_image.pack(expand=True, side=tk.LEFT, fill=tk.BOTH)

# options frame
frm_options = tk.Frame(master=window, borderwidth=3)
frm_options.grid(row=0, column=1, sticky="N", padx=3, pady=3)

# detekt changes in ent_set_text - place to set watermark text
watermark_text = tk.StringVar(master=frm_options)
watermark_text.trace("w", set_watermark_text)

# read image button
btn_read_image = tk.Button(frm_options, text="Read Image",
                           command=read_image, )
btn_read_image.grid(row=1, column=0, sticky="ew", padx=2, pady=2)

# read watermark text
ent_set_text = tk.Entry(frm_options, text="Set Text",
                        textvariable=watermark_text, state=tk.DISABLED)
ent_set_text.grid(row=2, column=0, sticky="ew", padx=2, pady=2, )

# change watermark text
btn_change_color = tk.Button(frm_options, text="Change Color",
                             command=set_watermark_text_color,
                             state=tk.DISABLED, )
btn_change_color.grid(row=3, column=0, sticky="ew", padx=2, pady=2, )

# change size of watermark text
scl_size = tk.Scale(master=frm_options, from_=10, to=max_text_size,
                    orient="horizontal", label="Size",
                    command=set_watermark_font_size, state=tk.DISABLED, )
scl_size.grid(row=4, column=0, sticky="ew", padx=2, pady=2, )

# set top left corner watermark text position
scl_set_X = tk.Scale(master=frm_options, from_=0, to=1000, orient="horizontal",
                     label="X pos", command=set_watermark_x_pos, state=tk.DISABLED, )
scl_set_X.grid(row=5, column=0, sticky="ew", padx=2, pady=2, )

# set top left corner watermark text position
scl_set_Y = tk.Scale(master=frm_options, from_=0, to=1000, orient="horizontal",
                     label="Y pos", command=set_watermark_y_pos, state=tk.DISABLED, )
scl_set_Y.grid(row=6, column=0, sticky="ew", padx=2, pady=2, )

# set opacity of watermark text
scl_opacity = tk.Scale(master=frm_options, from_=0, to=255, label="Opacity",
                       orient="horizontal", command=set_watermark_opacity, state=tk.DISABLED, )
scl_opacity.grid(row=7, column=0, sticky="ew", padx=2, pady=2, )

# save watermarked image to file
btn_save_image = tk.Button(master=frm_options, text="Save Image",
                           state=tk.DISABLED, command=save_image)
btn_save_image.grid(row=8, column=0, sticky="ew", padx=2, pady=2, )

window.mainloop()
