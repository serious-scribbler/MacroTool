import tkinter as tk

def OnLeftMouseDown(event):
    global InitialX, InitialY, RectID
    InitialX, InitialY = event.x, event.y
    RectID = canvas.create_rectangle(InitialX, InitialY, InitialX, InitialY)

def OnLeftMouseUp(event):
    canvas.delete(RectID)

def OnLeftMouseMove(event):
    canvas.update_idletasks()
    canvas.coords(RectID, InitialX, InitialY, event.x, event.y)

root = tk.Tk()
#root.overrideredirect(True)
root.lift()
root.geometry("+15+15")
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.4)
canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()
canvas.create_oval(200, 200, 400, 400, fill='blue')

canvas.bind("<ButtonPress-1>", OnLeftMouseDown)
canvas.bind("<B1-Motion>", OnLeftMouseMove)
canvas.bind("<ButtonRelease-1>", OnLeftMouseUp)
root.after(5000, root.destroy)
root.mainloop()

