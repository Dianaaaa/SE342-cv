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

def array_span(array, size):
    height, width, channel = array.shape
    span_row = int(int(size) / 2)
    new_array = np.zeros((int(height+span_row*2), int(width+span_row*2), 3))
    for x in range(height):
        for y in range(width):
            new_array[x+span_row, y+span_row] = array[x, y]
    return new_array

def reverse(kernel):
    h, w = kernel.shape
    kernel_reverse = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            kernel_reverse[h-i-1, w-j-1] = kernel[i, j]
    return kernel_reverse
    

def roberts_convolution(img):
    roberts_x = np.array(([1, 0], [0, -1]))
    roberts_y = np.array(([0, 1], [-1, 0]))

    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    # print(new_image.shape)
    for x in range(height):
        for y in range(width):
            for c in range(channel):
                if (x == height-1):
                    if (y == width-1):
                        new_image[x, y, c] = clip(abs(img_array[x, y, c]))
                    else:
                        new_image[x, y, c] = clip(int(abs(img_array[x, y, c])) + int(abs(img_array[x, y+1, c])))
                else:
                    if (y == width-1):
                        new_image[x, y, c] = clip(int(abs(img_array[x, y, c])) + int(abs(img_array[x+1, y, c])))
                    else:
                        try:
                            new_image[x, y, c] = clip(abs(int(img_array[x, y, c]) - int(img_array[x+1, y+1, c])) + abs(int(img_array[x, y+1, c]) - int(img_array[x+1, y, c])))
                        except:
                            print(x, y, c)
                            return
    # print(new_image)
    return new_image




def prewitt_convolution(img):
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    for x in range(height):
        for y in range(width):
            for c in range(channel):
                if (x == 0):
                    if (y == 0):
                        gx = int(img_array[x, y+1, c]) + int(img_array[x+1, y+1, c])
                        gy = -int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        gy = -int(img_array[x+1, y-1, c]) - int(img_array[x+1, y, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -int(img_array[x, y-1, c]) + int(img_array[x, y+1, c]) - int(img_array[x+1, y-1, c]) + int(img_array[x+1, y+1, c])
                        gy = -int(img_array[x+1, y-1, c]) - int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                elif (x == height-1):
                    if (y == 0):
                        gx = int(img_array[x-1, y+1, c]) + int(img_array[x, y+1, c])
                        gy = int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -int(img_array[x-1, y-1, c]) - int(img_array[x, y-1, c])
                        gy = int(img_array[x-1, y-1, c]) + int(img_array[x-1, y, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -int(img_array[x-1, y-1, c]) + int(img_array[x-1, y+1, c]) - int(img_array[x, y-1, c]) + int(img_array[x, y+1, c])
                        gy = int(img_array[x-1, y-1, c]) + int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                else:
                    if (y == 0):
                        gx = int(img_array[x-1, y+1, c]) +  int(img_array[x, y+1, c]) + int(img_array[x+1, y+1, c])
                        gy = int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c]) - int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -int(img_array[x-1, y-1, c]) - int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        gy = int(img_array[x-1, y-1, c]) + int(img_array[x-1, y, c]) - int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -int(img_array[x-1, y-1, c]) + int(img_array[x-1, y+1, c]) - int(img_array[x, y-1, c]) + int(img_array[x, y+1, c]) - int(img_array[x+1, y-1, c]) + int(img_array[x+1, y+1, c])
                        gy = int(img_array[x-1, y-1, c]) + int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c]) - int(img_array[x+1, y-1, c]) - int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
    return new_image





