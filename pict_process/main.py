#!/usr/bin/python3
# main.py

import tkinter as tk
from image_utils import load_image, start_crop, back_track, enhance_image  # 导入load_image中的加载函数
from image_utils import on_mouse_up, on_mouse_down, on_mouse_move # 导入鼠标相关函数

# 创建主窗口
root = tk.Tk()

#创建画布
canvas = tk.Canvas(root, width="1200", height="800")
canvas.pack()

# 绑定鼠标
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>",lambda event: on_mouse_move(event, canvas))
canvas.bind("<ButtonRelease-1>",lambda event: on_mouse_up(event,canvas))

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

# 创建按钮，点击会调用加载函数
button_load = tk.Button(root, text="Load Image", command=lambda: load_image(canvas,button_crop))
button_load.pack(side=tk.LEFT, padx=2)

button_load = tk.Button(root, text="reset", command=lambda: back_track(canvas))
button_load.pack(side=tk.LEFT, padx=2)

button_crop = tk.Button(root,text="Crop Image",state='disabled',command=lambda: start_crop(canvas))
button_crop.pack(side=tk.LEFT, padx=2)

enhance_button = tk.Button(root, text="Enhance Image", command=lambda: enhance_image(canvas))
enhance_button.pack(side=tk.LEFT, padx=2)

root.mainloop()

