import tkinter as tk
import random
from functools import reduce

print("SY-5, Kevin Victor, Roll No.-30")

# ---------------- CONFIG ----------------
BOX_W = 50
BOX_H = 35
ANIM_STEPS = 25
DEFAULT_SPEED = 20


# ---------------- DATA BOX CLASS ----------------
class DataBox:
    def __init__(self, canvas, value, x, y):
        self.canvas = canvas
        self.value = value
        self.x = x
        self.y = y

        self.rect = canvas.create_rectangle(
            x, y, x + BOX_W, y + BOX_H,
            fill="#4da6ff", outline="black", width=2,
            tags="box"
        )
        self.text = canvas.create_text(
            x + BOX_W/2, y + BOX_H/2,
            text=str(value), font=("Arial", 12, "bold"),
            tags="box"
        )

    def move_to(self, tx, ty, speed, callback=None):
        dx = (tx - self.x) / ANIM_STEPS
        dy = (ty - self.y) / ANIM_STEPS

        def step(i=0):
            if i >= ANIM_STEPS:
                self.x, self.y = tx, ty
                if callback:
                    callback()
                return
            self.canvas.move(self.rect, dx, dy)
            self.canvas.move(self.text, dx, dy)
            self.canvas.after(speed, step, i+1)

        step()

    def scale(self, factor, speed, callback=None):
        cx = self.x + BOX_W/2
        cy = self.y + BOX_H/2
        new_w = BOX_W * factor
        new_h = BOX_H * factor

        self.canvas.coords(
            self.rect,
            cx - new_w/2, cy - new_h/2,
            cx + new_w/2, cy + new_h/2
        )

        self.canvas.after(speed, callback if callback else lambda: None)

    def update_value(self, new_val):
        self.value = new_val
        self.canvas.itemconfig(self.text, text=str(new_val))

    def fade_out(self, speed, callback=None):
        self.canvas.itemconfig(self.rect, fill="#cccccc")
        self.canvas.itemconfig(self.text, fill="#aaaaaa")
        self.canvas.after(speed, callback if callback else lambda: None)


# ---------------- MAIN APP ----------------
class PipelineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Functional Pipeline")

        self.speed = tk.IntVar(value=DEFAULT_SPEED)

        # ----- Controls -----
        top = tk.Frame(root)
        top.pack()

        tk.Label(top, text="Numbers (comma separated):").grid(row=0, column=0)
        self.entry = tk.Entry(top, width=30)
        self.entry.grid(row=0, column=1)
        self.entry.insert(0, "1,5,7,2,4,42,26")

        tk.Button(top, text="Generate Random",
                  command=self.generate_random).grid(row=0, column=2)

        tk.Label(top, text="Speed").grid(row=0, column=3)
        tk.Scale(top, from_=5, to=60, orient="horizontal",
                 variable=self.speed).grid(row=0, column=4)

        # ----- Buttons -----
        mid = tk.Frame(root)
        mid.pack()

        tk.Button(mid, text="Start Auto",
                  command=self.start_auto).grid(row=0, column=0)
        tk.Button(mid, text="Reset",
                  command=self.reset_pipeline).grid(row=0, column=1)

        # ----- Canvas -----
        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        self.draw_labels()
        self.original = []
        self.filtered = []
        self.mapped = []

        self.reset_pipeline()

    # -------- LABELS --------
    def draw_labels(self):
        self.canvas.create_text(450, 40, text="INPUT",
                                font=("Arial", 14, "bold"),
                                tags="stage_label")
        self.canvas.create_text(450, 150, text="FILTERED",
                                font=("Arial", 14, "bold"),
                                tags="stage_label")
        self.canvas.create_text(450, 260, text="MAPPED (Squared)",
                                font=("Arial", 14, "bold"),
                                tags="stage_label")
        self.canvas.create_text(450, 380, text="REDUCED SUM",
                                font=("Arial", 14, "bold"),
                                tags="stage_label")

    # -------- RESET --------
    def reset_pipeline(self):
        self.canvas.delete("box")
        self.canvas.delete("result_text")
        self.canvas.delete("temp_text")

        self.original.clear()
        self.filtered.clear()
        self.mapped.clear()

        self.draw_input()

    # -------- DATA --------
    def generate_random(self):
        nums = [random.randint(1, 40) for _ in range(7)]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ",".join(map(str, nums)))

    def draw_input(self):
        try:
            values = [int(v.strip()) for v in self.entry.get().split(",") if v.strip()]
        except:
            values = []

        x = 80
        for val in values:
            self.original.append(DataBox(self.canvas, val, x, 70))
            x += 80

    # -------- PIPELINE --------
    def start_auto(self):
        self.reset_pipeline()
        self.step_filter()
        self.root.after(1800, self.step_map)
        self.root.after(3600, self.step_reduce)

    def step_filter(self):
        for box in self.original:
            if box.value % 2 == 0:
                tx = 120 + len(self.filtered)*80
                self.filtered.append(box)
                box.move_to(tx, 170, self.speed.get())
            else:
                box.fade_out(self.speed.get())

    def step_map(self):
        for box in self.filtered:
            tx = 120 + len(self.mapped)*120
            def after_move(b=box):
                b.scale(1.8, self.speed.get(),
                        lambda: b.update_value(b.value**2))
            box.move_to(tx, 280, self.speed.get(), after_move)
            self.mapped.append(box)

    def step_reduce(self):
        if not self.mapped:
            return

        cx, cy = 450, 340   # moved ABOVE result text

        for box in self.mapped:
            box.move_to(cx, cy, self.speed.get())

        values = [b.value for b in self.mapped]
        total = reduce(lambda a,b: a+b, values, 0)

        blur = self.canvas.create_text(
            450, 430,
            text="Calculating...",
            font=("Arial", 18),
            fill="grey",
            tags="temp_text"
        )

        def reveal():
            self.canvas.delete("temp_text")
            self.canvas.create_text(
                450, 430,
                text=f"SUM = {total}",
                font=("Arial", 22, "bold"),
                fill="black",
                tags="result_text"
            )
            self.canvas.tag_raise("result_text")

        self.canvas.after(800, reveal)


# ---------------- RUN ----------------
root = tk.Tk()
app = PipelineApp(root)
root.mainloop()
