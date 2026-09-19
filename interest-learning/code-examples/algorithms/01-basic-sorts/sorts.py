#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本排序算法：冒泡、选择、插入
对应教程：interest-learning/autonomous-driving/algorithms/01-排序问题与三种直观解法.md

每个排序函数都接收列表，返回新的已排序列表（不修改原始数据）
"""

import random
import time


def bubble_sort(a):
    """
    冒泡排序：相邻两两比较，大的往右挪
    - 时间复杂度：平均 O(n²)，最好 O(n)（已有序时提前结束）
    - 空间复杂度：O(1)
    - 稳定性：稳定
    """
    a = a[:]  # 复制列表，避免修改原始数据
    n = len(a)
    for i in range(n - 1):
        swapped = False
        # 每轮把最大的"冒泡"到末尾，所以内层范围逐渐缩小
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        # 如果某一轮完全没有交换，说明已经有序，提前结束
        if not swapped:
            break
    return a


def selection_sort(a):
    """
    选择排序：每轮在未排序区找最小值，放到已排序区末尾
    - 时间复杂度：固定 O(n²)（与输入顺序无关）
    - 空间复杂度：O(1)
    - 稳定性：不稳定（交换会跨过相等元素）
    """
    a = a[:]
    n = len(a)
    for i in range(n - 1):
        k = i  # 记录最小值的位置
        for j in range(i + 1, n):
            if a[j] < a[k]:
                k = j
        # 将找到的最小值与当前位置交换
        a[i], a[k] = a[k], a[i]
    return a


def insertion_sort(a):
    """
    插入排序：像整理扑克牌，将当前元素插入到前面已排序区间的合适位置
    - 时间复杂度：平均 O(n²)，最好 O(n)（接近有序时极快）
    - 空间复杂度：O(1)
    - 稳定性：稳定
    """
    a = a[:]
    n = len(a)
    for i in range(1, n):
        key = a[i]  # 取出当前要插入的元素
        j = i - 1
        # 在已排序区从右向左扫描，腾出位置
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key  # 插入到正确位置
    return a


def benchmark_sorts():
    """基准测试：对比三种排序在不同数据规模下的耗时"""
    print("=== 排序算法基准测试 ===\n")
    
    for n in [1000, 5000]:
        # 生成相同的随机数据用于公平对比
        random.seed(42)
        data = [random.randint(0, 100000) for _ in range(n)]
        
        print(f"--- n = {n} ---")
        
        for name, fn in [
            ("冒泡排序", bubble_sort),
            ("选择排序", selection_sort),
            ("插入排序", insertion_sort),
        ]:
            # 多次运行取最小值，减少系统抖动影响
            times = []
            for _ in range(3):
                t0 = time.perf_counter()
                fn(data)
                times.append(time.perf_counter() - t0)
            print(f"  {name:6s}: {min(times):.4f} s (3次取最快)")
        
        # 内置排序作为基准
        t0 = time.perf_counter()
        sorted(data)
        print(f"  {'内置sorted':6s}: {time.perf_counter() - t0:.4f} s")
        print()


def test_stability():
    """稳定性测试：使用元组 (关键字, 标记) 验证相等元素相对顺序是否保持"""
    print("=== 稳定性测试 ===\n")
    
    # 测试用例 1：两个相同关键字，按标记区分
    data1 = [(1, 'a'), (1, 'b'), (0, 'c')]
    
    # 测试用例 2：多个相同关键字
    data2 = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
    
    for name, fn in [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
    ]:
        result1 = fn(data1)
        result2 = fn(data2)
        print(f"{name}:")
        print(f"  输入1: {data1}")
        print(f"  输出1: {result1}  {'✓ 稳定' if result1 == [(0,'c'),(1,'a'),(1,'b')] else '✗ 不稳定'}")
        print(f"  输入2: {data2}")
        print(f"  输出2: {result2}  {'✓ 稳定' if result2 == [(1,'b'),(1,'d'),(2,'a'),(2,'c')] else '✗ 不稳定'}")
        print()


if __name__ == "__main__":
    # 1. 基本功能演示
    random.seed(1)
    data = [random.randint(1, 99) for _ in range(10)]
    print("原始数据:", data)
    print("冒泡排序:", bubble_sort(data))
    print("选择排序:", selection_sort(data))
    print("插入排序:", insertion_sort(data))
    print()
    
    # 2. 稳定性测试
    test_stability()
    
    # 3. 性能基准测试
    benchmark_sorts()
    
    # 4. 展示有序输入下的表现差异
    print("=== 有序输入对比 ===")
    for n in [5000]:
        data = list(range(n))
        for name, fn in [("冒泡", bubble_sort), ("插入", insertion_sort), ("选择", selection_sort)]:
            t0 = time.perf_counter()
            fn(data)
            print(f"  {name}排序 (有序输入 n={n}): {time.perf_counter() - t0:.4f} s")