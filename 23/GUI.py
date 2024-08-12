import tkinter as tk
import tkinter.ttk as ttk
from test_find import test
import threading

t = test()
root = tk.Tk()
frm = ttk.Frame(root, padding=10)

def switch_to_jiaozhen():
    frm_jiaozhen.grid()
    frm.grid_forget()
    threading.Thread(target=t.find_blob).start() 

def exit_jiaozhen():
    t.exit()  
    frm_jiaozhen.grid_forget()
    frm.grid()

frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=1, row=0)
ttk.Button(frm, text="校准", command=switch_to_jiaozhen).grid(column=1, row=1)
ttk.Button(frm, text="第一题", command=lambda: print("第一题")).grid(column=1, row=2)
ttk.Button(frm, text="第二题", command=lambda: print("第二题")).grid(column=1, row=3)
ttk.Button(frm, text="第三题", command=lambda: print("第三题")).grid(column=1, row=4)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=5)

frm_jiaozhen = ttk.Frame(root, padding=10)
ttk.Label(frm_jiaozhen, text="校准").grid(column=1, row=0)
ttk.Button(frm_jiaozhen, text="加入校准点", command=lambda: print("加入校准点")).grid(column=1, row=1)
ttk.Button(frm_jiaozhen, text="退出", command=exit_jiaozhen).grid(column=1, row=2)

root.mainloop()
