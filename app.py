import tkinter as tk
from tkinter import ttk
import random
import threading
import time
import csv

THEMES = {
    "Dark": "#1e1e1e",
    "Light": "#ffffff",
    "Blue": "#1a6ec9"
}

COMPLEXITY = {
    "Bubble": "Best O(n) Avg O(n²) Worst O(n²)",
    "Selection": "O(n²)",
    "Insertion": "Best O(n) Worst O(n²)",
    "Merge": "O(n log n)",
    "Quick": "Avg O(n log n) Worst O(n²)",
    "Heap": "O(n log n)",
    "Shell": "~ O(n^1.5)"
}

BAR = "#4FC3F7"
ACTIVE = "#FF5252"
DONE = "#4CAF50"


class SortingVisualizer:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced Sorting Visualizer")
        self.root.geometry("1300x760")

        self.arr = []

        self.paused = False
        self.stopped = False
        self.sorting = False

        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0

        self.build_ui()

        self.generate_array()

    def build_ui(self):

        top = tk.Frame(self.root)
        top.pack(fill="x")

        self.algorithm = tk.StringVar(value="Bubble")

        ttk.Combobox(
            top,
            textvariable=self.algorithm,
            values=[
                "Bubble",
                "Selection",
                "Insertion",
                "Merge",
                "Quick",
                "Heap",
                "Shell"
            ],
            width=12
        ).pack(side="left")

        self.array_mode = tk.StringVar(value="Random")

        ttk.Combobox(
            top,
            textvariable=self.array_mode,
            values=[
                "Random",
                "Sorted",
                "Reverse"
            ],
            width=10
        ).pack(side="left")

        self.size_slider = tk.Scale(
            top,
            from_=10,
            to=120,
            orient="horizontal",
            label="Size"
        )

        self.size_slider.set(50)

        self.size_slider.pack(side="left")

        self.speed = tk.Scale(
            top,
            from_=1,
            to=150,
            orient="horizontal",
            label="Delay"
        )

        self.speed.set(20)

        self.speed.pack(side="left")

        self.manual = tk.Entry(
            top,
            width=25
        )

        self.manual.pack(side="left")

        tk.Button(top,text="Load",command=self.load_manual).pack(side="left")
        tk.Button(top,text="Generate",command=self.generate_array).pack(side="left")
        tk.Button(top,text="Start",command=self.start_sort).pack(side="left")
        tk.Button(top,text="Pause",command=lambda:setattr(self,"paused",True)).pack(side="left")
        tk.Button(top,text="Resume",command=lambda:setattr(self,"paused",False)).pack(side="left")
        tk.Button(top,text="Stop",command=self.stop).pack(side="left")
        tk.Button(top,text="Export",command=self.export_csv).pack(side="left")

        self.theme = tk.StringVar(value="Dark")

        ttk.Combobox(
            top,
            values=list(THEMES.keys()),
            textvariable=self.theme,
            width=10
        ).pack(side="left")

        tk.Button(
            top,
            text="Theme",
            command=self.apply_theme
        ).pack(side="left")

        self.canvas = tk.Canvas(
            self.root,
            width=1250,
            height=520,
            bg="black"
        )

        self.canvas.pack()

        self.stats = tk.Label(self.root)
        self.stats.pack()

        self.comp = tk.Label(self.root)
        self.comp.pack()

        self.progress = ttk.Progressbar(
            self.root,
            length=500
        )

        self.progress.pack()

    def apply_theme(self):

        self.root.configure(
            bg=THEMES[self.theme.get()]
        )

    def wait(self):

        while self.paused:
            time.sleep(0.05)

        if self.stopped:
            raise Exception

    def draw(self, colors=None):

        self.wait()

        self.canvas.delete("all")

        n = len(self.arr)

        width = 1240 / max(1, n)

        if colors is None:
            colors = [BAR] * n

        for i, val in enumerate(self.arr):

            self.canvas.create_rectangle(
                i * width,
                500 - val * 4,
                (i + 1) * width,
                500,
                fill=colors[i]
            )

        runtime = round(
            time.time() - self.start_time,
            3
        )

        self.stats.config(
            text=f"Comparisons:{self.comparisons}  Swaps:{self.swaps}  Runtime:{runtime}s"
        )

        self.comp.config(
            text=COMPLEXITY[
                self.algorithm.get()
            ]
        )

        self.root.after(
            self.speed.get()
        )

        self.root.update_idletasks()

    def generate_array(self):

        if self.sorting:
            return

        size = self.size_slider.get()

        mode = self.array_mode.get()

        if mode == "Sorted":

            self.arr = list(
                range(10, size + 10)
            )

        elif mode == "Reverse":

            self.arr = list(
                range(size + 10, 10, -1)
            )

        else:

            self.arr = [

                random.randint(10,100)

                for _ in range(size)
            ]

        self.draw()

    def load_manual(self):

        try:

            self.arr = list(
                map(
                    int,
                    self.manual.get().split()
                )
            )

            self.draw()

        except:
            pass

    def bubble(self):

        n = len(self.arr)

        for i in range(n):

            for j in range(n-i-1):

                self.comparisons += 1

                if self.arr[j] > self.arr[j+1]:

                    self.arr[j], self.arr[j+1] = self.arr[j+1], self.arr[j]

                    self.swaps += 1

                self.progress["value"] = (i/n)*100

                self.draw()

    def selection(self):

        for i in range(len(self.arr)):

            mn = i

            for j in range(i+1,len(self.arr)):

                if self.arr[j] < self.arr[mn]:

                    mn = j

            self.arr[i], self.arr[mn] = self.arr[mn], self.arr[i]

            self.draw()

    def insertion(self):

        for i in range(1,len(self.arr)):

            key = self.arr[i]

            j = i-1

            while j>=0 and self.arr[j]>key:

                self.arr[j+1] = self.arr[j]

                j -= 1

                self.draw()

            self.arr[j+1] = key

    def merge_sort(self,l,r):

        if l>=r:
            return

        m=(l+r)//2

        self.merge_sort(l,m)

        self.merge_sort(m+1,r)

        self.merge(l,m,r)

    def merge(self,l,m,r):

        left=self.arr[l:m+1]
        right=self.arr[m+1:r+1]

        i=j=0
        k=l

        while i<len(left) and j<len(right):

            if left[i] <= right[j]:

                self.arr[k]=left[i]

                i+=1

            else:

                self.arr[k]=right[j]

                j+=1

            k+=1

            self.draw()

    def partition(self,low,high):

        pivot=self.arr[high]

        i=low-1

        for j in range(low,high):

            if self.arr[j] < pivot:

                i+=1

                self.arr[i],self.arr[j]=self.arr[j],self.arr[i]

                self.draw()

        self.arr[i+1],self.arr[high]=self.arr[high],self.arr[i+1]

        return i+1

    def quick_sort(self,low,high):

        if low<high:

            pi=self.partition(low,high)

            self.quick_sort(low,pi-1)

            self.quick_sort(pi+1,high)

    def heapify(self,n,i):

        largest=i

        l=2*i+1
        r=2*i+2

        if l<n and self.arr[l]>self.arr[largest]:
            largest=l

        if r<n and self.arr[r]>self.arr[largest]:
            largest=r

        if largest!=i:

            self.arr[i],self.arr[largest]=self.arr[largest],self.arr[i]

            self.draw()

            self.heapify(n,largest)

    def heap_sort(self):

        n=len(self.arr)

        for i in range(n//2-1,-1,-1):
            self.heapify(n,i)

        for i in range(n-1,0,-1):

            self.arr[i],self.arr[0]=self.arr[0],self.arr[i]

            self.draw()

            self.heapify(i,0)

    def shell(self):

        gap=len(self.arr)//2

        while gap:

            for i in range(gap,len(self.arr)):

                temp=self.arr[i]

                j=i

                while j>=gap and self.arr[j-gap]>temp:

                    self.arr[j]=self.arr[j-gap]

                    j-=gap

                    self.draw()

                self.arr[j]=temp

            gap//=2

    def export_csv(self):

        with open(
            "stats.csv",
            "a",
            newline=""
        ) as file:

            csv.writer(file).writerow([
                self.algorithm.get(),
                self.comparisons,
                self.swaps
            ])

    def stop(self):

        self.stopped=True

    def execute(self):

        try:

            self.start_time=time.time()

            algo=self.algorithm.get()

            if algo=="Bubble":
                self.bubble()

            elif algo=="Selection":
                self.selection()

            elif algo=="Insertion":
                self.insertion()

            elif algo=="Merge":
                self.merge_sort(0,len(self.arr)-1)

            elif algo=="Quick":
                self.quick_sort(0,len(self.arr)-1)

            elif algo=="Heap":
                self.heap_sort()

            elif algo=="Shell":
                self.shell()

            self.draw(
                [DONE]*len(self.arr)
            )

        except:
            pass

        self.sorting=False
        self.stopped=False

    def start_sort(self):

        if self.sorting:
            return

        self.sorting=True

        threading.Thread(
            target=self.execute,
            daemon=True
        ).start()


root = tk.Tk()

SortingVisualizer(root)

root.mainloop()

