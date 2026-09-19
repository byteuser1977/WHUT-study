#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
颜色空间与阈值分割：HSV、inRange、Otsu、自适应阈值
对应教程：interest-learning/perception/ai-perception/02-颜色空间与阈值分割.md
"""

import cv2
import numpy as np
import os


def create_color_test_image():
    """创建包含多种颜色的测试图"""
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # 画不同颜色的块 (BGR)
    colors = {
        "red": (0, 0, 255),      # 红
        "orange": (0, 128, 255), # 橙
        "yellow": (0, 255, 255), # 黄
        "green": (0, 255, 0),    # 绿
        "blue": (255, 0, 0),     # 蓝
        "purple": (255, 0, 128), # 紫
    }
    
    x_positions = [50, 150, 250, 350, 450, 550]
    for i, (name, bgr) in enumerate(colors.items()):
        cv2.rectangle(img, (x_positions[i], 100), (x_positions[i] + 80, 300), bgr, -1)
        cv2.putText(img, name, (x_positions[i], 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imwrite("color_test.jpg", img)
    return img


def demo_hsv_vs_bgr():
    """演示 HSV 为什么比 BGR 抗光照"""
    print("=" * 60)
    print("1. HSV vs BGR：光照变化下的表现")
    print("=" * 60)
    
    img = cv2.imread("color_test.jpg")
    if img is None:
        create_color_test_image()
        img = cv2.imread("color_test.jpg")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 取红色块中心的像素
    # 红色块大概在 x=50-130, y=100-300，中心约 (90, 200)
    bgr_pixel = img[200, 90]
    hsv_pixel = hsv[200, 90]
    print(f"原图红色块中心: BGR={bgr_pixel}, HSV={hsv_pixel}")
    
    # 模拟变暗 50%（阴影）
    dark = (img.astype(np.float32) * 0.5).astype(np.uint8)
    dark_hsv = cv2.cvtColor(dark, cv2.COLOR_BGR2HSV)
    bgr_dark = dark[200, 90]
    hsv_dark = dark_hsv[200, 90]
    print(f"变暗后同一位置: BGR={bgr_dark}, HSV={hsv_dark}")
    
    print(f"""
    对比：
    BGR: 三个通道全变了 ({bgr_pixel} -> {bgr_dark})
    HSV: H 几乎没变 ({hsv_pixel[0]} -> {hsv_dark[0]})，只有 S/V 变了
    
    结论：H 通道只表示"是什么颜色"，与光照基本解耦！
    """)


def demo_hsv_ranges():
    """HSV 常用颜色阈值参考表演示"""
    print("\n" + "=" * 60)
    print("2. HSV 颜色阈值参考表 (OpenCV: H=0~179)")
    print("=" * 60)
    
    ranges = {
        "红(段1)": ([0, 43, 46], [10, 255, 255]),
        "红(段2)": ([170, 43, 46], [179, 255, 255]),
        "橙(锥桶)": ([11, 43, 46], [25, 255, 255]),
        "黄": ([26, 43, 46], [34, 255, 255]),
        "绿": ([35, 43, 46], [77, 255, 255]),
        "蓝": ([100, 43, 46], [124, 255, 255]),
        "紫": ([125, 43, 46], [155, 255, 255]),
    }
    
    img = cv2.imread("color_test.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    for name, (lower, upper) in ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)
        white_pixels = int(mask.sum() / 255)
        print(f"  {name:8s}: H={lower[0]:3d}~{upper[0]:3d}  白像素={white_pixels:5d}")


def demo_inrange_basic():
    """inRange 基础用法：抠橙色（锥桶色）"""
    print("\n" + "=" * 60)
    print("3. inRange 基础：抠出橙色")
    print("=" * 60)
    
    img = cv2.imread("color_test.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 橙色范围
    lower = np.array([11, 43, 46])
    upper = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    
    # 用掩膜抠出原图对应区域
    result = cv2.bitwise_and(img, img, mask=mask)
    
    cv2.imwrite("mask_orange.png", mask)
    cv2.imwrite("result_orange.png", result)
    
    print(f"掩膜白像素: {int(mask.sum()/255)}")
    print("已保存 mask_orange.png, result_orange.png")


def demo_red_two_ranges():
    """红色的正确写法：两段合并"""
    print("\n" + "=" * 60)
    print("4. 红色陷阱：必须两段 inRange 再或运算")
    print("=" * 60)
    
    img = cv2.imread("color_test.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 第一段：H 0~10
    mask1 = cv2.inRange(hsv, np.array([0, 43, 46]), np.array([10, 255, 255]))
    # 第二段：H 170~179
    mask2 = cv2.inRange(hsv, np.array([170, 43, 46]), np.array([179, 255, 255]))
    # 合并
    mask_red = cv2.bitwise_or(mask1, mask2)
    
    # 错误写法：只写一段
    mask_red_wrong = cv2.inRange(hsv, np.array([0, 43, 46]), np.array([10, 255, 255]))
    
    cv2.imwrite("mask_red_correct.png", mask_red)
    cv2.imwrite("mask_red_wrong.png", mask_red_wrong)
    
    print(f"正确写法(两段或): 白像素={int(mask_red.sum()/255)}")
    print(f"错误写法(只一段): 白像素={int(mask_red_wrong.sum()/255)} (漏掉一半！)")


def demo_gray_thresholds():
    """灰度图阈值分割：固定、Otsu、自适应"""
    print("\n" + "=" * 60)
    print("5. 灰度图阈值：固定 / Otsu / 自适应")
    print("=" * 60)
    
    # 创建光照不均的测试图：左半边亮，右半边暗
    gray = np.zeros((300, 400), dtype=np.uint8)
    cv2.rectangle(gray, (0, 0), (200, 300), 200, -1)   # 左亮
    cv2.rectangle(gray, (200, 0), (400, 300), 100, -1)  # 右暗
    # 中间放个白方块跨越明暗边界
    cv2.rectangle(gray, (180, 100), (220, 200), 255, -1)
    
    cv2.imwrite("gray_uneven.png", gray)
    
    # (a) 固定阈值 127
    _, th_fixed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # (b) Otsu 自动阈值
    thresh_val, th_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # (c) 自适应阈值：每个小区域单独算阈值
    th_adapt = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,   # 邻域大小 (奇数)
        2     # 从局部均值减去的常数
    )
    
    cv2.imwrite("th_fixed.png", th_fixed)
    cv2.imwrite("th_otsu.png", th_otsu)
    cv2.imwrite("th_adapt.png", th_adapt)
    
    print(f"固定阈值 127:   白像素={int(th_fixed.sum()/255)}  (右半边全黑了)")
    print(f"Otsu 阈值={thresh_val:.1f}: 白像素={int(th_otsu.sum()/255)}  (折中，右半边丢了)")
    print(f"自适应阈值:     白像素={int(th_adapt.sum()/255)}  (两边都能分出来！)")


def demo_cone_detection_pipeline():
    """完整实战：锥桶检测流水线"""
    print("\n" + "=" * 60)
    print("6. 实战：橙色锥桶检测流水线")
    print("=" * 60)
    
    # 创建模拟赛道图：背景绿色，几个橙色锥桶
    img = np.zeros((300, 500, 3), dtype=np.uint8)
    img[:, :] = (50, 150, 50)  # 绿色草地背景 (BGR)
    
    # 画几个橙色锥桶 (近似三角形)
    cone_positions = [(100, 200), (250, 150), (400, 220)]
    for cx, cy in cone_positions:
        pts = np.array([
            [cx, cy - 30],      # 顶点
            [cx - 20, cy + 20], # 左下
            [cx + 20, cy + 20]  # 右下
        ], np.int32)
        cv2.fillPoly(img, [pts], (0, 128, 255))  # 橙色 BGR
    
    cv2.imwrite("cone_scene.jpg", img)
    
    # === 检测流水线 ===
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 1. 颜色筛选（橙红两段）
    m1 = cv2.inRange(hsv, np.array([0, 70, 70]), np.array([10, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([11, 70, 70]), np.array([25, 255, 255]))
    mask = cv2.bitwise_or(m1, m2)
    
    # 2. 形态学去噪
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 补小洞
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 去小噪点
    
    # 3. 找轮廓并框出来
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result = img.copy()
    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area < 100:      # 太小当噪声丢掉
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(result, "cone", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        count += 1
    
    cv2.imwrite("cone_mask.png", mask)
    cv2.imwrite("cone_result.png", result)
    
    print(f"检测到 {count} 个锥桶候选")
    print("已保存 cone_mask.png, cone_result.png")


def demo_light_influence():
    """练习：直观看光照影响"""
    print("\n" + "=" * 60)
    print("7. 练习：光照对 BGR vs HSV 的影响")
    print("=" * 60)
    
    img = cv2.imread("color_test.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 模拟变暗 50%
    dark = (img.astype(np.float32) * 0.5).astype(np.uint8)
    dark_hsv = cv2.cvtColor(dark, cv2.COLOR_BGR2HSV)
    
    # 取几个点对比
    points = [(200, 90), (200, 190), (200, 290), (200, 390), (200, 490), (200, 590)]
    color_names = ["红", "橙", "黄", "绿", "蓝", "紫"]
    
    print(f"{'颜色':<4} {'BGR原始':>18} {'BGR变暗':>18} {'HSV原始':>14} {'HSV变暗':>14}")
    print("-" * 70)
    for (y, x), name in zip(points, color_names):
        bgr_orig = img[y, x]
        bgr_dark = dark[y, x]
        hsv_orig = hsv[y, x]
        hsv_dark = dark_hsv[y, x]
        print(f"{name:<4} {str(tuple(bgr_orig)):>18} {str(tuple(bgr_dark)):>18} "
              f"H={hsv_orig[0]:3d} S={hsv_orig[1]:3d} V={hsv_orig[2]:3d} "
              f"H={hsv_dark[0]:3d} S={hsv_dark[1]:3d} V={hsv_dark[2]:3d}")


def demo_split_hsv():
    """拆分 HSV 三通道单独看"""
    print("\n" + "=" * 60)
    print("8. 拆分 HSV 通道观察")
    print("=" * 60)
    
    img = cv2.imread("color_test.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    cv2.imwrite("h_channel.png", h)
    cv2.imwrite("s_channel.png", s)
    cv2.imwrite("v_channel.png", v)
    
    print("H 通道：同一颜色区域亮度接近（颜色分类图）")
    print("S 通道：颜色纯度，彩色区域亮，灰色区域暗")
    print("V 通道：近似灰度图（明度）")
    print("已保存 h_channel.png, s_channel.png, v_channel.png")


if __name__ == "__main__":
    if not os.path.exists("color_test.jpg"):
        create_color_test_image()
    
    demo_hsv_vs_bgr()
    demo_hsv_ranges()
    demo_inrange_basic()
    demo_red_two_ranges()
    demo_gray_thresholds()
    demo_cone_detection_pipeline()
    demo_light_influence()
    demo_split_hsv()
    
    print("\n生成的文件：")
    files = [
        "color_test.jpg", "mask_orange.png", "result_orange.png",
        "mask_red_correct.png", "mask_red_wrong.png",
        "gray_uneven.png", "th_fixed.png", "th_otsu.png", "th_adapt.png",
        "cone_scene.jpg", "cone_mask.png", "cone_result.png",
        "h_channel.png", "s_channel.png", "v_channel.png"
    ]
    for f in files:
        if os.path.exists(f):
            print(f"  - {f}")