import numpy as np
from PIL import Image


def hello():
    print("hello world")

def clip(integer):
    if (integer > 255):
        integer = 255
    if (integer < 0):
        integer = 0
    return integer

def convert_binary(img_array):
    height, width = img_array.shape
    for i in range(height):
        for j in range(width):
            if (img_array[i, j] < 125):
                img_array[i, j] = 0
            else:
                img_array[i, j] = 255
    return img_array

def binary(integer):
    if integer == 255:
        return 1
    elif integer == 0:
        return 0
    else:
        return -1

def array_span(array, h, w):
    height, width, channel = array.shape
    # print(height, width, channel)
    new_array = np.zeros((int(height+(h - 1)*2), int(width+(w - 1)*2), 3))
    # print(new_array.shape)
    for x in range(height):
        for y in range(width):
            new_array[x+(h-1), y+(w-1)] = array[x, y]
    return new_array

def array_span_binary(array, h, w):
    height, width = array.shape
    # print(height, width)
    new_array = np.zeros((int(height+(h - 1)*2), int(width+(w - 1)*2)))
    # print(new_array.shape)
    for x in range(height):
        for y in range(width):
            new_array[x+(h-1), y+(w-1)] = array[x, y]
    return new_array


def reverse(kernel):
    h, w = kernel.shape
    kernel_reverse = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            kernel_reverse[h-i-1, w-j-1] = kernel[i, j]
    return kernel_reverse
    

