import tkinter as tk

def update_label():
    # Update the label text with what's written in the entry box
    label.config(text="Hello, " + entry.get())

# Create the main window
root = tk.Tk()
root.title("Tkinter Example")
root.geometry("300x150")  # Width x Height

# Create a label widget
label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
label.pack(pady=10)  # Add some vertical padding

# Create an entry widget
entry = tk.Entry(root, width=20)
entry.pack()

# Create a button widget
button = tk.Button(root, text="Submit", command=update_label)
button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
