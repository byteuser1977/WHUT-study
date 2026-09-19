#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排序算法综合基准测试：对比 5 种手写排序 + 内置排序
对应教程：interest-learning/autonomous-driving/algorithms/03-算法怎么选与实测对比.md
"""

import random
import time
import sys


# ===== 第 1 讲：基本排序 =====
def bubble_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def selection_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n - 1):
        k = i
        for j in range(i + 1, n):
            if a[j] < a[k]:
                k = j
        a[i], a[k] = a[k], a[i]
    return a


def insertion_sort(a):
    a = a[:]
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ===== 第 2 讲：分治排序 =====
def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[0]
    less = [x for x in a[1:] if x <= pivot]
    greater = [x for x in a[1:] if x > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def benchmark_all():
    """完整基准测试：随机数据 + 有序数据"""
    print("=" * 60)
    print("排序算法综合基准测试")
    print("=" * 60)
    
    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
        ("快速排序", quick_sort),
        ("归并排序", merge_sort),
        ("内置 sorted", sorted),
    ]
    
    # 测试 1：随机数据
    print("\n【测试 1：随机整数数据】")
    print("-" * 60)
    for n in [1000, 5000]:
        random.seed(42)
        data = [random.randint(0, 100000) for _ in range(n)]
        print(f"\n>>> n = {n}")
        print(f"{'算法':<12} {'耗时(ms)':>10} {'相对内置':>10}")
        print("-" * 40)
        
        baseline = None
        for name, fn in algorithms:
            times = []
            for _ in range(3):
                t0 = time.perf_counter()
                fn(data)
                times.append(time.perf_counter() - t0)
            best = min(times) * 1000  # 转毫秒
            if name == "内置 sorted":
                baseline = best
            ratio = best / baseline if baseline else 1
            print(f"{name:<12} {best:>10.2f} {ratio:>9.1f}x")
    
    # 测试 2：已有序数据（最坏/最好情况对比）
    print("\n\n【测试 2：已有序数据】")
    print("-" * 60)
    for n in [5000]:
        data = list(range(n))
        print(f"\n>>> n = {n} (已升序)")
        print(f"{'算法':<12} {'耗时(ms)':>10} {'说明':>30}")
        print("-" * 60)
        
        for name, fn in algorithms:
            if name == "快速排序" and n > 1000:
                print(f"{name:<12} {'RecursionError':>10} {'递归深度超限':>30}")
                continue
            t0 = time.perf_counter()
            fn(data)
            elapsed = (time.perf_counter() - t0) * 1000
            note = ""
            if name == "冒泡排序":
                note = "最好情况 O(n)"
            elif name == "插入排序":
                note = "最好情况 O(n)"
            elif name == "选择排序":
                note = "无视输入顺序 O(n²)"
            elif name == "快速排序":
                note = "最坏情况 O(n²) 退化"
            elif name == "归并排序":
                note = "稳定 O(n log n)"
            print(f"{name:<12} {elapsed:>10.2f} {note:>30}")
    
    # 测试 3：逆序数据
    print("\n\n【测试 3：逆序数据】")
    print("-" * 60)
    for n in [5000]:
        data = list(range(n, 0, -1))
        print(f"\n>>> n = {n} (降序)")
        for name, fn in algorithms:
            if name == "快速排序" and n > 1000:
                print(f"{name:<12} {'RecursionError':>10}")
                continue
            t0 = time.perf_counter()
            fn(data)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"{name:<12} {elapsed:>10.2f} ms")
    
    # 测试 4：部分有序数据（模拟真实场景）
    print("\n\n【测试 4：部分有序数据 (90%有序 + 10%随机)】")
    print("-" * 60)
    for n in [5000]:
        data = list(range(int(n * 0.9)))
        random.shuffle(data[:int(n * 0.1)])
        random.seed(42)
        data.extend([random.randint(0, 100000) for _ in range(n - len(data))])
        print(f"\n>>> n = {n}")
        for name, fn in algorithms:
            if name == "快速排序" and n > 1000:
                print(f"{name:<12} {'RecursionError':>10}")
                continue
            t0 = time.perf_counter()
            fn(data)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"{name:<12} {elapsed:>10.2f} ms")
    
    # 测试 5：大量重复元素
    print("\n\n【测试 5：大量重复元素】")
    print("-" * 60)
    for n in [5000]:
        random.seed(42)
        # 只有 10 个不同值
        data = [random.randint(0, 9) for _ in range(n)]
        print(f"\n>>> n = {n} (仅 10 个不同值)")
        for name, fn in algorithms:
            if name == "快速排序" and n > 1000:
                print(f"{name:<12} {'RecursionError':>10}")
                continue
            t0 = time.perf_counter()
            fn(data)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"{name:<12} {elapsed:>10.2f} ms")


def test_stability_comprehensive():
    """全面稳定性测试"""
    print("\n\n" + "=" * 60)
    print("稳定性综合测试")
    print("=" * 60)
    
    test_cases = [
        ("简单相等键", [(1, 'a'), (1, 'b'), (0, 'c')]),
        ("多组相等键", [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]),
        ("三组相等键", [(3, 'x'), (1, 'a'), (2, 'b'), (3, 'y'), (1, 'c'), (2, 'd')]),
    ]
    
    for case_name, data in test_cases:
        print(f"\n--- {case_name}: {data} ---")
        for name, fn in [
            ("冒泡", bubble_sort),
            ("选择", selection_sort),
            ("插入", insertion_sort),
            ("快速", quick_sort),
            ("归并", merge_sort),
        ]:
            result = fn(data)
            # 检查相等键的相对顺序
            stable = True
            for i in range(len(result) - 1):
                for j in range(i + 1, len(result)):
                    if result[i][0] == result[j][0]:
                        # 在原数组中找这两个元素的原始位置
                        orig_i = data.index(result[i])
                        orig_j = data.index(result[j])
                        if orig_i > orig_j:
                            stable = False
            status = "✓ 稳定" if stable else "✗ 不稳定"
            print(f"  {name:4s}: {result}  {status}")


def verify_correctness():
    """正确性验证：所有算法输出应一致"""
    print("\n\n" + "=" * 60)
    print("正确性验证")
    print("=" * 60)
    
    test_arrays = [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 2, 8, 1, 9, 3],
        [1, 1, 1, 1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
    ]
    
    for arr in test_arrays:
        expected = sorted(arr)
        results = {}
        for name, fn in [
            ("冒泡", bubble_sort),
            ("选择", selection_sort),
            ("插入", insertion_sort),
            ("快速", quick_sort),
            ("归并", merge_sort),
        ]:
            results[name] = fn(arr)
        
        all_ok = all(r == expected for r in results.values())
        status = "✓" if all_ok else "✗"
        if not all_ok:
            print(f"输入: {arr}")
            for name, res in results.items():
                mark = "✓" if res == expected else "✗"
                print(f"  {name:4s}: {res} {mark}")
        else:
            print(f"{status} {arr} -> {expected}")


def show_complexity_summary():
    """打印复杂度总结表"""
    print("\n\n" + "=" * 60)
    print("算法复杂度总结表")
    print("=" * 60)
    print(f"{'算法':<12} {'平均':>10} {'最坏':>10} {'最好':>10} {'空间':>8} {'稳定性':>6}")
    print("-" * 60)
    rows = [
        ("冒泡", "O(n²)", "O(n²)", "O(n)", "O(1)", "稳定"),
        ("选择", "O(n²)", "O(n²)", "O(n²)", "O(1)", "不稳定"),
        ("插入", "O(n²)", "O(n²)", "O(n)", "O(1)", "稳定"),
        ("快速", "O(n log n)", "O(n²)", "O(n log n)", "O(log n)", "不稳定"),
        ("归并", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "稳定"),
        ("Timsort", "O(n log n)", "O(n log n)", "O(n)", "O(n)", "稳定"),
    ]
    for name, avg, worst, best, space, stable in rows:
        print(f"{name:<12} {avg:>10} {worst:>10} {best:>10} {space:>8} {stable:>6}")
    
    print("\n注：")
    print("- Timsort = Python 内置 sorted() 使用的算法（归并+插入混合）")
    print("- 快速排序最坏情况可通过随机基准/三数取中避免")
    print("- 空间复杂度不含输入数组本身")


if __name__ == "__main__":
    verify_correctness()
    benchmark_all()
    test_stability_comprehensive()
    show_complexity_summary()
    
    print("\n\n=== 结论 ===")
    print("1. 小规模/近似有序：插入排序最快")
    print("2. 通用场景：内置 sorted() (Timsort) 最快且稳定")
    print("3. 需要稳定且保证 O(n log n)：归并排序")
    print("4. 平均最快但可能退化：快速排序（工程上常用三数取中优化）")
    print("5. 教学/极小数据/内存极限：选择/冒泡/插入")