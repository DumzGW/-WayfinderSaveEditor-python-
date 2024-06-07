import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import sys
import json
import subprocess
import zlib
import os
import webbrowser
from 主界面 import GetMain
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def path0(path):
    return os.path.join(os.path.dirname(sys.argv[0]),path)
# 加载配置
def load_config():
    with open(resource_path('config.json'), 'r',encoding='utf-8') as config_file:
        return json.load(config_file)
def get_default_save_path():
    user_name = os.getlogin()
    default_path = f'C:/Users/{user_name}/AppData/Local/Wayfinder/Saved/SaveGames'
    return default_path
def ensure_output_folder_exists():
    output_path = 'output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
def show_bin_editor(bin_file_path):
    editor_window = tk.Toplevel(app)
    editor_window.title("编辑存档文件")
    editor_window.geometry("800x600")

    tree = ttk.Treeview(editor_window)
    tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(editor_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    with open(bin_file_path, 'r', encoding='utf-8') as bin_file:
        try:
            json_data = json.load(bin_file)
        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"无法解析 JSON: {e}")
            return

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item, 'text')
            entry.delete(0, tk.END)
            entry.insert(0, item_text)

    def on_save():
        selected_item = tree.selection()
        if selected_item:
            new_value = entry.get()
            if ':' in new_value:
                _,new_value1=new_value.split(':',1)
            
            tree.item(selected_item, text=new_value)
        # Update JSON data with new value
            update_json_data(json_data, tree.item(selected_item, 'tags')[0].split('/'), new_value1)
            # Save updated JSON data to file
            with open(bin_file_path, 'w', encoding='utf-8') as bin_file:
                json.dump(json_data, bin_file, ensure_ascii=False, indent=2)
            messagebox.showinfo("提示", "修改已保存")
    def update_json_data(data, path, value):
        for key in path[:-1]:
            if key.isdigit():
                key = int(key)
            data = data[key]
        last_key = path[-1]
        if last_key.isdigit():
            last_key = int(last_key)
        data[last_key] = value
    def build_tree_with_tags(parent, dictionary, parent_tag=''):
        for key, value in dictionary.items():
            tag = f"{parent_tag}/{key}" if parent_tag else key
            if isinstance(value, dict):
                node = tree.insert(parent, 'end', text=key, open=True, tags=(tag,))
                build_tree_with_tags(node, value, tag)
            elif isinstance(value, list):
                node = tree.insert(parent, 'end', text=f"{key}[]", open=False, tags=(tag,))
                for i, item in enumerate(value):
                    item_node = tree.insert(node, 'end', text=f"[{i}]", open=False, tags=(f"{tag}/{i}",))
                    if isinstance(item, dict):
                        build_tree_with_tags(item_node, item, f"{tag}/{i}")
                    else:
                        tree.insert(item_node, 'end', text=item, tags=(f"{tag}/{i}",))
            else:
                tree.insert(parent, 'end', text=f"{key}: {value}", tags=(tag,))

    build_tree_with_tags('', json_data)
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    entry = tk.Entry(editor_window)
    entry.pack(fill=tk.X, padx=5, pady=5)

    save_button = tk.Button(editor_window, text="保存", command=on_save)
    save_button.pack(pady=5)
