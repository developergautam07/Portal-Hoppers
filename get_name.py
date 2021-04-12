from tkinter import *
from DataBridge import *

window = Tk()

window.title("Portal Hoppers")

labn = Label(window, text="Enter Your Name:", font= 24)
user_in = Entry(window, font= 24) 
lab_out = Label(window, text=user_in, font= 24)
lab_ln = Label(window, text="Your Name is:", font= 24)

def OnClickEvent():
    lab_out = Label(window, text=user_in.get().capitalize(), font= 32)
    lab_out.grid(row=3, column = 1)
    btn2 = Button(bd=4, bg="Green", fg="white", text="Save", padx=15, pady=5, font="bold", command=SaveName)
    lab_o = Label(window, text="", font= 32)
    lab_o.grid(row=5, column = 0)
    btn2.grid(row = 7, column = 0)

def SaveName():
	#playerdict = {"playerName" : user_in.get()}
    db = data_bridge()
    db.update_name(user_in.get().capitalize())
    window.destroy()

btn = Button(bd=4, bg="Blue", fg="white", text="Check", padx=10, pady=5, font="bold", command=OnClickEvent)

labn.grid(row = 0)
btn.grid(row = 4)
user_in.grid(row = 0, column = 1)
lab_ln.grid(row=2, column=0)
window.mainloop()