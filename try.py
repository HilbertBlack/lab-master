import tkinter as tk

root = tk.Tk()
root.title("Scrollable Frame with Items")
root.geometry("400x500")

# --- Canvas ---
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# --- Scrollbar ---
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# --- Parent Frame inside Canvas ---
parent_frame = tk.Frame(canvas)

# Create window inside canvas
canvas_window = canvas.create_window((0, 0), window=parent_frame, anchor="nw")

# --- Update scroll region ---
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

parent_frame.bind("<Configure>", update_scrollregion)

# --- Make frame width match canvas ---
def resize_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", resize_frame)

# --- Add multiple small frames ---
for i in range(30):
    item = tk.Frame(parent_frame, bg="lightblue", bd=2, relief="ridge")
    item.pack(fill="x", padx=10, pady=5)

    tk.Label(item, text=f"Item {i}", bg="lightblue").pack(padx=10, pady=10)

root.mainloop()
