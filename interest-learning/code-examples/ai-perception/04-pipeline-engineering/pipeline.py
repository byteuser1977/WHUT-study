#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
感知流水线与工程集成：相机标定、去畸变、ROI/降分辨率/抽帧、ROS2 发布、延迟量化
对应教程：interest-learning/perception/ai-perception/05-感知流水线与工程集成.md
"""

import cv2
import numpy as np
import os
import time
import glob


def demo_camera_calibration():
    """相机标定：棋盘格标定获取内参 K 和畸变系数 D"""
    print("=" * 60)
    print("1. 相机标定 (calibrate.py)")
    print("=" * 60)
    print("""
标定步骤：
1. 打印棋盘格 (如 9x6 内角点，格子 25mm)，贴硬板
2. 拍 15-20 张不同角度照片，棋盘格铺满画面不同区域
3. 放入 calib/ 目录
4. 运行下面代码，生成 camera_calib.npz
    """)
    
    # 标定代码（需要准备 calib/ 目录下的棋盘格照片）
    calib_code = '''
import numpy as np
import cv2
import glob

BOARD = (9, 6)          # 内角点数量（注意是"角点"，不是格子数，比格子少 1）
SQUARE_MM = 25.0

# 3D 世界坐标系下的角点位置
objp = np.zeros((BOARD[0] * BOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD[0], 0:BOARD[1]].T.reshape(-1, 2) * SQUARE_MM

obj_points, img_points = [], []
for fname in sorted(glob.glob("calib/*.jpg")):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ok, corners = cv2.findChessboardCorners(gray, BOARD, None)
    if ok:
        obj_points.append(objp)
        img_points.append(corners)
print(f"成功检测角点照片数: {len(obj_points)}")

ret, K, D, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
print(f"重投影误差: {ret:.4f} (<0.5 像素算优秀)")
print(f"内参矩阵 K:\\n{np.round(K, 2)}")
print(f"畸变系数 D: {np.round(D.ravel(), 4)}")

np.savez("camera_calib.npz", K=K, D=D)
print("已保存 camera_calib.npz")
'''
    print(calib_code)
    
    # 检查是否有标定文件
    if os.path.exists("camera_calib.npz"):
        calib = np.load("camera_calib.npz")
        K, D = calib["K"], calib["D"]
        print(f"已有标定文件:")
        print(f"  K =\\n{np.round(K, 2)}")
        print(f"  D = {np.round(D.ravel(), 4)}")
    else:
        print("⚠️ 无 camera_calib.npz，需先运行标定代码")


def demo_undistort():
    """去畸变：实时用 initUndistortRectifyMap + remap（查表法，比 undistort 快一倍）"""
    print("\n" + "=" * 60)
    print("2. 去畸变 (undistort_live.py)")
    print("=" * 60)
    
    if not os.path.exists("camera_calib.npz"):
        print("⚠️ 无标定文件，跳过演示")
        return
    
    calib = np.load("camera_calib.npz")
    K, D = calib["K"], calib["D"]
    
    # 模拟一帧图像演示
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (540, 380), (255, 255, 255), 2)
    cv2.line(img, (0, 240), (640, 240), (0, 255, 0), 1)
    cv2.line(img, (320, 0), (320, 480), (0, 255, 0), 1)
    
    h, w = img.shape[:2]
    
    # 关键：只算一次映射表
    map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, (w, h), cv2.CV_16SC2)
    
    # 实时每帧只做 remap 查表
    fixed = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)
    
    cv2.imwrite("distorted.png", img)
    cv2.imwrite("undistorted.png", fixed)
    print("已保存 distorted.png, undistorted.png")
    print("对比：右图直线（门框、显示器边缘）更直，边缘被拉伸修正")


def demo_performance_tricks():
    """三大省算力手段：ROI裁剪、降分辨率、抽帧"""
    print("\n" + "=" * 60)
    print("3. 三大省算力手段")
    print("=" * 60)
    
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    h, w = img.shape[:2]
    
    def dummy_perception(frame):
        """模拟感知算法耗时"""
        time.sleep(0.001)  # 模拟 1ms 计算
        return np.zeros(frame.shape[:2], dtype=np.uint8)
    
    # 基线：全图 640x480
    t0 = time.perf_counter()
    for _ in range(100):
        dummy_perception(img)
    baseline = (time.perf_counter() - t0) / 100 * 1000
    print(f"基线 (640x480 全图): {baseline:.1f} ms/帧")
    
    # 1. ROI 裁剪：只处理下半部分
    roi_img = img[h//2:, :]
    t0 = time.perf_counter()
    for _ in range(100):
        dummy_perception(roi_img)
    roi_time = (time.perf_counter() - t0) / 100 * 1000
    print(f"ROI 裁剪 (下半部 320x240): {roi_time:.1f} ms/帧  (省 {(1-roi_time/baseline)*100:.0f}%)")
    
    # 2. 降分辨率：640x480 -> 320x240
    small = cv2.resize(img, (w//2, h//2), interpolation=cv2.INTER_AREA)
    t0 = time.perf_counter()
    for _ in range(100):
        dummy_perception(small)
    resize_time = (time.perf_counter() - t0) / 100 * 1000
    print(f"降分辨率 (320x240): {resize_time:.1f} ms/帧  (省 {(1-resize_time/baseline)*100:.0f}%)")
    
    # 3. 组合：降分辨率 + ROI
    small_roi = small[small.shape[0]//2:, :]
    t0 = time.perf_counter()
    for _ in range(100):
        dummy_perception(small_roi)
    combo_time = (time.perf_counter() - t0) / 100 * 1000
    print(f"组合 (320x240 + ROI): {combo_time:.1f} ms/帧  (省 {(1-combo_time/baseline)*100:.0f}%)")
    
    # 4. 抽帧：30FPS 只处理 15FPS
    print(f"\\n抽帧 1/2: 理论再省 50% 算力 (需配合时序滤波)")
    
    print("""
