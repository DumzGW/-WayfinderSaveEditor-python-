import subprocess
import json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
path2 = config['original_path']
# 定义输入和输出路径


path1 = 'path/to/input' #存档位置 例如："C:/Users/xxx/AppData/Local/Wayfinder/Saved/SaveGames/xxxxx/WayfinderSave_x.sav"


command = ['./uesave.exe', 'to-json', '-i', path1, '-o', path2]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Command executed successfully")
    print("Output:", result.stdout.decode())
except subprocess.CalledProcessError as e:
    print("Error occurred while executing command")
    print("Error message:", e.stderr.decode())
