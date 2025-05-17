import streamlit as st
import sys
import time
from io import StringIO

# Sorting Algorithms
def insertion_sort(arr):
    print(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        print(arr)
    return arr

def selection_sort(arr):
    print(arr)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(arr)
    return arr

def bubble_sort(arr):
    print(arr)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(arr)
    return arr

def quick_sort(arr, start=0, end=None):
    if end is None:
        end = len(arr) - 1

    if start < end:
        pivot = arr[end]
        i = start
        for j in range(start, end):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                print(arr)
                i += 1
        arr[i], arr[end] = arr[end], arr[i]
        print(arr)
        quick_sort(arr, start, i - 1)
        quick_sort(arr, i + 1, end)
    return arr

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    print(result)
    return result

def merge_sort(arr):
    print(arr)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# Streamlit UI
st.title("📊 Sorting Algorithm Visualizer")

user_input = st.text_input("Enter a list of numbers (comma-separated):", "12, 11, 13, 5, 6")

algorithm = st.selectbox("Choose a sorting algorithm:", [
    "Insertion Sort", "Selection Sort", "Bubble Sort", "Quick Sort", "Merge Sort"
])

if st.button("Sort"):
    try:
        arr = [int(x.strip()) for x in user_input.split(",")]

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        start_time = time.perf_counter()

        if algorithm == "Insertion Sort":
            sorted_arr = insertion_sort(arr.copy())
        elif algorithm == "Selection Sort":
            sorted_arr = selection_sort(arr.copy())
        elif algorithm == "Bubble Sort":
            sorted_arr = bubble_sort(arr.copy())
        elif algorithm == "Quick Sort":
            sorted_arr = quick_sort(arr.copy())
        elif algorithm == "Merge Sort":
            sorted_arr = merge_sort(arr.copy())

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        sys.stdout = old_stdout  # Reset stdout

        output = mystdout.getvalue()

        # Display results
        st.text_area("🔍 Sorting Steps", output, height=400)
        st.success(f"✅ Sorted Result: {sorted_arr}")
        st.info(f"⏱️ Time taken: {elapsed_time:.6f} seconds")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")