总结：
| 手段          | 省算力 | 代价                    |
|---------------|--------|-------------------------|
| ROI 裁剪      | ~50%   | 远处目标看不见          |
| 降分辨率      | ~75%   | 小目标、细车道线精度下降 |
| 抽帧 1/2      |  50%   | 高速时滞后，需跟踪补偿  |
    """)


def demo_ros2_messages():
    """ROS 2 消息类型：Image vs OccupancyGrid"""
    print("\n" + "=" * 60)
    print("4. ROS 2 消息类型对比")
    print("=" * 60)
    
    print("""
sensor_msgs/Image:
  - 传图像/掩膜 (640x480 mono8 = 307 KB)
  - 字段: height, width, encoding, data[]
  - QoS: BEST_EFFORT (丢帧不阻塞)

nav_msgs/OccupancyGrid:
  - 传栅格地图 (40x20 = 800 字节！)
  - 字段: info.resolution, info.width/height, data[]
  - 值: 0=空闲, 100=占用, -1=未知
  - 极其省带宽，规划模块最爱
    """)
    
    # 模拟生成 OccupancyGrid 数据
    mask = np.zeros((480, 640), dtype=np.uint8)
    mask[240:, 100:540] = 255  # 模拟路面掩膜
    
    GRID_W, GRID_H = 40, 20
    RES = 0.1  # 米/格
    
    # 缩放掩膜到栅格尺寸
    small = cv2.resize(mask, (GRID_W, GRID_H), interpolation=cv2.INTER_AREA)
    # 0=可行驶(空闲), 100=占用, -1=未知
    data = np.where(small > 127, 0, 100).astype(np.int8)
    
    print(f"栅格地图: {GRID_W}x{GRID_H}, 分辨率 {RES}m")
    print(f"数据大小: {len(data.ravel())} 字节 (vs Image 307 KB)")
    print(f"可行驶格子数: {(data==0).sum()}, 占用格子数: {(data==100).sum()}")


def demo_latency_measurement():
    """延迟与帧率量化：P95 才是靠谱指标"""
    print("\n" + "=" * 60)
    print("5. 延迟与帧率量化")
    print("=" * 60)
    
    # 模拟 100 帧的端到端延迟
    np.random.seed(42)
    # 正态分布 + 偶发长尾
    latencies = np.random.normal(20, 5, 95)  # 95% 帧约 20ms
    latencies = np.append(latencies, np.random.uniform(50, 100, 5))  # 5% 抖动帧
    
    print(f"帧数: {len(latencies)}")
    print(f"平均耗时: {latencies.mean():.1f} ms  -> 平均 {1000/latencies.mean():.1f} FPS")
    print(f"最大耗时: {latencies.max():.1f} ms")
    print(f"P50 耗时:  {np.percentile(latencies, 50):.1f} ms")
    print(f"P95 耗时:  {np.percentile(latencies, 95):.1f} ms  ← 95% 帧都比它快")
    print(f"P99 耗时:  {np.percentile(latencies, 99):.1f} ms")
    
    print("""
