import os
import json

def process_json_files():
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.lower().endswith('.json'):
                json_path = os.path.join(root, file)
                try:
                    # 读取JSON文件
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 检查text_block字段
                    if 'text_block' not in data or not isinstance(data['text_block'], list):
                        print(f"警告: {json_path} 缺少有效的text_block字段，跳过")
                        continue
                    
                    output_lines = []
                    # 处理每个text_block对象
                    for idx, text_obj in enumerate(data['text_block'], 1):
                        if not isinstance(text_obj, dict) or 'texts' not in text_obj:
                            print(f"警告: {json_path} 中的text_block_{idx} 格式无效，跳过")
                            continue
                        
                        if not isinstance(text_obj['texts'], list):
                            print(f"警告: {json_path} 中的text_block_{idx} 的texts字段不是列表，跳过")
                            continue
                        
                        # 添加text_block标题
                        output_lines.append(f"text_block_{idx}")
                        # 添加文本内容
                        for text in text_obj['texts']:
                            output_lines.append(str(text))
                        # 添加空行分隔
                        output_lines.append('')
                    
                    # 生成输出文件路径
                    txt_path = os.path.splitext(json_path)[0] + '.txt'
                    
                    # 写入TXT文件
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(output_lines))
                    
                    print(f"成功生成: {txt_path}")
                
                except json.JSONDecodeError:
                    print(f"警告: {json_path} 不是有效的JSON文件，跳过")
                except Exception as e:
                    print(f"处理 {json_path} 时出错: {str(e)}，跳过")

if __name__ == "__main__":
    process_json_files()