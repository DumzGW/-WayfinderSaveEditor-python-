import tkinter as tk
from tkinter import filedialog, messagebox
import json
import subprocess
import zlib

# 加载配置
def load_config():
    with open('config.json', 'r',encoding='utf-8') as config_file:
        return json.load(config_file)

# 保存路径
def save_to_json():
    save_path = filedialog.askopenfilename(title="Select save file")
    if save_path:
        config = load_config()
        command = ['./uesave.exe', 'to-json', '-i', save_path, '-o', config['original_path']]
        run_command(command)
        status_label.config(text=f"Converted {save_path} to {config['original_path']}")

def uncompress_json():
    config = load_config()
    try:
        with open(config['original_path'], 'r', encoding='utf-8') as file:
            original_json_data = json.load(file)
        compressed_data = original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte']
        byte_data = bytes(compressed_data)
        decompressed_data = zlib.decompress(byte_data)
        with open(config['output_path_1'], 'wb') as b_file:
            b_file.write(decompressed_data)
        status_label.config(text=f"Uncompressed {config['original_path']} to {config['output_path_1']}")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def compress_file1():
    config = load_config()
    try:
        with open(config['output_path_1'], 'rb') as file:
            decompressed_data = file.read()
        compressed_data = zlib.compress(decompressed_data)
        compressed_data_array = list(compressed_data)
        with open(config['original_path'], 'r', encoding='utf-8') as file:
            original_json_data = json.load(file)
        original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte'] = compressed_data_array
        original_json_data['root']['properties']['UncompressedSize']['Int']['value'] = len(decompressed_data)
        original_json_data['root']['properties']['CompressedSize']['Int']['value'] = len(compressed_data_array)
        with open(config['output_path_2'], 'w', encoding='utf-8') as file:
            json.dump(original_json_data, file, ensure_ascii=False, indent=2)
        status_label.config(text=f"Compressed {config['output_path_1']} to {config['output_path_2']}")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def json_to_save():
    config = load_config()
    command = ['./uesave.exe', 'from-json', '-i', config['output_path_2'], '-o', config['save_path']]
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

app = tk.Tk()
app.title("Process Automation Tool")
fixed_width = 400
fixed_height = 300
app.minsize(fixed_width, fixed_height)
save_to_json_button = tk.Button(app, text="Convert Save to JSON输入存档路径", command=save_to_json)
save_to_json_button.pack(pady=10)

uncompress_button = tk.Button(app, text="Uncompress JSON解压存档文件\n请自行修改output中的'修改这个.bin'", command=uncompress_json)
uncompress_button.pack(pady=10)

compress_button = tk.Button(app, text="Compress File1压缩存档文件", command=compress_file1)
compress_button.pack(pady=10)

json_to_save_button = tk.Button(app, text="Convert JSON to Save输出修改后存档", command=json_to_save)
json_to_save_button.pack(pady=10)

status_label = tk.Label(app, text="Wayfinder Save Editor,请从上到下依次点击，\n输出文件在output文件夹中")
status_label.pack(pady=20)

app.mainloop()
