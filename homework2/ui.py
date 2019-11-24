import os
import re
import algorithm
import numpy as np
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
    input_prompt = Label(root, text="   ", fg="red")
    center_prompt = Label(root, text="   ", fg="red")
    result_label = Label(root)
    img_path = StringVar("")
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

    def get_se():
        se = entry_string.get()
        print(se)
        try:
            se_2d = eval(se)
        except:
            input_prompt["text"] = "invalid input"
            return None

        input_prompt["text"] = "   "
        print(se_2d)
        height = len(se_2d)
        width = len(se_2d[0])
        print(height, width)
        new_se = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                new_se[i, j] = se_2d[i][j]
        return new_se

    def get_center():
        center = center_string.get()
        print(center)
        try:
            center = eval(center)
        except:
            center_prompt["text"] = "invalid input"
            return None
        if (type(center) != list):
            center_prompt["text"] = "invalid input"
            return None
        if (len(center) != 2):
            center_prompt["text"] = "invalid input"
            return None

        center_prompt["text"] = "   "
        new_center = np.zeros((2))
        new_center[0] = center[0]
        new_center[1] = center[1]
        print(new_center)
        return new_center

    def morph_edge_detect():
        print("morphological edge detection:")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.morphological_edge_detection(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget


    def cond_dilation_click():
        print("Conditional dilation in binary image")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("L")
        except:
            img_prompt["text"] = "please choose a file"
            return
        
        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.conditional_dilation_binary(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget
        

    def OBR_click():
        print("OBR")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return

        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.OBR(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def CBR_click():
        print("CBR")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return

        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.CBR(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def geodesic_dilation_click():
        print("geodesic dilation click")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return

        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.geodesic_dilation_reconstruction(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget

    def geodesic_erosion_click():
        print("geodesic erosion click")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return

        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.geodesic_erosion_reconstruction(img, se, center)
        global result
        result = Image.fromarray(img_array.astype('uint8'))
        result_widget = get_image_widget(result, img_width, img_height)
        result_label.config(image=result_widget)
        result_label.image = result_widget
    
    def morph_grad_click():
        print("Morphological gradient")
        path = img_path.get()
        try:
            img = Image.open(path)
            img = img.convert("RGB")
        except:
            img_prompt["text"] = "please choose a file"
            return

        se = get_se()
        if (not se.any()):
            return

        center = get_center()
        if (center is None):
            return

        h, w = se.shape
        if (h <= center[0] or w <= center[1]):
            center_prompt["text"] = "center out of range"
            return
        
        img_array = algorithm.morphological_gradient(img, se, center)
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
    img_label.grid(row=0, column=0, columnspan=2)
    result_label.grid(row=0, column=2, columnspan=2)

    # row 1
    choose_button = Button(root, text="choose file", relief=GROOVE, command=choose_image).grid(row=1, column=0, columnspan=4)

    # row 2
    img_prompt.grid(row=2, column=0, columnspan=4)

    # row 3
    se_label = Label(root, text="costomized SE:").grid(row=3, column=0)
    entry_string = StringVar()
    se_entry = Entry(root, textvariable=entry_string).grid(row=3, column=1)
    entry_string.set("[[1, 1, 1], [1, 1, 1], [1, 1, 1]]")
    center_label = Label(root, text="center:").grid(row=3, column=2)
    center_string = StringVar()
    center_entry = Entry(root, textvariable=center_string).grid(row=3, column=3)
    center_string.set("[0, 0]")

    # row 4
    input_prompt.grid(row=4, column=0, columnspan=2)
    center_prompt.grid(row=4, column=2, columnspan=2)
    
    # row 5
    edge_label = Label(root, text="Morphological edge detection: ").grid(row=5, column=0)
    edge_button = Button(root, text="Generate", relief=GROOVE, command=morph_edge_detect).grid(row=5, column=1)


    # row 6
    recon_label = Label(root, text="Morphological Reconstruction: ").grid(row=6, column=0)
    dilation_button = Button(root, text="Conditional dilation in binary image", relief=GROOVE, command=cond_dilation_click).grid(row=6, column=1)
    grad_button = Button(root, text="Morphological gradient", relief=GROOVE, command=morph_grad_click).grid(row=6, column=3)

    # row 7
    gray_recon_label = Label(root, text="Grayscale Reconstruction: ").grid(row=7, column=0)
    recons_button = Button(root, text="geodesic dilation", relief=GROOVE, command=geodesic_dilation_click).grid(row=7, column=1)
    recons_button = Button(root, text="geodesic erosion", relief=GROOVE, command=geodesic_erosion_click).grid(row=7, column=2)
    recons_button = Button(root, text="OBR", relief=GROOVE, command=OBR_click).grid(row=7, column=3)
    recons_button = Button(root, text="CBR", relief=GROOVE, command=CBR_click).grid(row=7, column=4)

    # row 8
    save_button = Button(root, text="save file", relief=GROOVE, command=save_image).grid(row=8, column=0, columnspan=4)
    save_label.grid(row=8, column=0, columnspan=4)

    root.mainloop()


if __name__ == '__main__':
    main()

