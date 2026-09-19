#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
切片与 ROI 裁剪
对应教程：interest-learning/perception/python-vision-basics/02-切片与roi裁剪.md

核心语法：img[行范围, 列范围] —— 先行后列！
"""

import cv2
import numpy as np
import os


def create_test_image():
    """创建测试图片"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:, :] = (80, 80, 80)        # 深灰背景
    img[0:240, :] = (0, 0, 255)     # 上半部分红色
    cv2.imwrite("test.jpg", img)
    return img


def demo_slice_syntax():
    """演示切片语法"""
    print("=" * 60)
    print("1. 切片语法基础")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    if img is None:
        print("请先运行 create_test_image()")
        return
    
    h, w = img.shape[:2]
    print(f"原图 shape: {img.shape}")  # (480, 640, 3)
    
    # 核心：取上半部分（前 240 行）
    top = img[0:240, :]
    print(f"上半部分 shape: {top.shape}")  # (240, 640, 3)
    
    # 简写形式
    top_short = img[:240]
    print(f"简写 img[:240] shape: {top_short.shape}")
    
    # 其他常用切片
    print(f"\n下半部分 img[240:,:] shape: {img[240:, :].shape}")
    print(f"左半部分 img[:,:320] shape: {img[:, :320].shape}")
    print(f"右半部分 img[:,320:] shape: {img[:, 320:].shape}")
    print(f"中心块 img[100:200,200:400] shape: {img[100:200, 200:400].shape}")
    print(f"下采样 img[::2,::2] shape: {img[::2, ::2].shape}")  # 每隔一行一列


def demo_roi():
    """演示 ROI (Region of Interest)"""
    print("\n" + "=" * 60)
    print("2. ROI - 感兴趣区域")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    h, w = img.shape[:2]
    
    # 实际应用：只关心画面下半部分（路面区域）
    roi_top = int(h * 0.5)  # 从 50% 高度开始
    roi = img[roi_top:, :]
    print(f"ROI (下半部分) shape: {roi.shape}")  # (240, 640, 3)
    
    # ROI 的三个好处：
    # 1. 省算力 - 像素减半，后续计算量约减半
    # 2. 提准确率 - 排除天空、树木等干扰区域
    # 3. 降延迟 - 直接提升 FPS


def demo_view_vs_copy():
    """演示视图 vs 副本 - 极其重要的坑！"""
    print("\n" + "=" * 60)
    print("3. 视图 vs 副本（重要陷阱）")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    
    # 切片得到的是视图，共享底层数据
    view = img[0:240, :]
    print(f"view 修改前，原图左上角: {img[0, 0]}")
    view[0, 0] = [255, 255, 255]  # 修改视图
    print(f"view 修改后，原图左上角: {img[0, 0]}")  # 原图也被改了！
    
    # 如果需要独立副本，显式调用 .copy()
    copy_ = img[0:240, :].copy()
    copy_[0, 0] = [0, 0, 0]
    print(f"copy 修改后，原图左上角: {img[0, 0]}")  # 原图不变
    
    # 利用视图特性：直接在原图上画标注
    img[0:50, 0:50] = (0, 255, 0)  # 直接把左上角涂绿


def demo_resize_flip_draw():
    """缩放、翻转、画框"""
    print("\n" + "=" * 60)
    print("4. 缩放、翻转、画矩形")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    h, w = img.shape[:2]
    
    # 缩放 - 注意参数顺序是 (宽, 高)！
    small = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    print(f"缩小后 shape: {small.shape}")  # (240, 320, 3)
    
    # 翻转
    mirror = cv2.flip(img, 1)   # 水平镜像（自拍模式）
    flip_v = cv2.flip(img, 0)   # 垂直翻转
    flip_both = cv2.flip(img, -1)  # 双向翻转
    
    # 画矩形标注 ROI
    roi_vis = img.copy()
    cv2.rectangle(roi_vis, (0, 0), (w - 1, 239), (0, 255, 0), 3)  # 绿框
    cv2.putText(roi_vis, "TOP HALF (240 rows)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # 红字
    cv2.imwrite("roi_marked.jpg", roi_vis)
    print("已保存 roi_marked.jpg")


def demo_coordinate_systems():
    """三个函数的坐标系总结"""
    print("\n" + "=" * 60)
    print("5. 坐标系总结（背下来省调试时间）")
    print("=" * 60)
    print("""
函数/操作           | 坐标顺序      | 说明
--------------------|---------------|----------------------------
img[y, x] 切片      | (行, 列)      | 先行后列，与 shape 一致
cv2.resize(img,(w,h))| (宽, 高)     | 反了！第二个参数是 (width, height)
cv2.rectangle(img,(x,y),...) | (x, y) | 列在前，行在后
cv2.circle(img,(cx,cy),...)  | (x, y) | 同 rectangle
cv2.putText(img,text,(x,y),..)| (x, y) | 文字左下角起点
""")


def demo_roi_practical():
    """实际场景：感知流程中的 ROI 裁剪"""
    print("\n" + "=" * 60)
    print("6. 实战：感知流水线中的 ROI")
    print("=" * 60)
    
    img = cv2.imread("test.jpg")
    h, w = img.shape[:2]
    
    # 步骤 1: 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 步骤 2: 高斯模糊
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 步骤 3: ROI 裁剪 - 只处理下半部分
    roi_top = int(h * 0.5)
    roi = blur[roi_top:, :]
    print(f"ROI 灰度图 shape: {roi.shape}")
    
    # 步骤 4: 阈值分割 (Otsu)
    _, binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 步骤 5: 形态学闭运算
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 步骤 6: 最大连通域
    num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    if num > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        biggest = 1 + int(np.argmax(areas))
        mask_roi = np.where(labels == biggest, 255, 0).astype(np.uint8)
        print(f"找到 {num-1} 个连通域，最大面积: {int(areas.max())} 像素")
    else:
        mask_roi = np.zeros_like(closed)
    
    # 步骤 7: 还原到原图尺寸
    mask = np.zeros((h, w), np.uint8)
    mask[roi_top:, :] = mask_roi
    
    # 可视化
    overlay = img.copy()
    overlay[mask > 0] = (0, 255, 0)
    result = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
    cv2.imwrite("drivable_result.jpg", result)
    print("已保存 drivable_result.jpg")


if __name__ == "__main__":
    if not os.path.exists("test.jpg"):
        create_test_image()
    
    demo_slice_syntax()
    demo_roi()
    demo_view_vs_copy()
    demo_resize_flip_draw()
    demo_coordinate_systems()
    demo_roi_practical()
    
    print("\n生成的文件：")
    for f in ["test.jpg", "roi_marked.jpg", "drivable_result.jpg"]:
        if os.path.exists(f):
            print(f"  - {f}")