为什么看 P95 而不是平均？
- 控制环最怕"偶发卡顿"：平均 20ms 但每 20 帧抖一下 200ms，车就画龙了
- P95 意味着"95% 的帧都在这条线以内"，做验收标准比平均值靠谱

工程验收标准：
- 处理帧率 ≥ 15 FPS
- 单帧耗时 ≤ 66 ms (P95)
- 端到端延迟 ≤ 150 ms
    """)


def demo_perception_node_structure():
    """完整感知节点结构伪代码"""
    print("\n" + "=" * 60)
    print("6. 完整感知节点结构 (perception_node.py)")
    print("=" * 60)
    
    node_code = '''
import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from nav_msgs.msg import OccupancyGrid
from cv_bridge import CvBridge

GRID_W, GRID_H = 40, 20
RES = 0.1

class PerceptionNode(Node):
    def __init__(self):
        super().__init__("drivable_perception")
        self.bridge = CvBridge()
        
        # 传感器数据用 BEST_EFFORT：丢一两帧没关系，绝不阻塞
        qos = QoSProfile(depth=1,
                         reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST)
        
        self.pub_img = self.create_publisher(Image, "/perception/drivable_mask", qos)
        self.pub_grid = self.create_publisher(OccupancyGrid, "/perception/occupancy", qos)
        self.pub_raw = self.create_publisher(Image, "/perception/debug_view", qos)
        
        self.create_timer(1.0 / 15.0, self.timer_cb)  # 15 Hz 处理
        self.cap = cv2.VideoCapture(0)
        self.frames = 0
    
    def segment(self, img):
        """第 03 讲的最简方案"""
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        roi = blur[h//2:, :]
        _, binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        seed = binary[-60:, w//2-30:w//2+30]
        if (seed > 0).mean() < 0.5:
            binary = cv2.bitwise_not(binary)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
        mask = np.zeros((h, w), np.uint8)
        if num > 1:
            biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            mask[h//2:, :] = np.where(labels == biggest, 255, 0).astype(np.uint8)
        return mask
    
    def timer_cb(self):
        ok, frame = self.cap.read()
        if not ok: return
        self.frames += 1
        
        # 三大省算力手段
        frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        mask = self.segment(frame)
        
        # 1) 发布掩膜图
        img_msg = self.bridge.cv2_to_imgmsg(mask, encoding="mono8")
        img_msg.header.stamp = self.get_clock().now().to_msg()
        img_msg.header.frame_id = "camera_link"
        self.pub_img.publish(img_msg)
        
        # 2) 发布占据栅格
        small = cv2.resize(mask, (GRID_W, GRID_H), interpolation=cv2.INTER_AREA)
        grid = OccupancyGrid()
        grid.header = img_msg.header
        grid.info.resolution = RES
        grid.info.width = GRID_W
        grid.info.height = GRID_H
        grid.info.origin.position.x = -GRID_W * RES / 2.0
        grid.info.origin.position.y = -GRID_H * RES
        data = np.where(small > 127, 0, 100).astype(np.int8)
        grid.data = data.ravel().tolist()
        self.pub_grid.publish(grid)
        
        # 3) 发布调试图
        overlay = frame.copy()
        overlay[mask > 0] = (0, 255, 0)
        vis = cv2.addWeighted(frame, 0.6, overlay, 0.4, 0)
        self.pub_raw.publish(self.bridge.cv2_to_imgmsg(vis, encoding="bgr8"))

def main():
    rclpy.init()
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        node.destroy_node()
        rclpy.shutdown()
'''
    print(node_code)
    
    print("""
