import tkinter as tk


window = tk.Tk()
window.title("Image Watermarking Desktop Application")
window.columnconfigure(0, minsize=300, weight=50)
window.columnconfigure(1, minsize=50, weight=1)
window.rowconfigure(0, minsize=300, weight=1)

lbl_image = tk.Label(window, text="There will be an image.", width=100, relief=tk.SUNKEN)
lbl_image.grid(row=0, column=0, sticky="nsew")

frm_options = tk.Frame(window, borderwidth=3)
frm_options.grid(row=0, column=1, sticky="N", padx=3, pady=3)
buttons_names = ["Read Image", "Read Mark", "Save", "Size", "Set-X", "Set-Y", "Save"]
buttons = {}
# frm_options.rowconfigure(, minsize=25, weight=1)
frm_options.columnconfigure(0, minsize=80, weight=1)
for idx, button in enumerate(buttons_names):
    buttons[button] = tk.Button(frm_options, text=button, width=12)
    buttons[button].grid(row=idx, column=0)
    frm_options.rowconfigure(idx, minsize=25, weight=1)


window.mainloop()
