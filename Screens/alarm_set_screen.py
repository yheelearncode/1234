import tkinter as tk

class AlarmSetScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

    def create_frame(self, parent):
        frame = tk.Frame(parent, bg='black')
        label = tk.Label(frame, text="AlarmSetScreen 화면", fg="white", bg="black", font=("Helvetica", 24))
        label.pack(expand=True)
        return frame

    def on_show(self):
        pass

    def on_key_press(self, event):
        pass
