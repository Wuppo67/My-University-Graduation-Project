# 可视化基本功能
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *
from random import randint
from tkinter.simpledialog import askstring
from tkinter import simpledialog

# 窗口的宽度和高度  全局变量
win_width = 1000
win_height = 700
count = 0

class CustomDialog_top(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.entry_text = None
        super().__init__(parent, title)
    def body(self, master):
        Label(master, text="请输入顶事件:").grid(row=0)
        self.entry_text = Entry(master)
        self.entry_text.grid(row=1, padx=30, pady=10)   #调节输入框大小
        return self.entry_text
    def apply(self):
        self.result = self.entry_text.get()

class CustomDialog_mid(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.entry_text = None
        super().__init__(parent, title)
    def body(self, master):
        Label(master, text="请输入中间事件:").grid(row=0)
        self.entry_text = Entry(master)
        self.entry_text.grid(row=1, padx=30, pady=10)   #调节输入框大小
        return self.entry_text
    def apply(self):
        self.result = self.entry_text.get()

class CustomDialog_bot(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.entry_text = None
        super().__init__(parent, title)
    def body(self, master):
        Label(master, text="请输入底事件:").grid(row=0)
        self.entry_text = Entry(master)
        self.entry_text.grid(row=1, padx=30, pady=10)   #调节输入框大小
        return self.entry_text
    def apply(self):
        self.result = self.entry_text.get()

class Application(Frame):
    '''经典写法'''
    def __init__(self, master=None, bgcolor='green'):
        super().__init__(master)   # super代表父类定义 而不是父类对象
        self.master = master       # 挂钩
        self.bgcolor = bgcolor
        self.x = 0
        self.y = 0
        self.fgcolor = 'black'
        self.lastDraw = 0  # 表示最后绘制的图形的id
        self.startDrawFlag = False
        self.pack()
        self.createWidget()
        self.history = []  # 用于记录历史操作
        self.is_drawing = False

    def createWidget(self):
        '''创建组件'''
        # 绘图区
        self.drawpad = Canvas(self, width=win_width, height=win_height * 0.9, bg=self.bgcolor)
        self.drawpad.pack()
        self.img1 = PhotoImage(file="gif/r1.gif")  # 第一张图片
        self.img2 = PhotoImage(file="gif/r2.gif")
        # 创建按钮
        Button(self.master, text='添加顶事件', command=self.add_movable_label_top).pack(side='left', padx='10')
        Button(self.master, text='添加中间事件', command=self.add_movable_label_mid).pack(side='left', padx='10')
        Button(self.master, text='添加底事件', command=self.add_movable_label_bot).pack(side='left', padx='10')
        Button(self.master, text='添加或门', command=lambda: self.add_image(self.img1)).pack(side='left', padx='10')
        Button(self.master, text='添加与门', command=lambda: self.add_image(self.img2)).pack(side='left', padx='10')
        Button(self.master, text='连接线', command=self.activate_line_arrow).pack(side='left', padx='10')
        Button(self.master, text='线条颜色', command=self.choose_color).pack(side='left', padx='10')
        Button(self.master, text='撤销', command=self.undo_last_action).pack(side='left', padx='10')
        Button(self.master, text='清屏', command=self.clear_canvas).pack(side='left', padx='10')
        Button(self.master, text='计算最小割集', command=self.min_sep).pack(side='left', padx='10')


    def min_sep(self):
        messagebox.showinfo('结果', f'上式共有{count}个积项，因此得到{count}个最小割集。')

    #选择画笔颜色
    def choose_color(self):
        color = askcolor(color=self.fgcolor, title='选择画笔颜色')
        if color[1]:
            self.fgcolor = color[1]
            #print("选择的颜色:", self.fgcolor)

    # 清平功能
    def clear_canvas(self):
        self.drawpad.delete('all')

    # 连接线功能实现
    def activate_line_arrow(self):
        # 准备绘制箭头直线
        self.drawpad.bind('<Button-1>', self.start_draw)
        self.drawpad.bind('<B1-Motion>', self.myline_arrow)
        self.drawpad.bind('<ButtonRelease-1>', self.stop_draw)

    def start_draw(self, event):
        # 记录鼠标点击的初始位置
        self.x = event.x
        self.y = event.y
        self.lastDraw = None

    def myline_arrow(self, event):
        # 拖动时绘制箭头直线
        if self.lastDraw:
            self.drawpad.delete(self.lastDraw)
        self.lastDraw = self.drawpad.create_line(self.x, self.y, event.x, event.y, arrow=LAST, fill=self.fgcolor, width=6)

    def stop_draw(self, event):
        # 结束绘制，固定最后一条线
        self.myline_arrow(event)
        self.drawpad.unbind('<B1-Motion>')
        self.drawpad.unbind('<ButtonRelease-1>')
        # 记录添加的线条
        if self.lastDraw:
            self.history.append(('line', self.lastDraw))

    # 添加图片的功能函数
    def add_image(self, img):
        x = randint(50, 950)  # 随机位置需要考虑Canvas的实际大小
        y = randint(50, 500)
        image_on_canvas = self.drawpad.create_image(x, y, image=img, anchor='center')
        self.history.append(('image', image_on_canvas))  # 记录添加的图片
        self.drawpad.tag_bind(image_on_canvas, '<Button1-Motion>', lambda event, img=image_on_canvas: self.move_image(event, img))
        self.drawpad.tag_bind(image_on_canvas, '<ButtonPress-1>', lambda event, img=image_on_canvas: self.start_move_imag(event, img))

    def start_move_imag(self, event, img):
        self._drag_data = {'x': event.x, 'y': event.y, 'item': img}

    def move_image(self, event, img):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        self.drawpad.move(img, delta_x, delta_y)
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    # 添加对话框的功能函数
    def add_movable_label_top(self, event=None):  # event参数是可选的，这样可以直接从按钮点击调用
        global count
        dialog = CustomDialog_top(self.master, title="添加提示")
        text = dialog.result
        if text:
            # 使用固定位置创建标签，例如(400, 200)
            label = Label(self.drawpad, text=text,bg='red',font=('黑体',15),relief='raised')
            label_window = self.drawpad.create_window(400, 200, window=label, anchor='nw')
            self.history.append(('label', label_window, label))  # 记录添加的标签
            label.bind("<Button-1>", lambda event, lw=label_window: self.start_move_label(event, lw))
            label.bind("<B1-Motion>", lambda event, lw=label_window: self.move_label(event, lw))
        if text is not None:  # 确认用户点击了“OK”按钮
            count += 1

    def add_movable_label_mid(self, event=None):  # event参数是可选的，这样可以直接从按钮点击调用
        global count
        dialog = CustomDialog_mid(self.master, title="添加提示")
        text = dialog.result
        if text:
            # 使用固定位置创建标签，例如(400, 200)
            label = Label(self.drawpad, text=text, bg='blue',font=('黑体',12), relief='raised')
            label_window = self.drawpad.create_window(500, 300, window=label, anchor='nw')
            self.history.append(('label', label_window, label))  # 记录添加的标签
            label.bind("<Button-1>", lambda event, lw=label_window: self.start_move_label(event, lw))
            label.bind("<B1-Motion>", lambda event, lw=label_window: self.move_label(event, lw))
        if text is not None:  # 确认用户点击了“OK”按钮
            count += 1

    def add_movable_label_bot(self, event=None):  # event参数是可选的，这样可以直接从按钮点击调用
        dialog = CustomDialog_bot(self.master, title="添加提示")
        text = dialog.result
        if text:
            # 使用固定位置创建标签，例如(400, 200)
            label = Label(self.drawpad, text=text, bg='white',font=('黑体',10), relief='raised')
            label_window = self.drawpad.create_window(600, 400, window=label, anchor='nw')
            self.history.append(('label', label_window, label))  # 记录添加的标签
            label.bind("<Button-1>", lambda event, lw=label_window: self.start_move_label(event, lw))
            label.bind("<B1-Motion>", lambda event, lw=label_window: self.move_label(event, lw))

    def start_move_label(self, event, label_window):
        self.x = event.x
        self.y = event.y

    def move_label(self, event, label_window):
        delta_x = event.x - self.x
        delta_y = event.y - self.y
        self.drawpad.move(label_window, delta_x, delta_y)
        self.x = event.x
        self.y = event.y

    # 撤销功能的实现,本质是分别保存不同操作类型的历史到数组中
    def undo_last_action(self):
        if self.history:
            last_action = self.history.pop()
            if last_action[0] == 'label':
                label_window, label = last_action[1], last_action[2]
                self.drawpad.delete(label_window)  # 删除画布上的窗口
                label.destroy()  # 销毁标签对象
            elif last_action[0] == 'line':
                self.drawpad.delete(last_action[1])  # 删除线条
            elif last_action[0] == 'image':
                self.drawpad.delete(last_action[1])  # 删除图片

#封装成函数 方便登陆界面调用
def run_fault_tree():
    root = Tk()
    root.geometry(f'{win_width}x{win_height}+300+50')  #动态尺寸，固定显示位置
    root.title('可视化故障树')
    app = Application(master=root)
    root.mainloop()

# 当你想运行这个模块作为独立程序时，可以使用以下代码
#if __name__ == '__main__':
#   run_fault_tree()
