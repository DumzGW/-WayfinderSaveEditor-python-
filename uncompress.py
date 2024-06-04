import zlib
import struct
import json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

original = config['original_path']
output = config['output_path_1']
# original='save.json'
# output='改.bin'
# 从原始 JSON 文件中读取数据
with open(original, 'r', encoding='utf-8') as file:
    original_json_data = json.load(file)

# 更新原始 JSON 文件中的压缩数据
compressed_data=original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte']

# 将字节数组转换为字节对象
byte_data = bytes(compressed_data)
# 使用zlib解压缩
try:
    decompressed_data = zlib.decompress(byte_data)
    print("解压后的数据长度:", len(decompressed_data))
except zlib.error as e:
    print(f"解压缩失败: {e}")
    decompressed_data = None

if decompressed_data:


    with open(output, 'wb') as b_file:
        b_file.write(decompressed_data)
  
else:
    print("解压缩失败，可能数据不完整或损坏。")