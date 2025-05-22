from tkinter import Tk
from Screens.clock_screen import ClockScreen

if __name__ == "__main__":
    root = Tk()
    app = ClockScreen(root)
    root.mainloop()