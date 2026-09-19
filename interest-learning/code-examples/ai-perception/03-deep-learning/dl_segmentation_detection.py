#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度学习分割与检测入门：SegFormer 语义分割 + YOLOv8 目标检测
对应教程：interest-learning/perception/ai-perception/04-深度学习分割与检测入门.md

依赖：
  pip install ultralytics transformers torch torchvision
  export HF_ENDPOINT=https://hf-mirror.com  # 国内加速 HuggingFace 下载
"""

import cv2
import numpy as np
import os
import time


def check_dependencies():
    """检查依赖"""
    print("=" * 60)
    print("依赖检查")
    print("=" * 60)
    
    try:
        import torch
        print(f"PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}")
    except ImportError:
        print("PyTorch 未安装: pip install torch --index-url https://download.pytorch.org/whl/cpu")
    
    try:
        import ultralytics
        print(f"Ultralytics: {ultralytics.__version__}")
    except ImportError:
        print("Ultralytics 未安装: pip install ultralytics")
    
    try:
        import transformers
        print(f"Transformers: {transformers.__version__}")
    except ImportError:
        print("Transformers 未安装: pip install transformers")


def segformer_segmentation_demo(image_path="road.jpg"):
    """
    SegFormer-B0 (ADE20K预训练) 语义分割演示
    ADE20K 中 road 类别编号 = 6
    """
    print("\n" + "=" * 60)
    print("SegFormer 语义分割 (ADE20K)")
    print("=" * 60)
    
    try:
        import torch
        from PIL import Image
        from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
    except ImportError as e:
        print(f"缺少依赖: {e}")
        return
    
    MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"
    ROAD_ID = 6  # ADE20K 中 road 的类别编号
    
    # 加载模型（首次运行自动下载 ~15MB）
    print("加载模型...")
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)
    model.eval()
    
    # 读取图片
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"读不到图片: {image_path}")
        return
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w = img_bgr.shape[:2]
    
    # 推理
    print("推理中...")
    inputs = processor(images=Image.fromarray(img_rgb), return_tensors="pt")
    
    t0 = time.time()
    with torch.no_grad():
        outputs = model(**inputs)
    infer_time = (time.time() - t0) * 1000
    
    # 后处理：上采样回原图尺寸 + argmax
    logits = torch.nn.functional.interpolate(
        outputs.logits, size=(h, w), mode="bilinear", align_corners=False
    )
    pred = logits.argmax(dim=1)[0].numpy()  # (H, W) 每个像素的类别号
    
    # 提取 road 类别做掩膜
    mask = np.where(pred == ROAD_ID, 255, 0).astype(np.uint8)
    coverage = (mask > 0).mean() * 100
    
    # 可视化
    overlay = img_bgr.copy()
    overlay[mask > 0] = (0, 255, 0)
    result = cv2.addWeighted(img_bgr, 0.6, overlay, 0.4, 0)
    
    cv2.imwrite("seg_result.png", result)
    cv2.imwrite("seg_mask.png", mask)
    
    print(f"推理耗时: {infer_time:.1f} ms")
    print(f"输出类别图 shape: {pred.shape}")
    print(f"路面像素占比: {coverage:.1f}%")
    print("已保存 seg_result.png, seg_mask.png")
    
    # 演示：把 ROAD_ID 改成 1 (building) 看看会涂出什么
    print("\n⚠️ 类别编号搞错的后果演示：")
    wrong_mask = np.where(pred == 1, 255, 0).astype(np.uint8)  # building
    print(f"  ROAD_ID=1 (building) 掩膜占比: {(wrong_mask>0).mean()*100:.1f}%")


def yolov8_detection_demo(image_path="road.jpg"):
    """
    YOLOv8n 目标检测演示
    COCO 80 类，不含"锥桶"、"路面"等专用类别
    """
    print("\n" + "=" * 60)
    print("YOLOv8n 目标检测 (COCO 80类)")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("缺少 ultralytics: pip install ultralytics")
        return
    
    # 加载模型（首次自动下载 yolov8n.pt ~6MB）
    print("加载模型...")
    model = YOLO("yolov8n.pt")
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"读不到图片: {image_path}")
        return
    
    # 推理
    t0 = time.time()
    results = model(image_path, conf=0.35, verbose=False)
    infer_time = (time.time() - t0) * 1000
    
    # 解析结果
    print(f"推理耗时: {infer_time:.1f} ms")
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
            print(f"  {model.names[cls_id]:<12} 置信度 {conf:.2f}  框 ({x1},{y1})-({x2},{y2})")
    
    # 自带可视化
    annotated = results[0].plot()
    cv2.imwrite("det_result.jpg", annotated)
    print("已保存 det_result.jpg")
    
    # 重要提醒
    print("""
