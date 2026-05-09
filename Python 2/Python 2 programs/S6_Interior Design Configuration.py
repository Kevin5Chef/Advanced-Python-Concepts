import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime
print("SY-5, Kevin Victor, Roll No.-30")
# ===============================
# LOGGING CONFIGURATION
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | OBJECT CREATED | %(message)s",
    datefmt="%H:%M:%S"
)

# ===============================
# BASE CLASS
# ===============================
class InteriorItem:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        logging.info(f"{category}: {name}")

    def __str__(self):
        return f"{self.category}: {self.name}"


# ===============================
# CATEGORY CLASSES
# ===============================
class ColorTheme(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Color Theme")


class Furniture(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Furniture")


class Appliance(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Appliance")


class Lighting(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Lighting")


class Carpet(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Carpet")


class Decor(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Decor")


class Electrical(InteriorItem):
    def __init__(self, name):
        super().__init__(name, "Electrical")


# ===============================
# DUMMY DATA
# ===============================
color_themes = [
    "Scandinavian White",
    "Earthy Minimal",
    "Royal Blue & Gold",
    "Industrial Grey",
    "Pastel Harmony"
]

furniture_items = [
    "L-shaped Sofa",
    "Recliner Chair",
    "King Bed",
    "Modular Wardrobe",
    "Glass Coffee Table"
]

appliances = [
    "Smart Refrigerator",
    "Induction Cooktop",
    "Dishwasher",
    "Air Conditioner",
    "Smart TV"
]

lighting_options = [
    "Warm LED Panel",
    "Pendant Light",
    "Floor Lamp",
    "Chandelier",
    "Recessed Spotlights"
]

carpets = [
    "Persian Rug",
    "Woolen Carpet",
    "Minimalist Mat",
    "Shaggy Carpet",
    "Geometric Runner"
]

decor_items = [
    "Abstract Wall Art",
    "Indoor Plant",
    "Vintage Clock",
    "Ceramic Vase",
    "Floating Shelves"
]

electrical_items = [
    "Smart Switch Panel",
    "Dimmer Switch",
    "Motion Sensor",
    "Modular Socket",
    "Smart Hub Controller"
]

# ===============================
# TKINTER APPLICATION
# ===============================
class InteriorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Interior Design Configurator")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e1e")

        self.design_objects = []

        self.create_widgets()

    def create_widgets(self):

        style = ttk.Style()
        style.theme_use("clam")

        ttk.Label(self.root, text="Select Interior Components",
                  font=("Arial", 18),
                  background="#1e1e1e",
                  foreground="white").pack(pady=15)

        self.create_dropdown("Color Theme", color_themes)
        self.create_dropdown("Furniture", furniture_items)
        self.create_dropdown("Appliance", appliances)
        self.create_dropdown("Lighting", lighting_options)
        self.create_dropdown("Carpet", carpets)
        self.create_dropdown("Decor", decor_items)
        self.create_dropdown("Electrical", electrical_items)

        ttk.Button(self.root, text="Add to Design",
                   command=self.add_to_design).pack(pady=15)

        ttk.Button(self.root, text="Reset Design",
                   command=self.reset_design).pack()

        self.summary_box = tk.Text(self.root, height=10, width=80)
        self.summary_box.pack(pady=15)

    def create_dropdown(self, label, values):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=5)

        ttk.Label(frame, text=label,
                  background="#1e1e1e",
                  foreground="white",
                  width=20).pack(side=tk.LEFT)

        combo = ttk.Combobox(frame, values=values, width=40)
        combo.pack(side=tk.LEFT)
        combo.current(0)

        setattr(self, label.replace(" ", "_").lower(), combo)

    def add_to_design(self):
        # Instantiate objects (constructor logs automatically)

        selected_objects = [
            ColorTheme(self.color_theme.get()),
            Furniture(self.furniture.get()),
            Appliance(self.appliance.get()),
            Lighting(self.lighting.get()),
            Carpet(self.carpet.get()),
            Decor(self.decor.get()),
            Electrical(self.electrical.get())
        ]

        self.design_objects.extend(selected_objects)

        self.update_summary()

    def update_summary(self):
        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, "Current Interior Design Selection:\n\n")
        for obj in self.design_objects:
            self.summary_box.insert(tk.END, str(obj) + "\n")

    def reset_design(self):
        self.design_objects.clear()
        self.summary_box.delete("1.0", tk.END)


# ===============================
# RUN APPLICATION
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = InteriorApp(root)
    root.mainloop()
