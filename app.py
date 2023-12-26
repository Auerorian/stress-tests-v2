import tkinter as tk
from tkinter import ttk

def check_window_size():
    if root.winfo_width() < screen_width or root.winfo_height() < screen_height:
        root.geometry("1000x700")
    root.after(100, check_window_size)

#after entering the Order, Build, and S/N values... display the start testing screen, then the tabs with data. If I want tabs lol
def create_tab(notebook, text):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=text)
    label = ttk.Label(frame, text=f"Content of {text} tab")
    label.pack(fill='both', expand=True)
    if text == "Tab 1":
        entry = ttk.Entry(frame, width=20)
        entry.pack(padx=10, pady=10)
        button = ttk.Button(frame, text="Click Me")
        button.pack(pady=10)

    elif text == "Tab 2":
        text_widget = tk.Text(frame, height=5, width=30)
        text_widget.pack(padx=10, pady=10)
        checkbox = ttk.Checkbutton(frame, text="Check me")
        checkbox.pack()

    elif text == "Tab 3":
        scale = ttk.Scale(frame, from_=0, to=100, orient='horizontal', length=200)
        scale.pack(padx=10, pady=10)
        radio_button = ttk.Radiobutton(frame, text="Option 1")
        radio_button.pack()

root =tk.Tk()
root.title("System76 testing")

#screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#initial geometry for the window based on display
#probably doesn't need to be this big bu t we will see.
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(True, True)

notebook = ttk.Notebook(root)

create_tab(notebook, "Temps")
create_tab(notebook, "Tab 2")
create_tab(notebook, "Tab 3")

notebook.pack(fill='both', expand=True)

#widget example
label = tk.Label(root, text="Hello, world!")
#'pack' is used for displaying widgets nicely (suppossedly)
label.pack

button = tk.Button(root, text="Start all testing", command=lambda: print("bing bong"))
button.pack()

check_window_size()

# start the Tkinter event loop and listen for events
root.mainloop()