def morphological_edge_detection(img, se, center):
    print("morphological edge detection")
    img_array = np.array(img)
    height, width, channel = img_array.shape
    # print(height, width, channel)
    new_image = np.zeros((height, width,channel))
    h, w = se.shape
    # print(h,w)

    new_array = array_span(img_array, h, w)
    # print(new_array.shape)
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(new_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                        erosion_result.append(int(new_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                dilation_max = max(dilation_result)
                erosion_max = min(erosion_result)
                new_image[i, j, c] = clip(dilation_max - erosion_max)
    return new_image



def conditional_dilation_binary(img, se, center):
    print("conditional dilation binary")
    img_array = np.array(img)
    img_array = convert_binary(img_array)
    height, width = img_array.shape
    print(img_array.shape)
    new_image = np.zeros((height, width))
    h, w = se.shape
    print(h, w)
    new_array = array_span_binary(img_array, h, w)
    iteral_array = new_array.copy()
    last_array = iteral_array.copy()
    # ultimate erosion
    # while(iteral_array.any()):
    #     print("x")
    #     last_array = iteral_array.copy()
    #     current_array = iteral_array.copy()
    #     for i in range(height):
    #         for j in range(width):
    #             x = i + (h - 1)
    #             y = j + (w - 1)
    #             equal_flag = 1
    #             for a in range(h):
    #                 for b in range(w):
    #                     if (binary(iteral_array[int(x+(a-center[0])), int(y+(b-center[1]))]) != se[a, b]):
    #                         equal_flag = 0
    #                         break
    #                 if (equal_flag == 0):
    #                     break
    #             if (equal_flag == 1):
    #                 current_array[x, y] = 255
    #             else:
    #                 current_array[x, y] = 0
    #     iteral_array = current_array.copy()

    # opening
    erosion_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            equal_flag = 1
            for a in range(h):
                for b in range(w):
                    if (binary(iteral_array[int(x+(a-center[0])), int(y+(b-center[1]))]) != se[a, b]):
                        equal_flag = 0
                        break
                if (equal_flag == 0):
                    break
            if (equal_flag == 1):
                    erosion_array[x, y] = 255
            else:
                erosion_array[x, y] = 0
    opening_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            flag = 0
            for a in range(h):
                for b in range(w):
                    if (binary(erosion_array[int(x-(a-center[0])), int(y-(b-center[1]))]) == se[a, b] and se[a, b] == 1):
                        flag = 1
                        break
                if (flag == 1):
                    break
            if (flag == 1 and new_array[x, y] == 255):
                opening_array[x, y] = 255
            else:
                opening_array[x, y] = 0

    # conditional dilation
    iteral_array = opening_array.copy()
    last_array = np.zeros((iteral_array.shape))
    while (not (iteral_array==last_array).all()):
        print("y")
        last_array = iteral_array.copy()
        current_array = iteral_array.copy()
        for i in range(height):
            for j in range(width):
                x = i + (h - 1)
                y = j + (w - 1)
                flag = 0
                for a in range(h):
                    for b in range(w):
                        if (binary(iteral_array[int(x-(a-center[0])), int(y-(b-center[1]))]) == se[a, b] and se[a, b] == 1):
                            flag = 1
                            break
                    if (flag == 1):
                        break
                if (flag == 1 and new_array[x, y] == 255):
                    current_array[x, y] = 255
                else:
                    current_array[x, y] = 0
        iteral_array = current_array.copy()
    
    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            new_image[i, j] = last_array[x, y]
    print("end")
    return new_image


def OBR(img, se, center):
    print("gray scale reconstruction")

    img_array = np.array(img)
    height, width, channel = img_array.shape
    # print(height, width, channel)
    new_image = np.zeros((height, width,channel))
    h, w = se.shape
    # print(size)

    new_array = array_span(img_array, h, w)
    erosion_array = new_array.copy()
    # print(new_array.shape)
    # opening
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        erosion_result.append(int(new_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                erosion_min = min(erosion_result)
                erosion_array[x, y, c] = clip(int(erosion_min))
    opening_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(erosion_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                dilation_max = max(dilation_result)
                opening_array[x, y, c] = clip(int(dilation_max))
    # reconstructe
    iteral_array = opening_array.copy()
    last_array = np.zeros((iteral_array.shape))
    while (not (iteral_array == last_array).all()):
        print("y")
        last_array = iteral_array.copy()
        current_array = iteral_array.copy()
        for i in range(height):
            for j in range(width):
                for c in range(channel):
                    x = i + (h - 1)
                    y = j + (w - 1)
                    dilation_result = []
                    for a in range(h):
                        for b in range(w):
                            dilation_result.append(int(iteral_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                    dilation_max = max(dilation_result)
                    if (clip(int(dilation_max)) <= new_array[x, y, c]):
                        current_array[x, y, c] = clip(int(dilation_max))
        iteral_array = current_array.copy()

    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            new_image[i, j] = last_array[x, y]
    print("end")
    return new_image

def CBR(img, se, center):
    print("CBR")
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    h, w = se.shape

    new_array = array_span(img_array, h, w)
    dilation_array = new_array.copy()
    # closing
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(new_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                dilation_max = max(dilation_result)
                dilation_array[x, y, c] = clip(int(dilation_max))
    closing_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        erosion_result.append(int(dilation_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                erosion_min = min(erosion_result)
                closing_array[x, y, c] = clip(int(erosion_min))
    # reconstructe
    iteral_array = closing_array.copy()
    last_array = np.zeros((iteral_array.shape))
    while (not (iteral_array == last_array).all()):
        print("y")
        last_array = iteral_array.copy()
        current_array = iteral_array.copy()
        for i in range(height):
            for j in range(width):
                for c in range(channel):
                    x = i + (h - 1)
                    y = j + (w - 1)
                    dilation_result = []
                    for a in range(h):
                        for b in range(w):
                            dilation_result.append(int(iteral_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                    dilation_max = max(dilation_result)
                    if (clip(int(dilation_max)) <= new_array[x, y, c]):
                        current_array[x, y, c] = clip(int(dilation_max))
        iteral_array = current_array.copy()

    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            new_image[i, j] = last_array[x, y]
    print("end")
    return new_image

def geodesic_dilation_reconstruction(img, se, center):
    print("geodesic dilation reconstruction")
    img_array = np.array(img)
    height, width, channel = img_array.shape
    # print(height, width, channel)
    new_image = np.zeros((height, width,channel))
    h, w = se.shape
    # print(size)

    new_array = array_span(img_array, h, w)
    erosion_array = new_array.copy()
    # print(new_array.shape)
    # opening
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        erosion_result.append(int(new_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                erosion_min = min(erosion_result)
                erosion_array[x, y, c] = clip(int(erosion_min))
    opening_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(erosion_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                dilation_max = max(dilation_result)
                opening_array[x, y, c] = clip(max(int(dilation_max), new_array[x, y, c]))
    # reconstructe
    iteral_array = opening_array.copy()
    last_array = np.zeros((iteral_array.shape))
    while (not (iteral_array == last_array).all()):
        print("y")
        last_array = iteral_array.copy()
        current_array = iteral_array.copy()
        for i in range(height):
            for j in range(width):
                for c in range(channel):
                    x = i + (h - 1)
                    y = j + (w - 1)
                    dilation_result = []
                    for a in range(h):
                        for b in range(w):
                            dilation_result.append(int(iteral_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                    dilation_max = max(dilation_result)
                    if (clip(int(dilation_max)) <= new_array[x, y, c]):
                        current_array[x, y, c] = clip(int(dilation_max))
        iteral_array = current_array.copy()

    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            new_image[i, j] = last_array[x, y]
    print("end")
    return new_image


def geodesic_erosion_reconstruction(img, se, center):
    print("geodesic erosion reconstruction")
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    h, w = se.shape

    new_array = array_span(img_array, h, w)
    dilation_array = new_array.copy()
    # closing
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(new_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                dilation_max = max(dilation_result)
                dilation_array[x, y, c] = clip(int(dilation_max))
    closing_array = new_array.copy()
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        erosion_result.append(int(dilation_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                erosion_min = min(erosion_result)
                closing_array[x, y, c] = clip(min(int(erosion_min), new_array[x, y, c]))
    # reconstructe
    iteral_array = closing_array.copy()
    last_array = np.zeros((iteral_array.shape))
    while (not (iteral_array == last_array).all()):
        print("y")
        last_array = iteral_array.copy()
        current_array = iteral_array.copy()
        for i in range(height):
            for j in range(width):
                for c in range(channel):
                    x = i + (h - 1)
                    y = j + (w - 1)
                    dilation_result = []
                    for a in range(h):
                        for b in range(w):
                            dilation_result.append(int(iteral_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                    dilation_max = max(dilation_result)
                    if (clip(int(dilation_max)) <= new_array[x, y, c]):
                        current_array[x, y, c] = clip(int(dilation_max))
        iteral_array = current_array.copy()

    for i in range(height):
        for j in range(width):
            x = i + (h - 1)
            y = j + (w - 1)
            new_image[i, j] = last_array[x, y]
    print("end")
    return new_image


def morphological_gradient(img, se, center):
    print("morphological gradient")
    img_array = np.array(img)
    height, width, channel = img_array.shape
    # print(height, width, channel)
    new_image = np.zeros((height, width,channel))
    h, w = se.shape
    # print(h,w)

    new_array = array_span(img_array, h, w)
    # print(new_array.shape)
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + (h - 1)
                y = j + (w - 1)
                dilation_result = []
                erosion_result = []
                for a in range(h):
                    for b in range(w):
                        dilation_result.append(int(new_array[int(x-(a-center[0])), int(y-(b-center[1])), c]) + int(se[a, b]))
                        erosion_result.append(int(new_array[int(x+(a-center[0])), int(y+(b-center[1])), c]) - int(se[a, b]))
                dilation_max = max(dilation_result)
                erosion_max = min(erosion_result)
                new_image[i, j, c] = clip(int(0.5 * (dilation_max - erosion_max)))
    return new_image