def show_bin_editor1(bin_file_path):
    editor_window = tk.Toplevel(app)
    editor_window.title("编辑存档文件")
    editor_window.geometry("800x600")
    PAGE_SIZE = 1000
    current_page = 0
    bin_data_lines = []
    def load_page(page):
        nonlocal current_page
        text.delete('1.0', tk.END)
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        page_lines = bin_data_lines[start:end]
        text.insert(tk.END, ''.join(page_lines))
        current_page = page
        update_page_label()

    def next_page():
        if (current_page + 1) * PAGE_SIZE < len(bin_data_lines):
            load_page(current_page + 1)

    def prev_page():
        if current_page > 0:
            load_page(current_page - 1)

    def update_page_label():
        page_label.config(text=f"Page {current_page + 1} / {len(bin_data_lines) // PAGE_SIZE + 1}")
    
    with open(bin_file_path, 'rb') as bin_file:
        bin_data = bin_file.read().decode('utf-8', errors='replace')
        bin_data_lines = bin_data.splitlines(keepends=True)
        text = tk.Text(editor_window, wrap='none')
    text.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(editor_window, orient="vertical", command=text.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    text.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(editor_window)
    frame.pack(side=tk.TOP, fill=tk.X)

    prev_button = tk.Button(frame, text="上一页", command=prev_page)
    prev_button.pack(side=tk.LEFT)

    page_label = tk.Label(frame, text="")
    page_label.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(frame, text="下一页", command=next_page)
    next_button.pack(side=tk.LEFT)

    load_page(0)
    def save_bin_file():
        start = current_page * PAGE_SIZE
        end = start + PAGE_SIZE
        new_data = text.get('1.0', tk.END).splitlines(keepends=True)
        bin_data_lines[start:end] = new_data

        with open(bin_file_path, 'wb') as bin_file:
            bin_file.write(''.join(bin_data_lines).encode('utf-8'))
        messagebox.showinfo("提示", "文件已保存")

    save_button = tk.Button(frame, text="保存", command=save_bin_file)
    save_button.pack(side=tk.LEFT, padx=5)
# 保存路径
def save_to_json():
    ensure_output_folder_exists()
    default_path = get_default_save_path()
    if not os.path.exists(default_path):
        messagebox.showinfo("提示", "未找到存档路径，请手动选择")
        save_path = filedialog.askopenfilename(title="选择存档文件夹")
        if not folder_selected:
            return
    else:
        savegame_folders = os.listdir(default_path)
        if len(savegame_folders) == 1:
            folder_selected = os.path.join(default_path, savegame_folders[0])
            save_path = filedialog.askopenfilename(title="Select save file",initialdir=folder_selected)
        else:
            save_path = filedialog.askopenfilename(title="选择需要修改的Steam账号下的存档文件",initialdir=default_path)
            if not folder_selected:
                return
    if save_path:
        config = load_config()
        command = [resource_path('uesave.exe'), 'to-json', '-i', save_path, '-o', path0(config['original_path'])]
        run_command(command)
        status_label.config(text=f"Converted {save_path} to {config['original_path']}")
def uncompress_json():
    config = load_config()
    try:
        with open(path0(config['original_path']), 'r', encoding='utf-8') as file:
            original_json_data = json.load(file)
        compressed_data = original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte']
        byte_data = bytes(compressed_data)
        decompressed_data = zlib.decompress(byte_data)
        with open(path0(config['output_path_1']), 'wb') as b_file:
            b_file.write(decompressed_data)
        status_label.config(text=f"Uncompressed {config['original_path']} to {config['output_path_1']}")
    except Exception as e:
        status_label.config(text=f"Error: {e}")
def modify1():
    config = load_config()
    show_bin_editor(path0(config['output_path_1']))
def modify2():
    config = load_config()
    show_bin_editor1(path0(config['output_path_1']))
def compress_file1():
    config = load_config()
    try:
        with open(path0(config['output_path_1']), 'rb') as file:
            decompressed_data = file.read()
        compressed_data = zlib.compress(decompressed_data)
        compressed_data_array = list(compressed_data)
        with open(path0(config['original_path']), 'r', encoding='utf-8') as file:
            original_json_data = json.load(file)
        original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte'] = compressed_data_array
        original_json_data['root']['properties']['UncompressedSize']['Int']['value'] = len(decompressed_data)
        original_json_data['root']['properties']['CompressedSize']['Int']['value'] = len(compressed_data_array)
        with open(path0(config['output_path_2']), 'w', encoding='utf-8') as file:
            json.dump(original_json_data, file, ensure_ascii=False, indent=2)
        status_label.config(text=f"Compressed {config['output_path_1']} to {config['output_path_2']}")
    except Exception as e:
        status_label.config(text=f"Error: {e}")
def json_to_save():
    config = load_config()
    command = [resource_path('uesave.exe'), 'from-json', '-i', path0(config['output_path_2']), '-o', path0(config['save_path'])]
    run_command(command)
    status_label.config(text=f"Converted {config['output_path_2']} to save file")
def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")
        print("Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing command")
        print("Error message:", e.stderr.decode())
def donate1():
    webbrowser.open("https://afdian.net/a/WCHDumz")
    return
def donate2():
    webbrowser.open("https://www.patreon.com/user/shop/zan-zhu-donation-227577?u=130991073&utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=productshare_fan&utm_content=join_link")
    return
def donate3():
    webbrowser.open("https://github.com/DumzGW/-WayfinderSaveEditor-python-")
    return
from time import sleep
def uncompress():
    save_to_json()
    sleep(0.1)
    uncompress_json()
def compress():
    compress_file1()
    sleep(0.1)
    json_to_save()
print(sys.argv[0])
app = tk.Tk()
app.title("Wayfinder Save Editor")
fixed_width = 800
fixed_height = 400
app.minsize(fixed_width, fixed_height)
save_to_json_button = tk.Button(app, text="Uncompress\n选择存档文件并解压", command=uncompress)
save_to_json_button.pack(pady=5)
modifyMain_button = tk.Button(app, text="高级修改", command=GetMain)
modifyMain_button.pack(pady=5)

modify_button1 = tk.Button(app, text="(可选)Modify1阅读存档文件1", command=modify2)
modify_button2 = tk.Button(app, text="(可选)Modify2阅读存档文件2", command=modify2)
buttom_frame = tk.Frame(app)
buttom_frame.pack()
modify_button1.pack(padx=5)
modify_button2.pack(padx=5)
buttom_frame.pack(pady=10)

compress_button = tk.Button(app, text="Compress\n压缩并输出存档文件在output文件夹中", command=compress)
compress_button.pack(pady=10)

status_label = tk.Label(app, text="解压->修改->压缩，\n输出文件在output文件夹中",fg="red")
status_label.pack(pady=10)
dL1 = tk.Button(app, text="赞助",fg="blue",cursor="hand2", command=donate1)
dL1.pack(side=tk.BOTTOM, pady=0)
dL2 = tk.Button(app, text="donate",fg="blue",cursor="hand2", command=donate2)
dL2.pack(side=tk.BOTTOM, pady=0)
dL3 = tk.Button(app, text="访问github",fg="red",cursor="hand2", command=donate3)
dL3.pack(side=tk.BOTTOM, pady=10)
app.mainloop()
