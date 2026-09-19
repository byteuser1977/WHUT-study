#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分治排序算法：快速排序、归并排序
对应教程：interest-learning/autonomous-driving/algorithms/02-更快的排序与分治思想.md
"""

import random
import time


def quick_sort(a):
    """
    快速排序（函数式写法，非原地）：
    1. 选取基准
    2. 将数组分为：小于等于基准、大于基准
    3. 递归排序两部分并拼接

    - 时间复杂度：平均 O(n log n)，最坏 O(n²)（已有序+首元素作基准）
    - 空间复杂度：O(log n) 递归栈（此实现因列表推导式额外 O(n)）
    - 稳定性：不稳定
    """
    if len(a) <= 1:
        return a
    pivot = a[0]
    less = [x for x in a[1:] if x <= pivot]
    greater = [x for x in a[1:] if x > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)


def quick_sort_inplace(a, low=0, high=None):
    """
    快速排序（原地版本，省空间）
    使用 Hoare 分区方案
    """
    if high is None:
        high = len(a) - 1
    if low < high:
        pi = partition(a, low, high)
        quick_sort_inplace(a, low, pi - 1)
        quick_sort_inplace(a, pi + 1, high)


def partition(a, low, high):
    """分区：选取中间元素作基准，返回基准最终位置"""
    mid = (low + high) // 2
    a[mid], a[high] = a[high], a[mid]  # 基准移到末尾
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def merge_sort(a):
    """
    归并排序：分治 + 线性合并
    1. 递归拆分到单元素
    2. 合并两个有序数组（双指针）

    - 时间复杂度：稳定 O(n log n)
    - 空间复杂度：O(n) 额外数组
    - 稳定性：稳定（合并时 left[i] <= right[j] 优先取左）
    """
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])

    # 合并两个有序数组
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= 保证稳定性
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def merge_sort_inplace(a, temp=None, left=0, right=None):
    """
    归并排序（原地优化版，复用临时数组）
    """
    if right is None:
        right = len(a) - 1
        temp = [0] * len(a)
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(a, temp, left, mid)
        merge_sort_inplace(a, temp, mid + 1, right)
        merge(a, temp, left, mid, right)


def merge(a, temp, left, mid, right):
    """合并 a[left:mid+1] 和 a[mid+1:right+1]"""
    i, j, k = left, mid + 1, left
    while i <= mid and j <= right:
        if a[i] <= a[j]:
            temp[k] = a[i]
            i += 1
        else:
            temp[k] = a[j]
            j += 1
        k += 1
    while i <= mid:
        temp[k] = a[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = a[j]
        j += 1
        k += 1
    for idx in range(left, right + 1):
        a[idx] = temp[idx]


def test_stability():
    """稳定性测试：验证归并稳定、快排不稳定"""
    print("=== 稳定性测试 ===\n")

    # 只有关键字相同时才能看出稳定性，所以用 (key, label) 形式
    data1 = [(1, 'a'), (1, 'b'), (0, 'c')]
    data2 = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]

    print("输入1:", data1)
    print("输入2:", data2)
    print()

    # 快排（函数式）
    result = quick_sort(data1)
    print(f"快排(函数式) 输入1: {result}  {'✓' if result == [(0,'c'),(1,'a'),(1,'b')] else '✗ 不稳定'}")
    result = quick_sort(data2)
    print(f"快排(函数式) 输入2: {result}  {'✓' if result == [(1,'b'),(1,'d'),(2,'a'),(2,'c')] else '✗ 不稳定'}")

    # 归并
    result = merge_sort(data1)
    print(f"归并排序    输入1: {result}  {'✓ 稳定' if result == [(0,'c'),(1,'a'),(1,'b')] else '✗'}")
    result = merge_sort(data2)
    print(f"归并排序    输入2: {result}  {'✓ 稳定' if result == [(1,'b'),(1,'d'),(2,'a'),(2,'c')] else '✗'}")
    print()


def benchmark_recursive():
    """基准测试：快排、归并、内置排序对比"""
    print("=== 分治排序基准测试 ===\n")

    for n in [1000, 5000, 10000]:
        random.seed(42)
        data = [random.randint(0, 100000) for _ in range(n)]

        print(f"--- n = {n} (随机数据) ---")

        for name, fn in [
            ("快排(函数式)", quick_sort),
            ("归并排序", merge_sort),
            ("内置sorted", sorted),
        ]:
            times = []
            for _ in range(3):
                t0 = time.perf_counter()
                fn(data)
                times.append(time.perf_counter() - t0)
            print(f"  {name:10s}: {min(times):.4f} s")
        print()

    # 最坏情况测试：已有序输入
    print("--- 最坏情况：已有序输入 ---")
    for n in [500, 1000, 2000, 4000]:
        data = list(range(n))
        t0 = time.perf_counter()
        try:
            quick_sort(data)  # 函数式快排在已有序时退化
            elapsed = time.perf_counter() - t0
            print(f"  快排 n={n:4d}: {elapsed:.4f} s (每倍增约 4x = O(n²))")
        except RecursionError:
            print(f"  快排 n={n:4d}: RecursionError - 递归深度超限！(这就是最坏情况)")
            break  # 更大的 n 肯定也会超限

    # 归并排序不会有这个问题
    data = list(range(10000))
    t0 = time.perf_counter()
    merge_sort(data)
    print(f"  归并 n=10000: {time.perf_counter() - t0:.4f} s (递归深度仅 ~14，无问题)")

    # 递归深度测试
    print("\n=== 递归深度测试 ===")
    import sys
    print(f"Python 默认递归限制: {sys.getrecursionlimit()}")

    for n in [500, 1000]:
        data = list(range(n))
        try:
            t0 = time.perf_counter()
            quick_sort(data)
            print(f"  快排 n={n}: {time.perf_counter() - t0:.4f} s")
        except RecursionError:
            print(f"  快排 n={n}: RecursionError - 递归深度超限！(这就是最坏情况)")

    data = list(range(10000))
    t0 = time.perf_counter()
    merge_sort(data)
    print(f"  归并 n=10000: {time.perf_counter() - t0:.4f} s (递归深度仅 ~14，无问题)")

    print("\n  提示：工程上用随机基准或三数取中可避免最坏情况")


if __name__ == "__main__":
    # 1. 基本功能演示
    random.seed(1)
    data = [random.randint(1, 99) for _ in range(10)]
    print("原始数据:", data)
    print("快速排序:", quick_sort(data))
    print("归并排序:", merge_sort(data))
    print()

    # 2. 稳定性测试
    test_stability()

    # 3. 性能基准
    benchmark_recursive()

    # 4. 原地版本验证
    print("\n=== 原地版本验证 ===")
    test_data = [3, 1, 4, 1, 5, 9, 2, 6]
    arr1 = test_data[:]
    quick_sort_inplace(arr1)
    print("快排原地版:", arr1)

    arr2 = test_data[:]
    merge_sort_inplace(arr2)
    print("归并原地版:", arr2)