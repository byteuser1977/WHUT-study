#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用摄像头拍照
对应教程：interest-learning/perception/python-vision-basics/03-调用摄像头拍照.md

核心：摄像头是连续吐帧的"水龙头"，拍照=读一帧+存盘
"""

import cv2
import os
import time


def demo_camera_basics():
    """摄像头基本原理演示"""
    print("=" * 60)
    print("1. 摄像头原理：水龙头模型")
    print("=" * 60)
    print("""
    手机拍照：按快门 -> 得到一张照片
    程序里摄像头：打开后每秒塞 30 张画面 (30 FPS)，源源不断
    
    "拍照"在代码里拆成三步：
    1. 打开水龙头: cap = cv2.VideoCapture(0)
    2. 接一杯水:   ok, frame = cap.read()    
    3. 存进瓶子:   cv2.imwrite("photo.jpg", frame)
    """)


def take_photo_interactive():
    """
    完整交互版：预览 -> 按空格拍照 -> 存盘
    Windows 建议用 cv2.CAP_DSHOW 后端，打开快、稳定
    """
    print("\n" + "=" * 60)
    print("2. 交互式拍照程序")
    print("=" * 60)
    
    CAMERA_INDEX = 0        # 0=默认摄像头，外接常是 1
    SAVE_DIR = "photos"
    
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # Windows 用 DirectShow 后端，避免 5-10 秒卡顿
    backend = cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY
    cap = cv2.VideoCapture(CAMERA_INDEX, backend)
    
    if not cap.isOpened():
        print(f"❌ 无法打开摄像头 (index={CAMERA_INDEX})")
        print("   检查：1) 是否被微信/会议占用  2) 试 index=1  3) WSL 请在 Windows 跑")
        return
    
    # 请求分辨率（摄像头可能不听）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"✅ 摄像头已打开 (index={CAMERA_INDEX})")
    print("   操作：按【空格】拍照，按【q】或【ESC】退出")
    
    shot_count = 0
    
    try:
        while True:
            ok, frame = cap.read()           # 读一帧
            if not ok:
                print("⚠️ 读取帧失败，退出")
                break
            
            frame = cv2.flip(frame, 1)       # 水平镜像，符合自拍直觉
            
            # 画面上叠加提示文字
            cv2.putText(frame, "SPACE = shoot, q = quit",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
            
            cv2.imshow("Camera - press SPACE", frame)  # 显示
            
            key = cv2.waitKey(1) & 0xFF      # 等 1ms，处理 GUI 事件 + 读按键
            if key == ord(" ") or key == ord("s"):   # 空格或 s
                shot_count += 1
                filename = os.path.join(
                    SAVE_DIR,
                    time.strftime("photo_%Y%m%d_%H%M%S") + f"_{shot_count}.jpg"
                )
                cv2.imwrite(filename, frame)
                print(f"📷 已保存：{filename}  ({frame.shape[1]}x{frame.shape[0]})")
                time.sleep(0.3)              # 防手抖连拍
            elif key == ord("q") or key == 27:       # q 或 ESC
                break
    finally:
        cap.release()                        # 释放摄像头
        cv2.destroyAllWindows()              # 关所有窗口
        print(f"👋 退出，共拍 {shot_count} 张，文件在 ./{SAVE_DIR}/")


def quick_shot():
    """
    最简版：打开摄像头 3 秒后自动拍一张
    注意：摄像头刚打开前几帧常是黑的（自动曝光未稳定），别只用第一帧
    """
    print("\n" + "=" * 60)
    print("3. 最简版自动拍照")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
    
    # 丢掉前几帧，等曝光稳定
    for _ in range(5):
        cap.read()
        time.sleep(0.1)
    
    ok, frame = cap.read()
    if ok:
        frame = cv2.flip(frame, 1)
        cv2.imwrite("me.jpg", frame)
        print("✅ 已保存 me.jpg")
    else:
        print("❌ 打不开摄像头")
    
    cap.release()


def check_photo():
    """验证照片是否正常"""
    print("\n" + "=" * 60)
    print("4. 验证照片")
    print("=" * 60)
    
    # 找最新的照片
    photos_dir = "photos"
    if os.path.exists(photos_dir):
        files = [f for f in os.listdir(photos_dir) if f.endswith(".jpg")]
        if files:
            latest = max(files, key=lambda f: os.path.getmtime(os.path.join(photos_dir, f)))
            path = os.path.join(photos_dir, latest)
        else:
            path = "me.jpg" if os.path.exists("me.jpg") else None
    else:
        path = "me.jpg" if os.path.exists("me.jpg") else None
    
    if path and os.path.exists(path):
        img = cv2.imread(path)
        print(f"文件: {path}")
        print(f"shape = {img.shape}")      # 应为 (480, 640, 3)
        print(f"dtype = {img.dtype}")      # uint8
    else:
        print("未找到照片文件")


def fallback_no_camera():
    """
    没有摄像头时的兜底：用图片/视频模拟摄像头
    逻辑完全一样，只是数据源变了
    """
    print("\n" + "=" * 60)
    print("5. 兜底版：无摄像头也能练")
    print("=" * 60)
    
    # 传图片路径给 VideoCapture，OpenCV 会当成 1 帧的流
    cap = cv2.VideoCapture("test.jpg")   # 需要先有 test.jpg
    ok, frame = cap.read()
    print(f"读到帧: {ok}, shape: {frame.shape if frame is not None else None}")
    cap.release()
    
    # 也可以传视频文件
    # cap = cv2.VideoCapture("video.mp4")


def demo_common_pitfalls():
    """常见坑速查"""
    print("\n" + "=" * 60)
    print("6. 常见坑速查表")
    print("=" * 60)
    pits = [
        ("程序卡住 5-10 秒", "Windows 默认后端慢", "加 cv2.CAP_DSHOW"),
        ("无法打开摄像头", "被微信/会议/浏览器占用", "关掉占用程序"),
        ("画面全灰/全黑", "物理挡板/隐私开关没开", "检查 F10 热键、Win 隐私设置"),
        ("窗口白屏/无响应", "循环里没 waitKey", "补上 cv2.waitKey(1)"),
        ("按 q 退不出", "少了 & 0xFF", "key = cv2.waitKey(1) & 0xFF"),
        ("module 'cv2' has no attribute 'imshow'", "装成了 headless 版", "卸载 headless，装 opencv-python"),
        ("'NoneType' object has no attribute", "没检查 ok / 路径错", "检查 ok；imread 失败也返回 None"),
        ("程序结束摄像头灯还亮", "没 release()", "放在 finally 里"),
    ]
    for symptom, cause, fix in pits:
        print(f"  现象: {symptom}")
        print(f"    原因: {cause}")
        print(f"    解决: {fix}")
        print()


if __name__ == "__main__":
    demo_camera_basics()
    
    # 交互式拍照（取消注释运行）
    # take_photo_interactive()
    
    # 最简版（取消注释运行）
    # quick_shot()
    
    # 验证照片
    check_photo()
    
    # 兜底版
    # fallback_no_camera()
    
    # 常见坑
    demo_common_pitfalls()
    
    print("\n💡 使用说明：")
    print("  1. 先 pip install opencv-python numpy")
    print("  2. Windows 下直接运行：python take_photo.py")
    print("  3. WSL 请在 Windows 的 Python 里跑（WSL 默认访问不到摄像头）")
    print("  4. 窗口弹出后，按空格拍照，按 q 退出")