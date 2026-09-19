#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code-examples 统一运行器 - 简易菜单版 (无需 curses)
支持在任何终端环境运行 (Linux/WSL/Windows)
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

# 使用脚本所在目录作为基础目录，支持相对路径跨平台
BASE_DIR = Path(__file__).parent.resolve()

SAMPLES = [
    {
        "id": "algo_01",
        "path": "algorithms/01-basic-sorts/sorts.py",
        "name": "基本排序算法",
        "desc": "冒泡/选择/插入排序 + 基准测试 + 稳定性验证",
        "deps": [],
        "interactive": False,
        "needs_images": False,
    },
    {
        "id": "algo_02",
        "path": "algorithms/02-divide-conquer-sorts/recursive_sorts.py",
        "name": "分治排序算法",
        "desc": "快速排序/归并排序(函数式+原地) + 最坏情况演示",
        "deps": [],
        "interactive": False,
        "needs_images": False,
    },
    {
        "id": "algo_03",
        "path": "algorithms/03-benchmark/bench.py",
        "name": "综合基准测试",
        "desc": "5种手写排序+内置全对比 + 4种输入模式 + IoU验证",
        "deps": [],
        "interactive": False,
        "needs_images": False,
    },
    {
        "id": "vision_01",
        "path": "python-vision-basics/01-image-basics/image_basics.py",
        "name": "图像基础属性",
        "desc": "shape/dtype/BGR灰度/uint8溢出/颜色空间转换",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "vision_02",
        "path": "python-vision-basics/02-slice-roi/slice_roi.py",
        "name": "切片与ROI",
        "desc": "切片语法/视图vs副本/ROI/坐标系总结/实战流水线",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "vision_03",
        "path": "python-vision-basics/03-camera/take_photo.py",
        "name": "摄像头拍照",
        "desc": "交互版/最简版/兜底版/常见坑速查表 (需摄像头)",
        "deps": ["opencv-python", "numpy"],
        "interactive": True,
        "needs_images": False,
    },
    {
        "id": "vision_04",
        "path": "python-vision-basics/04-morphology/morphology.py",
        "name": "形态学操作",
        "desc": "腐蚀/膨胀/开闭运算/梯度/顶帽黑帽/核形状/决策指南",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "percept_01",
        "path": "ai-perception/01-color-threshold/color_threshold.py",
        "name": "颜色空间与阈值分割",
        "desc": "HSV抗光照/inRange/红色两段/三种阈值/锥桶检测",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "percept_02",
        "path": "ai-perception/02-drivable-area/drivable_area.py",
        "name": "可行驶区域识别",
        "desc": "完整9步流水线/对比图生成/参数敏感性表/自适应阈值对比",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "percept_03",
        "path": "ai-perception/03-deep-learning/dl_segmentation_detection.py",
        "name": "深度学习分割检测",
        "desc": "SegFormer/YOLOv8/模型对比/labelme转掩膜 (需PyTorch等)",
        "deps": ["torch", "ultralytics", "transformers", "opencv-python", "numpy"],
        "interactive": False,
        "needs_images": True,
    },
    {
        "id": "percept_04",
        "path": "ai-perception/04-pipeline-engineering/pipeline.py",
        "name": "感知流水线工程集成",
        "desc": "标定去畸变/三大省算力/Image+OccupancyGrid/P95量化/节点结构",
        "deps": ["opencv-python", "numpy"],
        "interactive": False,
        "needs_images": False,
    },
]

ROS2_SAMPLES = [
    {
        "id": "ros2_01",
        "path": "ros2/01-python-pkg/create_pkg.py",
        "name": "ROS2 Python包创建",
        "desc": "talker/listener/setup.py/package.xml/launch/构建脚本",
        "deps": [],
        "interactive": False,
        "needs_images": False,
        "is_ros2": True,
    },
    {
        "id": "ros2_02",
        "path": "ros2/02-cpp-pkg/create_cpp_pkg.py",
        "name": "ROS2 C++包创建",
        "desc": "talker.cpp/CMakeLists.txt逐行解读/六必备件/三翻车",
        "deps": [],
        "interactive": False,
        "needs_images": False,
        "is_ros2": True,
    },
]

ALL_SAMPLES = SAMPLES + ROS2_SAMPLES


def check_deps(deps):
    """检查依赖是否安装"""
    missing = []
    name_map = {
        "opencv-python": "cv2",
        "torch": "torch",
        "ultralytics": "ultralytics",
        "transformers": "transformers",
        "numpy": "numpy",
    }
    for dep in deps:
        import_name = name_map.get(dep, dep)
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(dep)
    return missing


def get_status(sample):
    """获取样例状态"""
    full_path = BASE_DIR / sample["path"]
    missing = check_deps(sample["deps"])
    exists = full_path.exists()
    
    if not exists:
        return "✗ 文件不存在", "red"
    if missing:
        return f"⚠ 缺少依赖: {', '.join(missing)}", "yellow"
    if sample.get("interactive"):
        return "⚠ 需交互式终端", "yellow"
    if sample.get("is_ros2"):
        return "✓ ROS2包 (需手动构建)", "cyan"
    return "✓ 就绪", "green"


