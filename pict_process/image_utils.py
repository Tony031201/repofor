#!/usr/bin/python3
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
from tkinter import filedialog
import pytesseract

# 初始化裁剪的起始点和结束点
crop_start = None
crop_end = None
rectangle = None

# 图片和尺寸
original_image = None
pil_image = None
old_size = None
canvas_width = None
canvas_height = None
tk_cropped_image = None
FILE = None

# 操作之前的图像状态
last_image_state = None

def on_mouse_down(event):
    global crop_start
    crop_start = (event.x,event.y)

def on_mouse_move(event,canvas):
    global crop_start, crop_end, rectangle
    if crop_start:
        crop_end = (event.x, event.y)
        if not rectangle:
            rectangle = canvas.create_rectangle(crop_start + crop_end, outline='red')
        else:
            canvas.coords(rectangle, crop_start + crop_end)

def on_mouse_up(event,canvas):
    global crop_start, crop_end, rectangle, last_image_state
    # 更新裁剪区域的结束点
    if crop_start:
        crop_end = (event.x,event.y)

def load_image(canvas, button_crop):
    global original_image, old_size, canvas_width, canvas_height, last_image_state, rectangle, crop_end, crop_start, FILE

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=(("JPEG files", "*.jpg;*.jpeg;*.JPG;*.JPEG"), ("PNG files", "*.png"), ("All files", "*.*"))
    )

    if not file_path:
        return

    canvas.image_path = file_path
    FILE = file_path
    image = Image.open(file_path)
    orig_width, orig_height = image.size
    ratio = min(canvas_width / orig_width, canvas_height / orig_height)
    new_size = (int(orig_width * ratio), int(orig_height * ratio))
    old_size = new_size

    image = image.resize(new_size)
    tk_image = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.image = tk_image

    original_image = image  # Save the original PIL image, not the Tk one.
    last_image_state = image.copy()

    button_crop['state'] = 'normal'

    # 重置全局
    crop_start = None
    crop_end = None
    if rectangle:
        canvas.delete(rectangle)
        rectangle = None


def back_track(canvas):
    global original_image, crop_end, crop_start, rectangle, old_size, canvas_height, canvas_width, FILE, last_image_state, canvas_height, canvas_width

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    image = Image.open(FILE)
    orig_width, orig_height = image.size
    ratio = min(canvas_width / orig_width, canvas_height / orig_height)
    new_size = (int(orig_width * ratio), int(orig_height * ratio))
    old_size = new_size

    image = image.resize(new_size)
    tk_image = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.image = tk_image

    original_image = image  # Save the original PIL image, not the Tk one.
    last_image_state = image.copy()


    # 重置全局
    crop_start = None
    crop_end = None
    if rectangle:
        canvas.delete(rectangle)
        rectangle = None

# crop modula
def start_crop(canvas):
    global crop_start, crop_end, rectangle, original_image, old_size, last_image_state, tk_cropped_image
    if not crop_start or not crop_end:
        return

    if original_image is None or not hasattr(canvas, 'image'):
        return

    last_image_state = original_image.copy()

    ratio = old_size[0] / original_image.width, old_size[1] / original_image.height
    real_crop_start = (int(crop_start[0] * ratio[0]), int(crop_start[1] * ratio[1]))
    real_crop_end = (int(crop_end[0] * ratio[0]), int(crop_end[1] * ratio[1]))
    crop_box = real_crop_start + real_crop_end

    # 裁剪图片
    cropped_image = original_image.crop(crop_box)
    new_size = (800, 600)
    resized_image = cropped_image.resize(new_size)

    canvas.delete("all")
    tk_cropped_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor="nw", image=tk_cropped_image)
    canvas.image = tk_cropped_image

    original_image = resized_image
    old_size = resized_image.size

    crop_start = None
    crop_end = None
    if rectangle:
        canvas.delete(rectangle)
        rectangle = None


def enhance_image(canvas, noise_reduction_factor=0.5, sharpness=1.2, brightness=1.1, contrast=1.05):
    global last_image_state
    # 检查 'original_image' 是否存在于全局变量中，并且是有效的Pillow Image对象
    if 'original_image' not in globals() or not isinstance(globals()['last_image_state'], Image.Image):
        print("No image to enhance.")
        return

    # 获取最后一次裁剪的图像状态
    image = globals()['original_image']
    last_image_state = image.copy()

    new_size = (800, 600)
    resized_image = image.resize(new_size)

    # 去噪点
    enhanced_image = resized_image.filter(ImageFilter.GaussianBlur(radius=noise_reduction_factor))

    # 使用Pillow的ImageEnhance来锐化图像
    enhanced_image = ImageEnhance.Sharpness(enhanced_image)
    enhanced_image = enhanced_image.enhance(sharpness)  # 可以调整这个值来设置锐化的程度

    # 增加清晰度
    enhanced_image = enhanced_image.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=3))

    # 调整亮度
    enhanced_image = ImageEnhance.Brightness(enhanced_image)
    enhanced_image = enhanced_image.enhance(brightness)

    # 调整对比度
    enhanced_image = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhanced_image.enhance(contrast)

    # 直方图均衡比
    enhanced_image = ImageOps.equalize(enhanced_image)

    # 将锐化后的图像转换为Tkinter可用的格式
    tk_enhanced_image = ImageTk.PhotoImage(enhanced_image)

    # 更新画布显示
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_enhanced_image)
    canvas.image = tk_enhanced_image  # 保存引用，防止Python垃圾回收机制删除它

    # 更新last_image_state为锐化后的图像，供后续操作使用
    globals()['original_image'] = enhanced_image


def extract_text_from_image():
    global last_image_state
    if 'original_image' not in globals() or not isinstance(globals()['last_image_state'], Image.Image):
        print("No image to extract.")
        return

    image = globals()['original_image']

    text = pytesseract.image_to_string(image, lang='eng')
    return text






