import zlib
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

original = config['original_path']
input = config['output_path_1']
output = config['output_path_2']
# input='改.bin'
# original='save.json'
# output='new.json'
# 读取修改后的 JSON 文件
with open(input, 'rb') as file:
    decompressed_data = file.read()
# 使用 zlib 重新压缩数据
compressed_data = zlib.compress(decompressed_data)

# 将压缩后的数据转换为字节数组（0-255）
compressed_data_array = list(compressed_data)

# 从原始 JSON 文件中读取数据
with open(original, 'r', encoding='utf-8') as file:
    original_json_data = json.load(file)

# 更新原始 JSON 文件中的压缩数据
original_json_data['root']['properties']['Buffer_CompressedJSONSaveGameContainer']['Array']['value']['Base']['Byte']['Byte'] = compressed_data_array
original_json_data['root']['properties']['UncompressedSize']['Int']['value'] = len(decompressed_data)
original_json_data['root']['properties']['CompressedSize']['Int']['value'] = len(compressed_data_array)
print("压缩后的数据长度:", len(compressed_data_array))
byte_data = bytes(compressed_data)
decompressed_data = zlib.decompress(byte_data)
print("解压后的数据长度:", len(decompressed_data))

# 将更新后的数据写回到原始 JSON 文件中
with open(output, 'w', encoding='utf-8') as file:
    json.dump(original_json_data, file,ensure_ascii=False,indent=2)
print("更新后的数据已写入json文件")