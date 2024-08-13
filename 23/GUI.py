import tkinter as tk
import tkinter.ttk as ttk
import threading
from test_find import test

class GUI_manager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("23-NUETC")
        self.t = test()
        self.stop_event_jiaozhun = threading.Event()
        # 初始化
        self.frm_main = ttk.Frame(self, padding=10)
        self.frm_jiaozhen = ttk.Frame(self, padding=10)
        # 创建控件
        self.create_main_frame()
        self.create_jiaozhen_frame()

    def create_main_frame(self):
        self.frm_main.grid()
        ttk.Label(self.frm_main, text="Hello World!").grid(column=1, row=0)
        ttk.Button(self.frm_main, text="校准", command=self.switch_to_jiaozhen).grid(column=1, row=1)
        ttk.Button(self.frm_main, text="第一题", command=lambda: print("第一题")).grid(column=1, row=2)
        ttk.Button(self.frm_main, text="第二题", command=lambda: print("第二题")).grid(column=1, row=3)
        ttk.Button(self.frm_main, text="第三题", command=lambda: print("第三题")).grid(column=1, row=4)
        ttk.Button(self.frm_main, text="Quit", command=self.destroy).grid(column=1, row=5)

    def create_jiaozhen_frame(self):
        ttk.Label(self.frm_jiaozhen, text="校准").grid(column=1, row=0)
        ttk.Button(self.frm_jiaozhen, text="加入校准点", command=self.toggle_write_down).grid(column=1, row=1)
        ttk.Button(self.frm_jiaozhen, text="打印坐标", command=lambda: print(self.t.corner_location)).grid(column=1, row=2)
        ttk.Button(self.frm_jiaozhen, text="退出", command=self.exit_jiaozhen).grid(column=1, row=3)

    def toggle_write_down(self):
        self.t.is_write_down = not self.t.is_write_down  

    def switch_to_jiaozhen(self):
        self.frm_jiaozhen.grid()
        self.frm_main.grid_forget()
        self.stop_event_jiaozhun.clear()
        threading.Thread(target=self.t.find_blob,args=(self.stop_event_jiaozhun,)).start()

    def exit_jiaozhen(self):
        self.stop_event_jiaozhun.set()
        if hasattr(self, 'thread'):
            self.thread.join()
        self.t.exit()
        self.frm_jiaozhen.grid_forget()
        self.frm_main.grid()
    
    def switch(self,new_screen,old_screen):
        self.new_screen.gird()
        self.old_screen.grid_forget()

if __name__ == "__main__":
    app = GUI_manager()
    app.mainloop()