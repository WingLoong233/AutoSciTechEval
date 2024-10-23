import json
import os

# 设置要提取的字符数
extract_length = 100000  # 您可以根据需要修改这个值

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输入和输出文件的完整路径
input_file = os.path.join(current_dir, 'SciKG_min_1.0.json')
output_file = os.path.join(current_dir, f'scikg_extract_{extract_length}.json')

try:
    # 读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read(extract_length)

    # 确保截取的内容是有效的JSON
    try:
        json.loads(data)
    except json.JSONDecodeError:
        # 如果不是有效的JSON,找到最后一个完整的对象
        last_brace = data.rfind('}')
        if last_brace != -1:
            data = data[:last_brace+1]
        else:
            raise ValueError(f"无法在前{extract_length}个字符中找到有效的JSON对象")

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"已成功提取前{extract_length}个字符并保存到 {output_file} 文件中。")

except FileNotFoundError:
    print(f"错误：找不到输入文件 {input_file}")
except PermissionError:
    print(f"错误：没有权限写入文件 {output_file}")
except Exception as e:
    print(f"发生错误：{str(e)}")