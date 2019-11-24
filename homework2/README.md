# How To Run

```
python ui.py
```

ui.py定义了ui的样式和行为，algorithm.py定义了算法逻辑。

# Morphological Edge Detection

![](./md_imgs/edge_result.png)

实现方法为，灰度膨胀结果减去灰度腐蚀结果

ps：jpg、png的彩色图片同样适用

# conditional dilation binary

![](./md_imgs/bi_recons_result.png)

![](./md_imgs/bi_recons_result2.png)

（输入图片预处理成二值图像）

实现方法为先对原图进行开操作，然后再conditional dilation

之前也尝试过ultimate erosion，效果一样，但速度太慢。

# Grayscale Reconstruction

- OBR

![](./md_imgs/OBR_result.png)



- CBR

![](./md_imgs/CBR_result.png)



- Geodesic dilation reconstruction

![](./md_imgs/geodesic_dilation_result.png)

- Geodesic erosion reconstruction

![](./md_imgs/geodesic_erosion_result.png)



此操作极其耗时，需要耐心等待。

（此操作支持彩色jpg、png图片）

# Morphological Gradient

![](./md_imgs/grad_result.png)

此操作与edge detection一致，不过最后要乘以一个0.5的系数