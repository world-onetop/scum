import tkinter as tk
from tkinter import messagebox
from pymem import Pymem
from pymem.ptypes import RemotePointer

import offsets

# 获取力量、体制、敏捷和智慧的偏移量
offsets_4d = offsets.get_4D()

# 获取22项技能的偏移量
offsets_skill = offsets.get_skill_22()

pm = Pymem('SCUM.exe')
world = pm.base_address


# 获取偏移指针
def getPtrAddr(base, addr):
    remote_pointer = RemotePointer(pm.process_handle, base)
    for i in range(len(addr)):
        if i != len(addr) - 1:
            remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + addr[i])
        else:
            return remote_pointer.value + addr[i]


# 设置最大值
def mix():
    default_values = ["8", "5", "5", "5"]
    for i in range(4):
        entries[i].delete(0, tk.END)  # 清除当前内容
        entries[i].insert(0, default_values[i])  # 插入默认值


# 四维属性修改
def modify_stats():
    # 获取用户输入的值
    try:
        strength_value = float(entries[0].get())
        constitution_value = float(entries[1].get())
        agility_value = float(entries[2].get())
        intelligence_value = float(entries[3].get())
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字！")
        return

    # 修改力量、体制、敏捷和智慧
    for add in offsets_4d:
        pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets_4d[add]), strength_value)

    # 显示成功消息框
    messagebox.showinfo("成功", "四维属性修改成功！")


# 22技能修改
def modify_skill():
    # 设置修改值
    value = 100000000.00
    # 修改
    # 对每个偏移量进行修改
    for offset in offsets_skill:
        # if offset == '0x80':
        #     continue  # 跳过键为 '0x80' 的偏移量
        pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets_skill[offset]), value)
    messagebox.showinfo("成功", "22项技能修改修改成功！")


# 窗口置顶
def set_window_topmost():
    if root.attributes('-topmost'):
        root.attributes('-topmost', False)
    else:
        root.attributes('-topmost', True)


root = tk.Tk()
root.title("【单机】SCUM属性修改2.0")

# 获取屏幕宽度和高度
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# 计算窗口左上角坐标值
x = int((width - 500) / 2)
y = int((height - 300) / 2)

# 设置主窗口大小和位置
root.geometry("{}x{}+{}+{}".format(500, 300, x, y))

# 创建四个标签和四个输入框
labels = ['力量：', '体制：', '敏捷：', '智慧：']
entries = [tk.Entry(root) for _ in range(4)]
stats = [pm.read_double(getPtrAddr(world + 0x06FF30B0, offsets_4d[key])) for key in offsets_4d]

for i, label in enumerate(labels):
    tk.Label(root, text=label).place(x=10, y=5 + 45 * i)
    entries[i].place(x=60, y=5 + 45 * i)
    entries[i].insert(0, str(stats[i]))

# 右侧22项属性显示
text = tk.Text(root, width=35, height=15)
text.place(x=220, y=5)
# 创建Label标签
# 创建Scrollbar滚动条
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# 绑定Scrollbar和Text
text.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=text.yview)


# 显示文本
def refresh_offsets_skill():
    # 清除先前生成的文本
    text.delete('0.0', tk.END)
    # 读取技能数值并输出
    for offset in offsets_skill:
        # if offset == '0x80':
        #     continue  # 跳过键为 '0x80' 的偏移量
        t = pm.read_double(getPtrAddr(world + 0x06FF30B0, offsets_skill[offset]))
        text.insert(tk.END, str(offset) + "的数值为:{}\n".format(t))


# 添加“确定”按钮和“退出”按钮
tk.Button(root, text="四维最大值", command=mix).place(x=10, y=250)
tk.Button(root, text="确定", command=modify_stats).place(x=100, y=250)
tk.Button(root, text="22项最大值修改", command=modify_skill).place(x=200, y=250)
tk.Button(root, text="22项数值读取", command=refresh_offsets_skill).place(x=320, y=250)
tk.Button(root, text="退出", command=root.quit).place(x=430, y=250)
tk.Button(root, text="窗口置顶", command=set_window_topmost).place(x=50, y=200)

root.mainloop()
