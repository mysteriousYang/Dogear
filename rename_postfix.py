# 这个脚本用于修改文件后缀名
# 由于团子翻译器的中间文件格式有问题
# 虽然以PNG结尾，但事实上是JPG的二进制格式
# 所以需要转换文件类型，否则PS打不开
# 当然，这里不需要真的转换，改一下后缀名就可以了
# 所以没有加入任何的内容读取操作

import os
import sys

def rename_png_to_jpg(directory):
    renamed_count = 0
    skipped_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                # 获取文件路径
                png_path = os.path.join(root, file)
                
                # 创建新的JPG文件名
                base_name = os.path.splitext(file)[0]
                jpg_file = base_name + '.jpg'
                jpg_path = os.path.join(root, jpg_file)
                
                # 检查目标文件是否已存在
                if os.path.exists(jpg_path):
                    skipped_files.append((png_path, "目标文件已存在"))
                    continue
                
                try:
                    # 重命名文件
                    os.rename(png_path, jpg_path)
                    renamed_count += 1
                    print(f"已重命名: {png_path} -> {jpg_path}")
                except OSError as e:
                    skipped_files.append((png_path, f"系统错误: {str(e)}"))
    
    # 输出汇总信息
    print("\n操作完成!")
    print(f"成功重命名文件数: {renamed_count}")
    
    if skipped_files:
        print("\n以下文件未重命名:")
        for file, reason in skipped_files:
            print(f"- {file}: {reason}")

if __name__ == "__main__":
    # 获取目标目录（默认为当前目录）
    # target_dir = '.' if len(sys.argv) < 2 else sys.argv[1]

    target_dir = "./はじめてのおつかい"
    
    # 验证目录是否存在
    if not os.path.isdir(target_dir):
        print(f"错误: 目录 '{target_dir}' 不存在")
        sys.exit(1)
    
    print(f"开始处理目录: {os.path.abspath(target_dir)}")
    rename_png_to_jpg(target_dir)