运行依赖：
  sudo apt install -y ros-humble-cv-bridge ros-humble-vision-msgs
  source /opt/ros/humble/setup.bash
  python3 perception_node.py

验证：
  ros2 topic hz /perception/drivable_mask   # 应约 15 Hz
  ros2 topic echo /perception/occupancy --once
  ros2 run rqt_image_view rqt_image_view    # 看 /perception/debug_view

⚠️ 坑：cv_bridge 与 pip 版 opencv-python 冲突
     解决：统一用 ROS 自带的 python3-opencv (apt install)
    """)


def demo_benchmark_script():
    """基准测试脚本：量化不同配置下的性能"""
    print("\n" + "=" * 60)
    print("7. 基准测试脚本 (填表得实证)")
    print("=" * 60)
    
    benchmark_code = '''
import time
import numpy as np
import cv2

def segment(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    roi = blur[h//2:, :]
    _, binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    seed = binary[-60:, w//2-30:w//2+30]
    if (seed > 0).mean() < 0.5:
        binary = cv2.bitwise_not(binary)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(closed, 8)
    mask = np.zeros((h, w), np.uint8)
    if num > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        mask[h//2:, :] = np.where(labels == biggest, 255, 0).astype(np.uint8)
    return mask

cap = cv2.VideoCapture(0)
configs = [
    ("640x480 全图", lambda f: f),
    ("640x480 + ROI 下半", lambda f: f[f.shape[0]//2:, :]),
    ("320x240 + ROI 下半", lambda f: cv2.resize(f, (320,240))[120:, :]),
    ("320x240 + ROI + 抽帧1/2", lambda f: cv2.resize(f, (320,240))[120:, :]),
]

print(f"{'配置':<25} {'平均耗时':>10} {'P95':>8} {'平均FPS':>10}")
print("-" * 55)

for name, preprocess in configs:
    latencies = []
    frame_id = 0
    for _ in range(100):
        ok, frame = cap.read()
        if not ok: break
        frame_id += 1
        
        # 抽帧逻辑
        if "抽帧" in name and frame_id % 2 == 0:
            continue
            
        t0 = time.perf_counter()
        processed = preprocess(frame)
        _ = segment(processed)
        latencies.append((time.perf_counter() - t0) * 1000)
    
    lat = np.array(latencies)
    print(f"{name:<25} {lat.mean():>10.1f} {np.percentile(lat,95):>8.1f} {1000/lat.mean():>10.1f}")

cap.release()
'''
    print(benchmark_code)
    
    print("""
预期结果（每加一个手段，耗时明显下降）：
| 配置                    | 平均耗时 | P95   | 平均 FPS |
|-------------------------|----------|-------|----------|
| 640x480 全图            | ~40ms    | ~55ms | ~25      |
| 640x480 + ROI 下半      | ~20ms    | ~28ms | ~50      |
| 320x240 + ROI 下半      | ~6ms     | ~9ms  | ~160     |
| 320x240 + ROI + 抽帧 1/2| ~3ms*    | ~5ms* | ~320*    |
(* 抽帧时实际处理帧率减半，但单帧耗时更低)

把这张表贴上，就是"算力优化"最有力的实证。
    """)


if __name__ == "__main__":
    demo_camera_calibration()
    demo_undistort()
    demo_performance_tricks()
    demo_ros2_messages()
    demo_latency_measurement()
    demo_perception_node_structure()
    demo_benchmark_script()
    
    print("\n" + "=" * 60)
    print("完整感知流水线总结")
    print("=" * 60)
    print("""
采集 -> 去畸变 -> 预处理(降分辨率/ROI/抽帧) -> 感知算法 -> 后处理 -> ROS2发布 -> 规划

关键点：
1. 标定一次，参数存 .npz，启动加载
2. 去畸变用 remap 查表，别每帧 undistort
3. 三大省算力手段：ROI、降分辨率、抽帧
4. 发布两路：Image(掩膜/调试) + OccupancyGrid(规划用)
5. 量化看 P95，验收标准：≥15FPS, P95≤66ms, 端到端≤150ms
6. 统计耗时必须从 cap.read() 到 publish 全链路
    """)