def sobel_convolution(img):
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    for x in range(height):
        for y in range(width):
            for c in range(channel):
                if (x == 0):
                    if (y == 0):
                        gx = 2*int(img_array[x, y+1, c]) + int(img_array[x+1, y+1, c])
                        gy = -2*int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -2*int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        gy = -int(img_array[x+1, y-1, c]) - 2*int(img_array[x+1, y, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -2*int(img_array[x, y-1, c]) + 2*int(img_array[x, y+1, c]) - int(img_array[x+1, y-1, c]) + int(img_array[x+1, y+1, c])
                        gy = -int(img_array[x+1, y-1, c]) - 2*int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                elif (x == height-1):
                    if (y == 0):
                        gx = int(img_array[x-1, y+1, c]) + 2*int(img_array[x, y+1, c])
                        gy = 2*int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -int(img_array[x-1, y-1, c]) - 2*int(img_array[x, y-1, c])
                        gy = int(img_array[x-1, y-1, c]) + 2*int(img_array[x-1, y, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -int(img_array[x-1, y-1, c]) + int(img_array[x-1, y+1, c]) - 2*int(img_array[x, y-1, c]) + 2*int(img_array[x, y+1, c])
                        gy = int(img_array[x-1, y-1, c]) + 2*int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                else:
                    if (y == 0):
                        gx = int(img_array[x-1, y+1, c]) +  2*int(img_array[x, y+1, c]) + int(img_array[x+1, y+1, c])
                        gy = 2*int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c]) - 2*int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    elif (y == width-1):
                        gx = -int(img_array[x-1, y-1, c]) - 2*int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        gy = int(img_array[x-1, y-1, c]) + 2*int(img_array[x-1, y, c]) - 2*int(img_array[x, y-1, c]) - int(img_array[x+1, y-1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
                    else:
                        gx = -int(img_array[x-1, y-1, c]) + int(img_array[x-1, y+1, c]) - 2*int(img_array[x, y-1, c]) + 2*int(img_array[x, y+1, c]) - int(img_array[x+1, y-1, c]) + int(img_array[x+1, y+1, c])
                        gy = int(img_array[x-1, y-1, c]) + 2*int(img_array[x-1, y, c]) + int(img_array[x-1, y+1, c]) - int(img_array[x+1, y-1, c]) - 2*int(img_array[x+1, y, c]) - int(img_array[x+1, y+1, c])
                        new_image[x, y, c] = clip(abs(gx) + abs(gy))
    return new_image

def get_gaussian_kernel(size, sigma):
    kernel = np.zeros((size, size))
    center = size / 2
    if sigma <= 0:
        sigma = ((size - 1) * 0.5 - 1) * 0.3 + 0.8
    sigma2 = sigma**2
    total = 0
    pi = 3.1415926
    for i in range(size):
        for j in range(size):
            x = i - center
            y = j - center
            cal =  (1/(2*pi*sigma*sigma)) * np.exp(-(x*x + y*y) / (2*sigma*sigma))
            kernel[i, j] = cal
            total += cal
    for i in range(size):
        for j in range(size):
            kernel[i, j] = kernel[i, j] / total
    return kernel


def gaussian_filter(img, size, sigma):
    img_array = np.array(img)
    height, width, channel = img_array.shape
    # print(height, width, channel)
    new_image = np.zeros((height, width,channel))

    kernel = get_gaussian_kernel(size, sigma)
    # print(kernel)
    kernel = reverse(kernel)
    # print(kernel_reverse)

    new_array = array_span(img_array, size)
    # print(new_array.shape)
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + int(size / 2)
                y = j + int(size / 2)
                result = 0
                for a in range(size):
                    for b in range(size):
                        result += kernel[a, b] * new_array[x-int(size/2)+b, y-int(size/2)+b, c]
                new_image[i, j, c] = clip(int(result))
    return new_image



def mean_filter(img, size):
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    new_array = array_span(img_array, size)
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + int(size / 2)
                y = j + int(size / 2)
                result = 0
                for a in range(size):
                    for b in range(size):
                        result += new_array[x-int(size/2)+b, y-int(size/2)+b, c]
                new_image[i, j, c] = clip(int(result / (size * size)))
    return new_image


def median_filter(img, size):
    img_array = np.array(img)
    height, width, channel = img_array.shape
    new_image = np.zeros((height, width,channel))
    new_array = array_span(img_array, size)
    for i in range(height):
        for j in range(width):
            for c in range(channel):
                x = i + int(size // 2)
                y = j + int(size // 2)
                nums = []
                for a in range(size):
                    for b in range(size):
                        nums.append(new_array[x-int(size//2)+b, y-int(size//2)+b, c])
                new_image[i, j, c] = clip(int(np.median(nums)))
    return new_image