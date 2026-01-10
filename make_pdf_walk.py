# 这个脚本是用来生成PDF文件的
# 它可以把某个给定目录下所有的子文件夹全部生成为对应名称的PDF文件
# 是的，它用于把IMG文件夹下的本子转换到PDF文件夹下

import os
import re
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------
# 你原来的工具函数（保持不变）
# ---------------------------

def natural_sort_key(s):
    return [int(c) if c.isdigit() else c.lower()
            for c in re.split('(\d+)', s)]

def compress_image(img, quality=85, max_dimension=2000):
    width, height = img.size
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        img = img.resize(
            (int(width * ratio), int(height * ratio)),
            Image.LANCZOS
        )

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG',
             quality=quality, optimize=True)
    img_byte_arr.seek(0)

    return ImageReader(img_byte_arr)

def create_pdf_from_images(folder_path, output_pdf,
                           quality=85, max_dimension=2000):

    image_extensions = ('.png', '.jpg', '.jpeg')
    image_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_files.append(os.path.join(folder_path, filename))

    if not image_files:
        print(f"⚠️ 跳过空文件夹: {folder_path}")
        return

    image_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))

    c = canvas.Canvas(output_pdf, pagesize=A4)
    page_width, page_height = A4

    try:
        pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
        c.setFont('SimSun', 10)
    except:
        pass

    total = len(image_files)
    for i, image_path in enumerate(image_files):
        try:
            img = Image.open(image_path)
            img_reader = compress_image(img, quality, max_dimension)
            img_width, img_height = img_reader.getSize()

            scale = min(page_width / img_width, page_height / img_height)
            new_width = img_width * scale
            new_height = img_height * scale

            x_offset = (page_width - new_width) / 2
            y_offset = (page_height - new_height) / 2

            c.drawImage(
                img_reader,
                x_offset,
                y_offset,
                width=new_width,
                height=new_height,
                preserveAspectRatio=True
            )

            c.showPage()
            print(f"  已处理 {i+1}/{total}: {os.path.basename(image_path)}")

        except Exception as e:
            print(f"处理失败 {image_path}: {e}")

    c.save()
    print(f"✅ 生成完成: {output_pdf}")

# --------------------------------
# 新增：批量处理子文件夹的函数
# --------------------------------

def batch_folders_to_pdfs(root_dir, out_dir,
                          quality=85, max_dimension=2000):
    """
    root_dir: 包含多个子文件夹的目录
    out_dir: PDF 输出目录
    """

    os.makedirs(out_dir, exist_ok=True)

    for name in sorted(os.listdir(root_dir)):
        folder_path = os.path.join(root_dir, name)

        if not os.path.isdir(folder_path):
            continue

        output_pdf = os.path.join(out_dir, f"{name}.pdf")

        print(f"\n📘 正在处理文件夹: {name}")
        create_pdf_from_images(
            folder_path,
            output_pdf,
            quality=quality,
            max_dimension=max_dimension
        )

# ---------------------------
# 示例用法
# ---------------------------

if __name__ == "__main__":
    input_dir = r"生肉/IMG"      # 你的图片根目录
    output_dir = r"生肉/PDF"  # PDF 输出目录

    batch_folders_to_pdfs(input_dir, output_dir)
