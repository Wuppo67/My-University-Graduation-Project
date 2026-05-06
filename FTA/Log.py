# 开发登陆页面   开发结束
from tkinter import *
from tkinter import messagebox
from  FaultTree import  run_fault_tree

class Application(Frame):
    '''经典写法'''
    def __init__(self, master=None):
        super().__init__(master)   #super代表父类定义 而不是父类对象
        self.master=master         #挂钩
        self.pack()
        self.createWidget()
    def createWidget(self):
        '''创建组件'''
        self.label01 = Label(self, text='可视化', width=10, height=2, bg='gold', fg='red')
        self.label01.grid(row=0,column=1)
        self.label02 = Label(self, text='建立故障树', width=10, height=2, bg='blue', fg='gold',font=('黑体',30))
        self.label02.grid(row=1,column=1)
        # 显示图像
        global photo  # 转化为全局变量，如果为局部，笨方法执行完后，图象被销毁
        photo = PhotoImage(file='gif/tree.gif')
        self.label03 = Label(self, imag=photo)
        self.label03.grid(row=2,column=1)
        #用户名和密码，输入框
        self.label04 = Label(self, text='用户名', width=10, height=2, bg='black', fg='white')
        self.label04.grid(row=3, column=0)
        self.entry01 = Entry(self)
        self.entry01.grid(row=3, column=1)
        self.label05 = Label(self, text='密码', width=10, height=2, bg='black', fg='white')
        self.label05.grid(row=4, column=0)
        self.entry02 = Entry(self, show='*')
        self.entry02.grid(row=4, column=1)
        #登录与退出按钮
        Button(self, text='登录',command=self.LG).grid(row=5, column=1, sticky=EW)
        Button(self, text='退出',command=root.destroy).grid(row=5, column=2, sticky=EW)  # 东西拉长
        #保存密码和自动登录
        self.codeHobby = IntVar()       # 用来存数字 也可用StringVar()
        self.videoHobby = IntVar()      # 用不同变量来接受
        print(self.codeHobby.get())     # 默认值是0
        self.c1 = Checkbutton(self, text='保存密码',variable=self.codeHobby, onvalue=1, offvalue=0)  # 选中是1 不选是0
        self.c2 = Checkbutton(self, text='自动登录', variable=self.videoHobby, onvalue=1, offvalue=0)
        self.c1.grid(row=3, column=2)
        self.c2.grid(row=4, column=2)

    def LG(self):
        username = self.entry01.get()
        pwd = self.entry02.get()
        '''模拟数据库'''
        if  username == 'admin' and pwd == '123456':
            messagebox.showinfo('提示', '登陆成功')
            self.master.destroy()  # 销毁登录窗口
            run_fault_tree()  # 打开故障树绘制窗口
        else:
            messagebox.showerror('警告', '登录失败')

if __name__ == '__main__':   # 更加规范 独立调用
    root = Tk()
    root.geometry('600x500+480+100')   # 前面是尺寸 后面是位置
    root.title('登陆界面')
    app = Application(master=root)
    # 传递对象/挂钩+继承 /self是容器对象
    root.mainloop()



