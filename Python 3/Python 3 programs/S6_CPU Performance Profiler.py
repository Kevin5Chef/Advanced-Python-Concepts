import tkinter as tk
from tkinter import ttk
import threading
import random
import time
import tracemalloc
import cProfile
import pstats
import io
import numpy as np
import psutil
print("SY-5, Kevin Victor, Roll No.-30")
# ---------------- HEAVY TASKS (TUNED TO ~3 SEC) ----------------

def generate_shapes(n=7000):
    shapes = []
    for _ in range(n):
        shapes.append((
            random.random(),
            random.random(),
            random.randint(0,255)
        ))
    return shapes


def generate_textures(n=3500):
    textures = []
    for _ in range(n):
        arr = np.random.rand(45,45)
        textures.append(np.sin(arr) * np.cos(arr))
    return textures


def matrix_multiply_heavy(n=30, loops=85):
    A = np.random.rand(n,n)
    B = np.random.rand(n,n)
    for _ in range(loops):
        A = np.dot(A,B)
    return A


# ---------------- BOTTLENECK ANALYZER ----------------

def print_bottleneck(stats_text):

    print("\n[PROFILE] Top cumulative-time functions")
    print("----------------------------------------")

    lines = stats_text.splitlines()
    for line in lines[:15]:
        print(line)

    print("\n[DIAGNOSTIC]")

    if "matrix_multiply_heavy" in stats_text:
        print("[BOTTLENECK] MATMUL_CORE")
        print("[CAUSE] Deep iterative matrix multiplication")
        print("[FIX] Use multiprocessing / GPU / reduce loops")

    elif "generate_textures" in stats_text:
        print("[BOTTLENECK] TEX_SIM")
        print("[CAUSE] High trig ops on arrays")
        print("[FIX] Lower resolution OR batch compute")

    else:
        print("[BOTTLENECK] GEN_MISC")
        print("[CAUSE] Python loop overhead")
        print("[FIX] Vectorize / use C-backed ops")


# ---------------- MAIN APP ----------------

class ProfilerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CPU Simulation Dashboard")
        self.root.geometry("620x420")

        tk.Label(root,text="Heavy Simulation Monitor",
                 font=("Arial",16,"bold")).pack(pady=10)

        self.status = tk.StringVar(value="Idle")
        tk.Label(root,textvariable=self.status).pack()

        self.time_label = tk.Label(root,text="Execution Time: -")
        self.time_label.pack()

        self.cpu_label = tk.Label(root,text="CPU Usage: -")
        self.cpu_label.pack()

        self.mem_label = tk.Label(root,text="Memory Usage: -")
        self.mem_label.pack()

        self.progress = ttk.Progressbar(root,length=300,mode="determinate")
        self.progress.pack(pady=10)

        ttk.Button(root,text="Run Simulation",
                   command=self.start_thread).pack()

    # ---------- THREAD ----------
    def start_thread(self):
        thread = threading.Thread(target=self.run_profiled_task)
        thread.start()

    # ---------- TASK ----------
    def run_profiled_task(self):

        self.status.set("Running: Shapes")
        self.progress["value"] = 0

        tracemalloc.start()
        start = time.time()

        profiler = cProfile.Profile()
        profiler.enable()

        generate_shapes()
        self.progress["value"] = 33
        self.root.update_idletasks()

        self.status.set("Running: Textures")
        generate_textures()
        self.progress["value"] = 66
        self.root.update_idletasks()

        self.status.set("Running: Matrix Core")
        matrix_multiply_heavy()

        profiler.disable()

        end = time.time()
        exec_time = round(end-start,3)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        cpu = psutil.cpu_percent()
        mem = round(peak/1024/1024,2)

        self.progress["value"] = 100
        self.status.set("Completed")

        # ---------- PROFILE TO TERMINAL ----------
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumtime')
        ps.print_stats(10)

        stats_text = s.getvalue()

        print("\n================ PERFORMANCE REPORT ================")
        print(f"[TIME] {exec_time} sec")
        print(f"[CPU] {cpu}%")
        print(f"[MEMORY PEAK] {mem} MB")

        print_bottleneck(stats_text)
        print("====================================================\n")

        # ---------- UPDATE GUI ----------
        self.time_label.config(text=f"Execution Time: {exec_time}s")
        self.cpu_label.config(text=f"CPU Usage: {cpu}%")
        self.mem_label.config(text=f"Memory Usage Peak: {mem} MB")


# ---------------- RUN ----------------
root = tk.Tk()
app = ProfilerApp(root)
root.mainloop()
