#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形态学操作：腐蚀、膨胀、开运算、闭运算、梯度、顶帽、黑帽
对应教程：interest-learning/perception/python-vision-basics/04-形态学操作.md
"""

import cv2
import numpy as np
import os


def create_test_binary():
    """创建测试用的二值图"""
    # 先生成一张灰度图
    img = np.zeros((400, 600), dtype=np.uint8)
    
    # 画几个白色矩形和圆
    cv2.rectangle(img, (50, 50), (200, 200), 255, -1)    # 实心矩形
    cv2.rectangle(img, (250, 50), (350, 150), 255, -1)   # 另一个矩形
    cv2.circle(img, (450, 100), 60, 255, -1)             # 实心圆
    cv2.rectangle(img, (50, 250), (150, 350), 255, -1)   # 小矩形
    
    # 故意加一些噪点
    noise = np.random.randint(0, 256, img.shape, dtype=np.uint8)
    img[noise > 250] = 255
    
    # 在大矩形里挖个洞
    cv2.rectangle(img, (100, 100), (150, 150), 0, -1)
    
    cv2.imwrite("binary_src.png", img)
    return img


def demo_basic_operations():
    """基础操作：腐蚀、膨胀"""
    print("=" * 60)
    print("1. 基础操作：腐蚀 vs 膨胀")
    print("=" * 60)
    
    binary = create_test_binary()
    kernel = np.ones((5, 5), np.uint8)
    
    # 腐蚀：白区变小，噪点消失，小洞变大
    eroded = cv2.erode(binary, kernel, iterations=1)
    
    # 膨胀：白区变大，小洞被填，近邻连接
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    cv2.imwrite("morph_erode.png", eroded)
    cv2.imwrite("morph_dilate.png", dilated)
    
    print(f"原图白像素: {int(binary.sum()/255)}")
    print(f"腐蚀后:   {int(eroded.sum()/255)} (变小)")
    print(f"膨胀后:   {int(dilated.sum()/255)} (变大)")


def demo_open_close():
    """组合操作：开运算、闭运算"""
    print("\n" + "=" * 60)
    print("2. 组合操作：开运算 vs 闭运算")
    print("=" * 60)
    
    binary = create_test_binary()
    kernel = np.ones((5, 5), np.uint8)
    
    # 开运算 = 先腐蚀后膨胀
    # 效果：去掉小噪点，形状大小基本不变
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # 闭运算 = 先膨胀后腐蚀
    # 效果：填补小孔洞、连接断裂，形状大小基本不变
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    cv2.imwrite("morph_open.png", opened)
    cv2.imwrite("morph_close.png", closed)
    
    print(f"原图白像素:  {int(binary.sum()/255)}")
    print(f"开运算后:    {int(opened.sum()/255)}  (噪点没了，主体保留)")
    print(f"闭运算后:    {int(closed.sum()/255)}   (洞补上了，断缝连上了)")
    
    # 记忆口诀
    print("""
    记忆：
    - 开运算 = 开"掉"噪点（先腐蚀把噪点干掉，再膨胀恢复主体）
    - 闭运算 = 闭"上"孔洞（先膨胀把洞填上，再腐蚀恢复边界）
    """)


def demo_advanced_operations():
    """进阶操作：梯度、顶帽、黑帽"""
    print("\n" + "=" * 60)
    print("3. 进阶操作：梯度、顶帽、黑帽")
    print("=" * 60)
    
    binary = create_test_binary()
    kernel = np.ones((5, 5), np.uint8)
    
    # 形态学梯度 = 膨胀 - 腐蚀
    # 效果：只保留边缘轮廓线
    gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
    
    # 顶帽 = 原图 - 开运算
    # 效果：提取比背景亮的小细节
    tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
    
    # 黑帽 = 闭运算 - 原图
    # 效果：提取比背景暗的小细节
    blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
    
    cv2.imwrite("morph_gradient.png", gradient)
    cv2.imwrite("morph_tophat.png", tophat)
    cv2.imwrite("morph_blackhat.png", blackhat)
    
    print(f"梯度白像素:  {int(gradient.sum()/255)}  (边缘线)")
    print(f"顶帽白像素:  {int(tophat.sum()/255)}   (亮细节)")
    print(f"黑帽白像素:  {int(blackhat.sum()/255)}   (暗细节)")


def demo_kernel_shapes():
    """不同形状的结构元素"""
    print("\n" + "=" * 60)
    print("4. 结构元素形状对比")
    print("=" * 60)
    
    binary = create_test_binary()
    
    # 矩形核
    kernel_rect = np.ones((5, 5), np.uint8)
    # 椭圆核 - 更自然，处理圆形目标效果好
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # 十字核 - 保留细长结构
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    
    close_rect = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_rect)
    close_ellipse = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_ellipse)
    close_cross = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_cross)
    
    cv2.imwrite("kernel_rect.png", close_rect)
    cv2.imwrite("kernel_ellipse.png", close_ellipse)
    cv2.imwrite("kernel_cross.png", close_cross)
    
    print(f"矩形核闭运算:  {int(close_rect.sum()/255)}")
    print(f"椭圆核闭运算:  {int(close_ellipse.sum()/255)}  (边缘更圆润)")
    print(f"十字核闭运算:  {int(close_cross.sum()/255)}   (保留细长结构)")


def demo_iterations():
    """iterations 参数效果"""
    print("\n" + "=" * 60)
    print("5. iterations 参数：重复多次")
    print("=" * 60)
    
    binary = create_test_binary()
    kernel = np.ones((3, 3), np.uint8)
    
    for iters in [1, 2, 3]:
        eroded = cv2.erode(binary, kernel, iterations=iters)
        dilated = cv2.dilate(binary, kernel, iterations=iters)
        print(f"  iterations={iters}: 腐蚀白像素={int(eroded.sum()/255)}, 膨胀白像素={int(dilated.sum()/255)}")
    
    print("注意：iterations=2 等于做两次操作，效果更强")


def demo_practical_pipeline():
    """实战流水线：阈值分割后用形态学修补"""
    print("\n" + "=" * 60)
    print("6. 实战：可行驶区域识别中的形态学")
    print("=" * 60)
    
    # 模拟：灰度图 -> 阈值分割 -> 得到粗糙二值图
    gray = np.zeros((300, 400), dtype=np.uint8)
    cv2.rectangle(gray, (50, 150), (350, 250), 200, -1)  # 路面区域
    cv2.circle(gray, (200, 200), 80, 180, -1)
    # 加噪声
    noise = np.random.randint(0, 50, gray.shape, dtype=np.uint8)
    gray = cv2.add(gray, noise)
    
    # 阈值分割
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # 形态学清理流水线
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    
    # 1. 闭运算：填路面上的小洞（井盖、阴影、水坑）
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 2. 开运算：去隔离噪点
    cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    
    cv2.imwrite("pipeline_gray.png", gray)
    cv2.imwrite("pipeline_binary.png", binary)
    cv2.imwrite("pipeline_closed.png", closed)
    cv2.imwrite("pipeline_cleaned.png", cleaned)
    
    print("流水线：灰度图 -> 阈值分割 -> 闭运算(补洞) -> 开运算(去噪) -> 干净掩膜")


def demo_selection_guide():
    """选哪个操作的决策指南"""
    print("\n" + "=" * 60)
    print("7. 决策指南：拿到二值图，怎么选操作？")
    print("=" * 60)
    print("""
    问自己两个问题：
    
    1. 有孤立的小白点（噪点）吗？
       是 --> 开运算 MORPH_OPEN  (去噪)
    
    2. 区域内有黑洞、断缝吗？
       是 --> 闭运算 MORPH_CLOSE (补洞、连线)
    
    3. 想要目标轮廓线吗？
       是 --> 形态学梯度 MORPH_GRADIENT
    
    4. 光照不均、要提亮/暗细节吗？
       是 --> 顶帽/黑帽 MORPH_TOPHAT / MORPH_BLACKHAT
    
    5. 都不确定/通用场景？
       先试闭运算 (可行驶区域识别最常用的就是它)
    """)


if __name__ == "__main__":
    if not os.path.exists("binary_src.png"):
        create_test_binary()
    
    demo_basic_operations()
    demo_open_close()
    demo_advanced_operations()
    demo_kernel_shapes()
    demo_iterations()
    demo_practical_pipeline()
    demo_selection_guide()
    
    print("\n生成的文件：")
    files = [
        "binary_src.png", "morph_erode.png", "morph_dilate.png",
        "morph_open.png", "morph_close.png", "morph_gradient.png",
        "morph_tophat.png", "morph_blackhat.png",
        "kernel_rect.png", "kernel_ellipse.png", "kernel_cross.png",
        "pipeline_gray.png", "pipeline_binary.png", "pipeline_closed.png", "pipeline_cleaned.png"
    ]
    for f in files:
        if os.path.exists(f):
            print(f"  - {f}")