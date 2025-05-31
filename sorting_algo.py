import streamlit as st
import sys
import time
from io import StringIO
import matplotlib.pyplot as plt


def record_snapshot(snapshots, arr):
    snapshots.append(arr.copy())

#--------------------------------------------------------------------------------------- Insertion Sort ---------------------------------------------------------------------------------------#

def insertion_sort(arr, snapshots):
    record_snapshot(snapshots, arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            record_snapshot(snapshots, arr)
        arr[j + 1] = key
        record_snapshot(snapshots, arr)
    return arr

#--------------------------------------------------------------------------------------- Selection Sort ---------------------------------------------------------------------------------------#

def selection_sort(arr, snapshots):
    record_snapshot(snapshots, arr)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        record_snapshot(snapshots, arr)
    return arr

#--------------------------------------------------------------------------------------- Bubble Sort ---------------------------------------------------------------------------------------#

def bubble_sort(arr, snapshots):
    record_snapshot(snapshots, arr)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                record_snapshot(snapshots, arr)
    return arr

#--------------------------------------------------------------------------------------- Quick Sort ---------------------------------------------------------------------------------------#

def quick_sort(arr, snapshots, start=0, end=None, first_call=True):
    if first_call:
        record_snapshot(snapshots, arr) 

    if end is None:
        end = len(arr) - 1

    if start < end:
        pivot = arr[end]
        i = start
        for j in range(start, end):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                record_snapshot(snapshots, arr)
                i += 1
        arr[i], arr[end] = arr[end], arr[i]
        record_snapshot(snapshots, arr)

        quick_sort(arr, snapshots, start, i - 1, first_call=False)
        quick_sort(arr, snapshots, i + 1, end, first_call=False)
    
    return arr

#--------------------------------------------------------------------------------------- Merge Sort ---------------------------------------------------------------------------------------#

def merge(left, right, snapshots):
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
    record_snapshot(snapshots, result)
    return result

def merge_sort(arr, snapshots):
    record_snapshot(snapshots, arr)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], snapshots)
    right = merge_sort(arr[mid:], snapshots)
    return merge(left, right, snapshots)

#--------------------------------------------------------------------------------------- UI ---------------------------------------------------------------------------------------#

st.title("📊 Sorting Algorithm Visualizer")

user_input = st.text_input("Enter a list of numbers (comma-separated):", "12, 11, 13, 5, 6")

algorithm = st.selectbox("Choose a sorting algorithm:", [
    "Insertion Sort", "Selection Sort", "Bubble Sort", "Quick Sort", "Merge Sort"
])

if st.button("Sort"):
    try:
        arr = [int(x.strip()) for x in user_input.split(",")]

        # Reset state
        st.session_state.snapshots = []
        st.session_state.step = 0

        snapshots = st.session_state.snapshots
        start_time = time.perf_counter()

        if algorithm == "Insertion Sort":
            sorted_arr = insertion_sort(arr.copy(), snapshots)
        elif algorithm == "Selection Sort":
            sorted_arr = selection_sort(arr.copy(), snapshots)
        elif algorithm == "Bubble Sort":
            sorted_arr = bubble_sort(arr.copy(), snapshots)
        elif algorithm == "Quick Sort":
            sorted_arr = quick_sort(arr.copy(), snapshots, first_call=True)
        elif algorithm == "Merge Sort":
            sorted_arr = merge_sort(arr.copy(), snapshots)

        end_time = time.perf_counter()
        st.session_state.sorted_arr = sorted_arr
        st.session_state.time_taken = end_time - start_time

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Navigation buttons
if "snapshots" in st.session_state and st.session_state.snapshots:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous") and st.session_state.step > 0:
            st.session_state.step -= 1
    with col3:
        if st.button("Next ➡️") and st.session_state.step < len(st.session_state.snapshots) - 1:
            st.session_state.step += 1

    # Plot current snapshot using matplotlib
    step = st.session_state.step
    current_snapshot = st.session_state.snapshots[step]

    fig, ax = plt.subplots()
    ax.bar([str(x) for x in current_snapshot], current_snapshot)
    ax.set_title(f"Step {step + 1} of {len(st.session_state.snapshots)}")
    ax.set_xlabel("Values")
    ax.set_ylabel("Height")
    st.pyplot(fig)

    st.info(f"⏱️ Time taken: {st.session_state.time_taken:.6f} seconds")
    st.success(f"✅ Sorted Result: {st.session_state.sorted_arr}")
