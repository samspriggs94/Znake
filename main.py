from tkinter import Tk, Canvas

if __name__ == "__main__":
    # Create the main window
    root = Tk()
    root.title("Centered Square")
    root.geometry("500x500")  # Set window size

    # Create a Canvas to draw shapes
    canvas = Canvas(root, width=500, height=500, bg="white", highlightthickness=0)
    canvas.pack()

    # Size of the small black square
    square_size = 2

    # Calculate coordinates to center it
    x0 = (100 - square_size) / 2
    y0 = (100 - square_size) / 2
    x1 = x0 + square_size
    y1 = y0 + square_size

    # Draw the black square
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")

    # Start the event loop
    root.mainloop()

