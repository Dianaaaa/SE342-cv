import os
import re
import algorithm
from tkinter import *
from tkinter.filedialog import *
from PIL import Image,ImageTk

# resize a image to fit the window
def resize(box_w, box_h, pil_img):
    w,h = pil_img.size
    f1 = 1.0*box_w/w
    f2 = 1.0*box_h/h
    f = min(f1, f2)
    width = int(w * f)
    height = int(h * f)
    return pil_img.resize((width, height), Image.ANTIALIAS)


def main():
    img_width = 500
    img_height = 300

    root = Tk()
    root.title("filters")
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    img_label = Label(root)
    img_prompt = Label(root, text="   ", fg="red")
    result_label = Label(root)
    img_path = StringVar("")
    confirm_label = Label(root, text="   ")
    result = ""
    save_label = Label(root, text="  ", fg="red")
    
    

    def get_image_widget(img, box_w, box_h):
        resized_img = resize(box_w, box_h, img)
        img_widget = ImageTk.PhotoImage(resized_img)
        return img_widget

    def choose_image():
        default_dir = r"文件路径"
        file_path = askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
        print("file_path", file_path)
        img_path.set(file_path)
        # img = get_resized_image(file_path, img_width, img_height)
        try:
            img = Image.open(file_path)
        except:
            img_prompt["text"] = "please choose jpg/jpeg or png files"
            return
        img_prompt["text"] = "    "
        img_widget = get_image_widget(img, img_width, img_height)
        img_label.config(image=img_widget)
        img_label.image = img_widget

    
    def get_kernel():
        size = entry_string.get()
        # print(size)
    
    def roberts_convolution_click():
        print("roberts")
        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        img_array = algorithm.roberts_convolution(img)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget
    
    def prewitt_convolution_click():
        print("prewitt")
        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        img_array = algorithm.prewitt_convolution(img)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def sobel_convolution_click():
        print("sobel")
        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        img_array = algorithm.sobel_convolution(img)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget
    
    def gaussian_filter_click():
        print("gaussian filter")
        size = entry_string.get()
        if (not size.isdigit()):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return
        if (eval(size) % 2 == 0):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return
        
        sigma = sigma_string.get()
        value = re.compile(r'^[0-9]+(\.[0-9]+)?$')
        if (not value.match(sigma)):
            confirm_label["text"] = "sigma should be a double"
            confirm_label["fg"] = "red"
            return

        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return

        confirm_label["text"] = "kernel size: " + size + ", sigma: " + sigma
        confirm_label["fg"] = "black"
        # print(size, sigma)

        img_array = algorithm.gaussian_filter(img, eval(size), eval(sigma))
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def mean_filter_click():
        print("mean filter")
        size = entry_string.get()
        if (not size.isdigit()):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return
        if (eval(size) % 2 == 0):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return

        confirm_label["text"] = "kernel size: " + size
        confirm_label["fg"] = "black"

        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return
        # print(size)

        img_array = algorithm.mean_filter(img, eval(size))
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def median_filter_click():
        print("median filter")
        size = entry_string.get()
        if (not size.isdigit()):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return
        if (eval(size) % 2 == 0):
            confirm_label["text"] = "size should be an odd"
            confirm_label["fg"] = "red"
            return
        confirm_label["text"] = "kernel size: " + size
        confirm_label["fg"] = "black"

        path = img_path.get()
        try:
            img = Image.open(path)
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        img_array = algorithm.median_filter(img, eval(size))
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def save_image():
        global result
        if result=="":
            save_label["text"] = "no file need to save"
            return
        save_label["text"] = "  "
        fname = asksaveasfilename(title=u'保存文件', filetypes=[("PNG", ".png")])
        
        result.save(str(fname) + '.png', 'PNG')
        save_label["text"] = "save successfully"



    # row 0
    img_label.grid(row=0, column=0, columnspan=4)
    result_label.grid(row=0, column=4, columnspan=4)

    # row 1
    img_prompt.grid(row=1, column=0, columnspan=4)

    # row 2
    choose_button = Button(root, text="choose file", relief=GROOVE, command=choose_image).grid(row=2, column=0, columnspan=4)

    # row 3
    conv_label = Label(root, text="covolution: ").grid(row=3, column=0)
    roberts_button = Button(root, text="Roberts", relief=GROOVE, command=roberts_convolution_click).grid(row=3, column=1)
    prewitt_button = Button(root, text="Prewitt", relief=GROOVE, command=prewitt_convolution_click).grid(row=3, column=2)
    sobel_button = Button(root, text="Sobel", relief=GROOVE, command=sobel_convolution_click).grid(row=3, column=3)

    # row 4
    size_label = Label(root, text="kernel size:").grid(row=4, column=0)
    entry_string = StringVar()
    size_entry = Entry(root, textvariable=entry_string).grid(row=4, column=1, columnspan=3)
    entry_string.set("input kernel size")
    sigma_string = StringVar()
    sigma_entry = Entry(root, text=sigma_string).grid(row=4, column=4)
    sigma_string.set("input sigma")

    # row 5
    confirm_label.grid(row=5, column=0, columnspan=4)

    # row 6
    filter_label = Label(root, text="filters: ").grid(row=6, column=0)
    gaussian_button = Button(root, text="Gaussian filter", relief=GROOVE, command=gaussian_filter_click).grid(row=6, column=1)
    mean_button = Button(root, text="Mean filter", relief=GROOVE, command=mean_filter_click).grid(row=6, column=2)
    median_button = Button(root, text="Median filter", relief=GROOVE, command=median_filter_click).grid(row=6, column=3)

    # row 7
    save_button = Button(root, text="save file", relief=GROOVE, command=save_image).grid(row=7, column=0, columnspan=4)
    save_label.grid(row=8, column=0, columnspan=4)

    root.mainloop()


if __name__ == '__main__':
    main()

