import tkinter as tk
from tkinter import messagebox

from pymem import Pymem

# 力量、体制、敏捷和智慧的偏移量
offsets = {
    'strength': [0x190, 0x30, 0x2A0],
    'constitution': [0x190, 0x30, 0x2A0 + 0x10],
    'agility': [0x190, 0x30, 0x2A0 + 0x20],
    'intelligence': [0x190, 0x30, 0x2A0 + 0x30]
}

pm = Pymem('SCUM.exe')
world = pm.base_address


def getPtrAddr(address, offses):
    addr = pm.read_longlong(address)
    for offset in offses:
        if offset != offses[-1]:
            addr = pm.read_longlong(addr + offset)
    addr = addr + offses[-1]
    return addr


# 设置最大值
def mix():
    default_values = ["8", "5", "5", "5"]
    for i in range(4):
        entries[i].delete(0, tk.END)  # 清除当前内容
        entries[i].insert(0, default_values[i])  # 插入默认值


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
    pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets['strength']), strength_value)
    pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets['constitution']), constitution_value)
    pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets['agility']), agility_value)
    pm.write_double(getPtrAddr(world + 0x06FF30B0, offsets['intelligence']), intelligence_value)

    # 显示成功消息框
    messagebox.showinfo("成功", "属性修改成功！")


root = tk.Tk()
root.title("SCUM四维属性修改")

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
stats = [pm.read_double(getPtrAddr(world + 0x06FF30B0, offsets[key])) for key in offsets]

for i, label in enumerate(labels):
    tk.Label(root, text=label).place(x=10, y=5 + 45 * i)
    entries[i].place(x=60, y=5 + 45 * i)
    entries[i].insert(0, str(stats[i]))

# 添加“确定”按钮和“退出”按钮
tk.Button(root, text="最大值", command=mix).place(x=100, y=250)
tk.Button(root, text="确定", command=modify_stats).place(x=200, y=250)
tk.Button(root, text="退出", command=root.quit).place(x=300, y=250)

root.mainloop()