⚠️ 重要：COCO 80 类里没有"锥桶"、"路面"等巴哈赛道专用类别！
     预训练模型只能认出它见过的东西（人、车、狗、杯子...）
     想检测锥桶，必须自己标注几十张图再微调 (fine-tune)
    """)


def yolov8_seg_demo(image_path="road.jpg"):
    """YOLOv8n-seg 实例分割演示"""
    print("\n" + "=" * 60)
    print("YOLOv8n-seg 实例分割")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        return
    
    model = YOLO("yolov8n-seg.pt")  # 首次下载 ~7MB
    results = model(image_path, conf=0.35, verbose=False)
    
    for r in results:
        if r.masks is not None:
            print(f"检测到 {len(r.masks)} 个实例掩膜")
            for i, mask in enumerate(r.masks.data):
                cls_id = int(r.boxes.cls[i])
                print(f"  实例 {i}: {model.names[cls_id]}, 掩膜形状 {mask.shape}")
    
    annotated = results[0].plot()
    cv2.imwrite("det_seg_result.jpg", annotated)
    print("已保存 det_seg_result.jpg")


def compare_model_sizes(image_path="road.jpg"):
    """对比不同尺寸模型的速度与精度"""
    print("\n" + "=" * 60)
    print("模型尺寸对比 (YOLOv8 系列)")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        return
    
    models = [
        ("yolov8n", "yolov8n.pt", 3.2),
        ("yolov8s", "yolov8s.pt", 11.2),
        ("yolov8m", "yolov8m.pt", 25.9),
        ("yolov8l", "yolov8l.pt", 43.7),
        ("yolov8x", "yolov8x.pt", 68.2),
    ]
    
    print(f"{'模型':<8} {'参数量(M)':>10} {'单帧耗时(ms)':>12} {'检测数':>6}")
    print("-" * 45)
    
    for name, weight_file, params in models:
        try:
            model = YOLO(weight_file)
            t0 = time.time()
            results = model(image_path, conf=0.35, verbose=False)
            elapsed = (time.time() - t0) * 1000
            det_count = sum(len(r.boxes) for r in results)
            print(f"{name:<8} {params:>10.1f} {elapsed:>12.1f} {det_count:>6}")
        except Exception as e:
            print(f"{name:<8} {params:>10.1f} {'失败':>12} ({e})")


def labelme_to_mask_demo():
    """labelme JSON 标注转掩膜图（造训练数据必备）"""
    print("\n" + "=" * 60)
    print("labelme JSON -> 掩膜图")
    print("=" * 60)
    
    import json
    
    # 模拟一个 labelme 标注文件
    sample_json = {
        "version": "5.0.1",
        "flags": {},
        "shapes": [
            {
                "label": "road",
                "points": [[100, 300], [200, 250], [400, 250], [500, 300], [500, 480], [100, 480]],
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            },
            {
                "label": "cone",
                "points": [[300, 200], [320, 240], [280, 240]],
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
        ],
        "imagePath": "road.jpg",
        "imageData": None,
        "imageHeight": 480,
        "imageWidth": 640
    }
    
    # 保存示例 JSON
    with open("sample_labelme.json", "w", encoding="utf-8") as f:
        json.dump(sample_json, f, indent=2)
    
    # 转掩膜代码
    print("转换代码：")
    print("""
import json, cv2, numpy as np

with open("xxx.json", "r", encoding="utf-8") as f:
    data = json.load(f)

h, w = data["imageHeight"], data["imageWidth"]
mask = np.zeros((h, w), np.uint8)

for shape in data["shapes"]:
    if shape["label"] == "road":  # 只看 road 标签
        pts = np.array(shape["points"], dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)

cv2.imwrite("road_mask.png", mask)
    """)
    
    # 实际运行
    h, w = sample_json["imageHeight"], sample_json["imageWidth"]
    mask = np.zeros((h, w), np.uint8)
    for shape in sample_json["shapes"]:
        if shape["label"] == "road":
            pts = np.array(shape["points"], dtype=np.int32)
            cv2.fillPoly(mask, [pts], 255)
    
    cv2.imwrite("road_mask_from_json.png", mask)
    print(f"已保存 road_mask_from_json.png, 白像素占比: {(mask>0).mean()*100:.1f}%")
    print("示例 JSON 已保存: sample_labelme.json")


if __name__ == "__main__":
    # 准备测试图
    if not os.path.exists("road.jpg"):
        # 创建一个简单的测试图
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[240:, :] = (120, 120, 120)  # 下半部灰色路面
        img[:240, :] = (100, 80, 60)    # 上半部天空
        cv2.imwrite("road.jpg", img)
    
    check_dependencies()
    
    # 这些需要联网下载模型，取消注释运行：
    # segformer_segmentation_demo()
    # yolov8_detection_demo()
    # yolov8_seg_demo()
    # compare_model_sizes()
    
    # 这个不需要联网
    labelme_to_mask_demo()
    
    print("\n💡 使用说明：")
    print("  1. pip install ultralytics transformers torch torchvision")
    print("  2. export HF_ENDPOINT=https://hf-mirror.com  # 加速下载")
    print("  3. 取消注释对应函数运行")
    print("  4. 第一次运行会自动下载权重，第二次秒开")