import subprocess
import json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
path2 = config['output_path_2']
# 定义输入和输出路径


path1 = 'path/to/input' #新的存档位置 WayfinderSave_x.sav



command = ['./uesave.exe', 'from-json', '-i', path2, '-o', path1]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Command executed successfully")
    print("Output:", result.stdout.decode())
except subprocess.CalledProcessError as e:
    print("Error occurred while executing command")
    print("Error message:", e.stderr.decode())
