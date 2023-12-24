import tkinter as tk

def check_window_size():
    if root.winfo_width() < screen_width or root.winfo_height() < screen_height:
        root.geometry("1000x700")
    root.after(100, check_window_size)

root =tk.Tk()
root.title("System76 testing")

#screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#initial geometry for the window based on display
#probably doesn't need to be this big bu t we will see.
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(True, True)



#widget example
label = tk.Label(root, text="Hello, world!")
#'pack' is used for displaying widgets nicely (suppossedly)
label.pack

button = tk.Button(root, text="Start all testing", command=lambda: print("Started! heres your display cunt!"))
button.pack()

check_window_size()

# start the Tkinter event loop and listen for events
root.mainloop()

