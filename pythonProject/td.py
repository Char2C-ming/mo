import os
import tkinter as tk
from tkinter import messagebox, ttk


def bad_character_heuristic(pattern):
    bad_char = {}
    m = len(pattern)
    for i in range(m):
        bad_char[pattern[i]] = i
    return bad_char


def good_suffix_heuristic(pattern):
    m = len(pattern)
    good_suffix = [-1] * m
    last_prefix_position = m

    for j in range(m - 1, -1, -1):
        if is_prefix(pattern, j + 1):
            last_prefix_position = j + 1
        good_suffix[j] = last_prefix_position - j + m - 1

    for j in range(m - 1):
        length = suffix_length(pattern, j)
        good_suffix[length] = m - 1 - j + length

    return good_suffix


def is_prefix(pattern, p):
    m = len(pattern)
    for i in range(p, m):
        if pattern[i] != pattern[i - p]:
            return False
    return True


def suffix_length(pattern, j):
    m = len(pattern)
    length = 0
    for i in range(m - 1, j, -1):
        if pattern[i] == pattern[m - 1 - length]:
            length += 1
        else:
            break
    return length


def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    bad_char = bad_character_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)

    s = 0
    matches = []
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            matches.append(s)
            s += good_suffix[0]
        else:
            bad_char_shift = j - bad_char.get(text[s + j], -1)
            good_suffix_shift = good_suffix[j]
            s += max(bad_char_shift, good_suffix_shift)
    return matches


def scan_directory(directory, virus_signatures):
    """ 扫描目录并返回每个文件及其状态 """
    files_status = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                is_virus = False
                for signature in virus_signatures:
                    matches = boyer_moore_search(file_content.decode(errors='ignore'), signature)
                    if matches:
                        is_virus = True
                        break
                files_status.append((file_path, is_virus))
            except Exception:
                continue  # 跳过无法读取的文件
    return files_status


def delete_files(files_to_delete):
    """ 删除指定文件 """
    for file_path in files_to_delete:
        os.remove(file_path)


def scan_folder():
    """ 扫描指定文件夹并更新结果 """
    folder_path = r"D:\pycharmdata\pythonProject\make"  # 指定扫描文件夹

    # 清空当前结果
    for item in tree.get_children():
        tree.delete(item)

    # 显示扫描的文件和识别病毒
    files_status = scan_directory(folder_path, virus_signatures)

    files_to_delete = []  # 存储待删除的病毒文件

    for file_path, is_virus in files_status:
        if is_virus:
            tree.insert("", "end", text=file_path, tags=("virus",))
            files_to_delete.append(file_path)  # 添加到待删除列表
        else:
            tree.insert("", "end", text=file_path, tags=("safe",))

    # 更新界面
    messagebox.showinfo("Сканирование завершено.", f"Сканирование завершено {len(files_status)} Файл.")

    # 弹出确认删除对话框
    if files_to_delete:
        if messagebox.askyesno("Подтверждаю.", f"Найди файл с вирусом: {len(files_to_delete)} Во-первых, удалить эти файлы или нет?"):
            delete_files(files_to_delete)
            messagebox.showinfo("Удалено.", f"Удалено. {len(files_to_delete)} Вирус.")
    else:
        messagebox.showinfo("Вируса нет.", "Вирусные файлы не обнаружены")


# 设置病毒签名
virus_signatures = [
    "rb3",  # 替换为实际签名
    "virus_signature_2"      # 替换为实际签名
]

# 创建主窗口
root = tk.Tk()
root.title("Вирусный сканер")
root.geometry("600x400")

# 创建扫描按钮
scan_button = tk.Button(root, text="Сканирующая папка", command=scan_folder)
scan_button.pack(pady=10)

# 创建树形视图显示结果
tree = ttk.Treeview(root, columns=("path"), show="tree")
tree.pack(expand=True, fill="both")

# 添加滚动条
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# 添加水平滚动条
h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
tree.configure(xscroll=h_scrollbar.set)
h_scrollbar.pack(side="bottom", fill="x")

# 设置列宽
tree.column("#0", width=600)  # 主列宽度
tree.heading("#0", text="文件路径")

# 添加样式
tree.tag_configure("virus", foreground="red")  # 病毒文件为红色
tree.tag_configure("safe", foreground="green")  # 安全文件为绿色

# 启动主循环
root.mainloop()