#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像基础：读取、显示、shape、dtype、BGR/RGB、灰度转换
对应教程：interest-learning/perception/python-vision-basics/01-图像与numpy数组.md
"""

import cv2
import numpy as np
import os


def create_test_image():
    """创建测试图片：上半部分红色，下半部分灰色"""
    # shape = (高, 宽, 通道) = (480, 640, 3)
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:, :] = (80, 80, 80)        # 整张图铺深灰 (B, G, R)
    img[0:240, :] = (0, 0, 255)     # 上半部分涂红（BGR 里第三个通道是红）
    cv2.imwrite("test.jpg", img)
    print("已生成测试图片 test.jpg")
    print(f"shape: {img.shape}, dtype: {img.dtype}")
    return img


def demo_basic_properties():
    """演示图像基本属性"""
    print("=" * 60)
    print("1. 图像基本属性")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    if img is None:
        print("读取失败，先运行 create_test_image()")
        return
    
    print(f"shape: {img.shape}")           # (480, 640, 3)
    print(f"  高度(行数): {img.shape[0]}")  # 480
    print(f"  宽度(列数): {img.shape[1]}")  # 640
    print(f"  通道数: {img.shape[2]}")      # 3
    print(f"dtype: {img.dtype}")           # uint8
    print(f"总元素数: {img.size}")         # 480*640*3 = 921600
    
    # 取中心像素的 BGR 值
    h, w = img.shape[:2]
    center_pixel = img[h // 2, w // 2]
    print(f"中心像素 BGR: {center_pixel}")  # 下半部分灰区，约 [80, 80, 80]


def demo_bgr_vs_rgb():
    """演示 BGR 与 RGB 的区别"""
    print("\n" + "=" * 60)
    print("2. BGR vs RGB")
    print("=" * 60)
    
    # 纯红色在 BGR 中是 [0, 0, 255]
    red_bgr = np.array([[[0, 0, 255]]], dtype=np.uint8)
    
    # 用 OpenCV 显示/保存：正确显示红色
    cv2.imwrite("red_bgr.jpg", red_bgr)
    
    # 转 RGB 给 matplotlib 用
    red_rgb = cv2.cvtColor(red_bgr, cv2.COLOR_BGR2RGB)
    print(f"BGR [0,0,255] -> RGB: {red_rgb.ravel()}")  # [255, 0, 0]
    
    # 错误示范：直接用 matplotlib 显示 BGR 图会导致红蓝互换
    # 正确做法：plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def demo_grayscale():
    """演示灰度转换"""
    print("\n" + "=" * 60)
    print("3. 彩色转灰度")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    print(f"彩色 shape: {img.shape}")   # (480, 640, 3)
    print(f"灰度 shape: {gray.shape}")  # (480, 640) - 没有第三维！
    
    # 为什么没有第三维？因为灰度图每个像素只有 1 个值（亮度）
    # 判断方法：
    print(f"img.ndim = {img.ndim}")     # 3
    print(f"gray.ndim = {gray.ndim}")   # 2
    
    cv2.imwrite("test_gray.jpg", gray)


def demo_uint8_overflow():
    """演示 uint8 溢出问题"""
    print("\n" + "=" * 60)
    print("4. uint8 溢出问题")
    print("=" * 60)
    
    # uint8 只能表示 0-255
    a = np.array([[200]], dtype=np.uint8)
    
    # 直接加法会溢出（绕回去）
    result_numpy = a + 100
    print(f"NumPy 直接相加: 200 + 100 = {result_numpy.ravel()[0]} (溢出！绕回 44)")
    
    # OpenCV 的 add 带截断保护
    result_cv2 = cv2.add(a, 100)
    print(f"cv2.add: 200 + 100 = {result_cv2.ravel()[0]} (截断在 255)")
    
    # 正确做法：转 float32 计算，再 clip 转回
    a_float = a.astype(np.float32)
    result_float = np.clip(a_float + 100, 0, 255).astype(np.uint8)
    print(f"float32 计算后 clip: {result_float.ravel()[0]}")


def demo_color_spaces():
    """演示各种颜色空间转换"""
    print("\n" + "=" * 60)
    print("5. 颜色空间转换")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    
    # BGR -> HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(f"HSV shape: {hsv.shape}")  # (480, 640, 3)
    print(f"  H: 0-179 (OpenCV 压缩了 360 度)")
    print(f"  S: 0-255")
    print(f"  V: 0-255")
    
    # BGR -> LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    print(f"LAB shape: {lab.shape}")
    
    # BGR -> RGB (给 matplotlib 用)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def demo_pixel_access():
    """像素访问与修改"""
    print("\n" + "=" * 60)
    print("6. 像素访问与修改")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    h, w = img.shape[:2]
    
    # 单个像素访问：img[row, col] -> [B, G, R]
    print(f"左上角 (0,0): {img[0, 0]}")        # 红色区域 [0, 0, 255]
    print(f"中心点 ({h//2},{w//2}): {img[h//2, w//2]}")  # 灰色区域
    
    # 修改单个像素
    img_copy = img.copy()
    img_copy[10, 10] = [255, 255, 255]  # 把 (10,10) 改成白色
    
    # 修改一块区域（ROI）
    img_copy[0:50, 0:50] = [0, 255, 0]  # 左上角 50x50 改成绿色
    cv2.imwrite("modified.jpg", img_copy)


def demo_image_operations():
    """常见图像操作"""
    print("\n" + "=" * 60)
    print("7. 常见图像操作")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    
    # 缩放 - 注意参数是 (宽, 高)！
    small = cv2.resize(img, (320, 240))  # 宽 320，高 240
    print(f"缩放后: {small.shape}")  # (240, 320, 3)
    
    # 翻转
    flip_h = cv2.flip(img, 1)  # 水平镜像
    flip_v = cv2.flip(img, 0)  # 垂直翻转
    
    # 画矩形
    vis = img.copy()
    cv2.rectangle(vis, (100, 100), (300, 200), (0, 255, 0), 2)  # 绿框
    cv2.putText(vis, "ROI", (100, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imwrite("with_rect.jpg", vis)


if __name__ == "__main__":
    # 准备测试图
    if not os.path.exists("test.jpg"):
        create_test_image()
    
    demo_basic_properties()
    demo_bgr_vs_rgb()
    demo_grayscale()
    demo_uint8_overflow()
    demo_color_spaces()
    demo_pixel_access()
    demo_image_operations()
    
    print("\n" + "=" * 60)
    print("所有演示完成，生成的文件：")
    for f in ["test.jpg", "test_gray.jpg", "red_bgr.jpg", "modified.jpg", "with_rect.jpg"]:
        if os.path.exists(f):
            print(f"  - {f}")