def print_menu():
    """打印菜单"""
    print("\n" + "=" * 70)
    print(" code-examples 统一运行器")
    print("=" * 70)
    
    for i, sample in enumerate(ALL_SAMPLES):
        status, _ = get_status(sample)
        mark = " [ROS2]" if sample.get("is_ros2") else ""
        mark += " [交互]" if sample.get("interactive") else ""
        print(f"  {i+1:2d}. {sample['name']}{mark}")
        print(f"      {sample['desc']}")
        print(f"      状态: {status}")
        print()


def run_sample(sample):
    """运行样例"""
    full_path = BASE_DIR / sample["path"]
    
    if not full_path.exists():
        print(f"✗ 文件不存在: {full_path}")
        return
    
    missing = check_deps(sample["deps"])
    if missing:
        print(f"⚠ 缺少依赖: {', '.join(missing)}")
        print(f"  请安装: pip install {' '.join(missing)}")
        return
    
    if sample.get("is_ros2"):
        print(f"ROS2 样例为包结构，请手动运行:")
        print(f"  cd {full_path.parent}")
        print(f"  python3 {full_path.name}")
        return
    
    if sample.get("interactive"):
        print(f"⚠ 交互式样例，需在真实终端运行:")
        print(f"  cd {full_path.parent}")
        print(f"  python3 {full_path.name}")
        return
    
    print(f"\n>>> 运行: {sample['name']}")
    print(f"    路径: {full_path}")
    print("-" * 50)
    
    try:
        work_dir = full_path.parent
        result = subprocess.run(
            [sys.executable, full_path.name],
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("--- stderr ---")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"\n✓ 运行成功")
        else:
            print(f"\n✗ 运行失败 (code={result.returncode})")
            
    except subprocess.TimeoutExpired:
        print("运行超时 (120s)")
    except Exception as e:
        print(f"异常: {e}")


def check_all():
    """检查所有样例环境"""
    print("\n" + "=" * 70)
    print(" 环境检查报告")
    print("=" * 70)
    
    ready = 0
    missing_deps = 0
    missing_files = 0
    interactive = 0
    ros2 = 0
    
    for sample in ALL_SAMPLES:
        full_path = BASE_DIR / sample["path"]
        missing = check_deps(sample["deps"])
        exists = full_path.exists()
        
        if not exists:
            status = "✗ 文件不存在"
            missing_files += 1
        elif missing:
            status = f"⚠ 缺少: {', '.join(missing)}"
            missing_deps += 1
        elif sample.get("interactive"):
            status = "⚠ 需交互"
            interactive += 1
        elif sample.get("is_ros2"):
            status = "✓ ROS2包"
            ros2 += 1
        else:
            status = "✓ 就绪"
            ready += 1
        
        mark = " [ROS2]" if sample.get("is_ros2") else ""
        print(f"  {sample['name']:30s} {status}{mark}")
    
    print("-" * 70)
    print(f" 就绪: {ready}  |  缺依赖: {missing_deps}  |  缺文件: {missing_files}  |  交互: {interactive}  |  ROS2: {ros2}")
    print(f" 总计: {len(ALL_SAMPLES)}")


def main():
    if len(sys.argv) > 1:
        # 命令行参数模式
        if sys.argv[1] == "check":
            check_all()
            return
        if sys.argv[1] == "list":
            for i, s in enumerate(ALL_SAMPLES):
                print(f"{i+1}: {s['name']} - {s['path']}")
            return
        # 直接运行指定编号
        try:
            idx = int(sys.argv[1]) - 1
            if 0 <= idx < len(ALL_SAMPLES):
                run_sample(ALL_SAMPLES[idx])
            else:
                print(f"编号超范围 (1-{len(ALL_SAMPLES)})")
        except ValueError:
            print("用法: python3 run.py [check|list|编号]")
        return
    
    # 交互菜单模式
    while True:
        print_menu()
        print("操作:  输入编号运行  |  check=全量检查  |  list=列表  |  q=退出")
        choice = input(">>> ").strip().lower()
        
        if choice in ('q', 'quit', 'exit'):
            print("bye")
            break
        elif choice == 'check':
            check_all()
        elif choice == 'list':
            for i, s in enumerate(ALL_SAMPLES):
                print(f"{i+1}: {s['name']} - {s['path']}")
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(ALL_SAMPLES):
                    run_sample(ALL_SAMPLES[idx])
                else:
                    print(f"请输入 1-{len(ALL_SAMPLES)} 之间的数字")
            except ValueError:
                print("无效输入，请输入数字或命令")
        
        input("\n按回车继续...")


if __name__ == "__main__":
    main()