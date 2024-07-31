import threading
import random
import time
import matplotlib.pyplot as plt

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    print("bubleSort")            

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = arr[l:m+1]
    R = arr[m+1:r+1]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
    print("Merge")

def merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)
        print("Merge_sort")

def parallel_merge_sort(arr, l, r, n_threads):
    if n_threads <= 1 or l >= r:
        merge_sort(arr, l, r)
    else:
        m = l + (r - l) // 2

        left_thread = threading.Thread(target=parallel_merge_sort, args=(arr, l, m, n_threads // 2))
        right_thread = threading.Thread(target=parallel_merge_sort, args=(arr, m + 1, r, n_threads // 2))

        left_thread.start()
        right_thread.start()

        left_thread.join()
        right_thread.join()

        merge(arr, l, m, r)

def run_experiment(n_threads, use_parallel):
    arr = [random.randint(0, 1000) for _ in range(1000)]
    subarr_len = len(arr) // n_threads
    subarrays = [arr[i*subarr_len:(i+1)*subarr_len] for i in range(n_threads)]

    start_time = time.time()

    if use_parallel:
        threads = []
        for subarr in subarrays:
            thread = threading.Thread(target=bubble_sort, args=(subarr,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        parallel_merge_sort(arr, 0, len(arr) - 1, n_threads)
    else:
        for subarr in subarrays:
            bubble_sort(subarr)

        merge_sort(arr, 0, len(arr) - 1)

    end_time = time.time()

    return end_time - start_time

def main():
    n_values = [1,2,5,8,16]
    sequential_times = []
    parallel_times = []
    print("Koe")
    for n in n_values:
        sequential_time = run_experiment(n, False)
        parallel_time = run_experiment(n, True)

        sequential_times.append(sequential_time)
        parallel_times.append(parallel_time)

    plt.plot(n_values, sequential_times, label="Sequential")
    plt.plot(n_values, parallel_times, label="Parallel")
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
