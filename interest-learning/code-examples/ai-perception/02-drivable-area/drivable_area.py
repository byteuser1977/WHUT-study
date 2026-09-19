#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可行驶区域识别实战：完整流水线（传统视觉方案，无深度学习）
对应教程：interest-learning/perception/ai-perception/03-可行驶区域识别实战.md
"""

import cv2
import numpy as np
import os


def create_road_test_image():
    """创建模拟路面测试图"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 天空区域（上半部）- 蓝色渐变
    for y in range(240):
        intensity = int(100 + y * 0.5)
        img[y, :] = (intensity, intensity // 2, 50)
    
    # 路面区域（下半部）- 灰色带纹理
    for y in range(240, 480):
        base = 120 + (y - 240) // 2
        row = np.full((640, 3), (base, base, base), dtype=np.uint8)
        # 加点噪声模拟路面纹理
        noise = np.random.randint(-10, 10, (640, 3))
        row = np.clip(row.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img[y, :] = row
    
    # 路边草地 - 绿色
    cv2.rectangle(img, (0, 300), (100, 480), (50, 150, 50), -1)
    cv2.rectangle(img, (540, 300), (640, 480), (50, 150, 50), -1)
    
    # 远处树木/建筑 - 深色块
    cv2.rectangle(img, (200, 100), (300, 240), (40, 40, 40), -1)
    cv2.rectangle(img, (400, 80), (500, 200), (60, 60, 60), -1)
    
    cv2.imwrite("road.jpg", img)
    return img


def drivable_detection_pipeline(img):
    """
    可行驶区域识别完整流水线
    
    步骤：
    1. 灰度化 - 3通道->1通道，降2/3运算量，本任务不依赖颜色
    2. 高斯模糊 - 抹掉高频噪声，让同质区域更整块
    3. ROI裁剪 - 只保留画面下半部分，提速+防天空干扰
    4. 阈值分割 - Otsu自动找阈值，按亮度分路面/非路面
    5. 极性判断 - 用底边中央采样点确定"白=路面"还是"黑=路面"
    6. 形态学闭运算 - 填孔洞、连断缝
    7. 最大连通域 - 只留面积最大那块（主路面）
    8. 掩膜还原 - 贴回原图位置
    9. 可视化叠加 - 半透明绿色+红色描边
    """
    h, w = img.shape[:2]
    
    # 1. 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 高斯模糊（核必须是奇数！7x7是经验值）
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 3. ROI：只保留画面下半部分
    roi_top = int(h * 0.5)
    roi = blur[roi_top:, :]
    
    # 4. 阈值分割：Otsu 自动找阈值
    thr_val, binary = cv2.threshold(roi, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"Otsu 自动阈值 = {thr_val:.1f}")
    
    # 5. 判断极性：用图像最底边中央 60x60 像素当"路面采样点"
    # 车轮正前方一定是路面，用它做锚点
    seed = binary[-60:, w // 2 - 30: w // 2 + 30]
    if (seed > 0).mean() < 0.5:
        binary = cv2.bitwise_not(binary)   # 反相，保证"白 = 可行驶"
        print("检测到路面为暗区，已反相")
    
    # 6. 形态学闭运算：修补孔洞、连接断缝
    # 椭圆核比矩形核更自然，边缘更圆润
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 7. 提取最大连通域
    num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    mask_roi = np.zeros_like(closed)
    if num > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]     # 跳过 label=0（背景）
        biggest = 1 + int(np.argmax(areas))     # 最大区域的 label
        mask_roi[labels == biggest] = 255
        print(f"共 {num - 1} 个连通域，最大面积 {int(areas.max())} 像素")
    else:
        print("未找到任何连通域，检查阈值/ROI 设置")
    
    # 8. 还原成整图尺寸的掩膜
    mask = np.zeros((h, w), np.uint8)
    mask[roi_top:, :] = mask_roi
    
    # 9. 叠加可视化
    overlay = img.copy()
    overlay[mask > 0] = (0, 255, 0)                    # 可行驶区域涂绿
    result = cv2.addWeighted(img, 0.6, overlay, 0.4, 0) # 半透明混合
    
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result, cnts, -1, (0, 0, 255), 2)  # 红色描边界
    
    coverage = (mask > 0).mean() * 100
    print(f"可行驶区域占全图 {coverage:.1f}%")
    
    return result, mask, coverage


def make_report_figure(img, save_path="report_figure.png"):
    """生成 2x2 对比图用于文档配图"""
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    roi_top = int(h * 0.5)
    roi = blur[roi_top:, :]
    
    thr_val, binary_roi = cv2.threshold(roi, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    seed = binary_roi[-60:, w // 2 - 30: w // 2 + 30]
    if (seed > 0).mean() < 0.5:
        binary_roi = cv2.bitwise_not(binary_roi)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(binary_roi, cv2.MORPH_CLOSE, kernel)
    
    num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    mask = np.zeros((h, w), np.uint8)
    if num > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        biggest = 1 + int(np.argmax(areas))
        mask[roi_top:, :] = np.where(labels == biggest, 255, 0).astype(np.uint8)
    
    overlay = img.copy()
    overlay[mask > 0] = (0, 255, 0)
    result = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result, cnts, -1, (0, 0, 255), 2)
    
    # 拼 2x2
    def to3ch(m):
        t = cv2.cvtColor(m, cv2.COLOR_GRAY2BGR)
        return t
    
    panels = [
        ("original",   img),
        ("threshold",  cv2.cvtColor(binary_roi, cv2.COLOR_GRAY2BGR)),
        ("mask",       to3ch(mask)),
        ("overlay",    result),
    ]
    # 阈值图补足到整图高度
    panels[1] = ("threshold", cv2.copyMakeBorder(
        panels[1][1], roi_top, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)))
    
    top = np.hstack([panels[0][1], panels[1][1]])
    bottom = np.hstack([panels[2][1], panels[3][1]])
    grid = np.vstack([top, bottom])
    
    # 加编号
    for i in range(4):
        pos = {0: (10, 30), 1: (w + 10, 30), 2: (10, h + 30), 3: (w + 10, h + 30)}[i]
        cv2.putText(grid, str(i+1), pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imwrite(save_path, grid)
    print(f"对比图已保存: {save_path} 尺寸: {grid.shape[1]} x {grid.shape[0]}")


def parameter_sensitivity_test(img):
    """参数敏感性对照实验"""
    print("\n" + "=" * 60)
    print("参数敏感性对照实验")
    print("=" * 60)
    
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 测试不同 ROI 起点
    print("\n--- ROI 起点比例 ---")
    for ratio in [0.4, 0.5, 0.6]:
        roi_top = int(h * ratio)
        roi = gray[roi_top:, :]
        blur = cv2.GaussianBlur(roi, (7, 7), 0)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        seed = binary[-60:, w // 2 - 30: w // 2 + 30]
        if (seed > 0).mean() < 0.5:
            binary = cv2.bitwise_not(binary)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
        if num > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            biggest = 1 + int(np.argmax(areas))
            mask = np.where(labels == biggest, 255, 0).astype(np.uint8)
            coverage = (mask > 0).mean() * 100
            print(f"  ROI={ratio}: 覆盖率={coverage:.1f}%, 最大连通域={int(areas.max())}")
    
    # 测试不同模糊核
    print("\n--- 高斯模糊核大小 ---")
    roi_top = int(h * 0.5)
    roi = gray[roi_top:, :]
    for k in [3, 7, 15]:
        blur = cv2.GaussianBlur(roi, (k, k), 0)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        seed = binary[-60:, w // 2 - 30: w // 2 + 30]
        if (seed > 0).mean() < 0.5:
            binary = cv2.bitwise_not(binary)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
        if num > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            print(f"  Blur={k}x{k}: 最大连通域={int(areas.max())}")
    
    # 测试不同闭运算核
    print("\n--- 闭运算核大小 ---")
    roi_top = int(h * 0.5)
    roi = gray[roi_top:, :]
    blur = cv2.GaussianBlur(roi, (7, 7), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    seed = binary[-60:, w // 2 - 30: w // 2 + 30]
    if (seed > 0).mean() < 0.5:
        binary = cv2.bitwise_not(binary)
    for k in [9, 25, 51]:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
        if num > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            print(f"  Kernel={k}x{k}: 最大连通域={int(areas.max())}")


def adaptive_threshold_version(img):
    """自适应阈值版本（对比 Otsu）"""
    print("\n" + "=" * 60)
    print("自适应阈值版本对比")
    print("=" * 60)
    
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    roi_top = int(h * 0.5)
    roi = blur[roi_top:, :]
    
    # Otsu
    _, binary_otsu = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 自适应阈值
    binary_adapt = cv2.adaptiveThreshold(
        roi, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 51, -10
    )
    
    cv2.imwrite("binary_otsu.png", binary_otsu)
    cv2.imwrite("binary_adapt.png", binary_adapt)
    
    print("Otsu: 全局单一阈值，适合光照均匀场景")
    print("自适应: 每块区域单独算阈值，扛单侧阴影，但噪点多")
    print("已保存 binary_otsu.png, binary_adapt.png")


def compute_iou(pred_mask, gt_mask):
    """计算 IoU (Intersection over Union)"""
    pred = pred_mask > 0
    gt = gt_mask > 0
    intersection = (pred & gt).sum()
    union = (pred | gt).sum()
    return intersection / union if union > 0 else 0


if __name__ == "__main__":
    if not os.path.exists("road.jpg"):
        create_road_test_image()
    
    img = cv2.imread("road.jpg")
    
    # 1. 跑通基线
    print("=" * 60)
    print("基线版本")
    print("=" * 60)
    result, mask, coverage = drivable_detection_pipeline(img)
    cv2.imwrite("drivable_result.png", result)
    cv2.imwrite("drivable_mask.png", mask)
    print("已保存 drivable_result.png, drivable_mask.png")
    
    # 2. 生成文档用对比图
    make_report_figure(img)
    
    # 3. 参数敏感性测试
    parameter_sensitivity_test(img)
    
    # 4. 自适应阈值对比
    adaptive_threshold_version(img)
    
    print("\n生成的文件：")
    files = ["road.jpg", "drivable_result.png", "drivable_mask.png", 
             "report_figure.png", "binary_otsu.png", "binary_adapt.png"]
    for f in files:
        if os.path.exists(f):
            print(f"  - {f}")