import os
import re
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def natural_sort_key(s):
    """生成自然排序键，使数字按数值大小排序"""
    return [int(c) if c.isdigit() else c.lower() for c in re.split('(\d+)', s)]

def compress_image(img, quality=85, max_dimension=2000):
    """
    压缩图片并转换为JPEG格式
    :param img: PIL图像对象
    :param quality: JPEG质量 (0-100)
    :param max_dimension: 最大边长（像素）
    :return: 压缩后的ImageReader对象
    """
    # 计算新尺寸，保持宽高比
    width, height = img.size
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # 转换为RGB模式（去除alpha通道）
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 将压缩后的图片保存到内存中
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
    img_byte_arr.seek(0)
    
    return ImageReader(img_byte_arr)

def create_pdf_from_images(folder_path, output_pdf, quality=85, max_dimension=2000):
    """
    创建压缩的PDF文件
    :param folder_path: 图片文件夹路径
    :param output_pdf: 输出PDF路径
    :param quality: 图片压缩质量 (0-100)
    :param max_dimension: 图片最大边长（像素）
    """
    # 支持的图片格式
    image_extensions = ('.png', '.jpg', '.jpeg')
    # 收集图片文件路径
    image_files = []
    
    # 遍历文件夹获取图片文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_files.append(os.path.join(folder_path, filename))
    
    if not image_files:
        print("未找到任何图片文件")
        return
    
    # 按自然排序算法排序
    image_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
    
    # 创建PDF
    c = canvas.Canvas(output_pdf, pagesize=A4)
    page_width, page_height = A4
    
    # 添加PDF元数据
    c.setTitle("图片生成PDF")
    c.setAuthor("自动生成")
    c.setSubject("图片集合")
    
    # 添加中文字体支持（可选）
    try:
        pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
        c.setFont('SimSun', 10)
    except:
        pass
    
    total = len(image_files)
    for i, image_path in enumerate(image_files):
        try:
            # 使用PIL打开图片
            img = Image.open(image_path)
            
            # 压缩图片
            img_reader = compress_image(img, quality, max_dimension)
            img_width, img_height = img_reader.getSize()
            
            # 计算缩放比例以适应A4页面
            scale_width = page_width / img_width
            scale_height = page_height / img_height
            scale = min(scale_width, scale_height)
            
            # 计算居中位置
            new_width = img_width * scale
            new_height = img_height * scale
            x_offset = (page_width - new_width) / 2
            y_offset = (page_height - new_height) / 2
            
            # 添加图片到PDF页面
            c.drawImage(img_reader, x_offset, y_offset, 
                        width=new_width, height=new_height,
                        preserveAspectRatio=True)
            
            # 添加页码（可选）
            # c.drawString(30, 30, f"{i+1}/{total}")
            
            # 添加新页面
            c.showPage()
            
            print(f"已处理: {os.path.basename(image_path)} ({i+1}/{total})")
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {str(e)}")
    
    # 保存PDF
    c.save()
    print(f"PDF已成功创建: {output_pdf}")
    print(f"文件大小: {os.path.getsize(output_pdf)/1024/1024:.2f} MB")

if __name__ == "__main__":
    # 配置参数
    folder_path = r"熟肉\IMG\[逃亡者x新桥月白日语社] (HARUCC23) [Dogear (犬耳もえ太)] やわらかな傷痕 (ズートピア)"  # 替换为你的图片文件夹路径
    output_pdf = r"熟肉\PDF\[逃亡者x新桥月白日语社] (HARUCC23) [Dogear (犬耳もえ太)] やわらかな傷痕 (ズートピア).pdf"    # 替换为想要的输出文件名
    
    # 压缩参数（根据需要调整）
    jpeg_quality = 75      # 图片压缩质量 (0-100)，建议75-85
    max_dimension = 1600   # 图片最大边长（像素），建议1200-2000
    
    # 执行转换
    create_pdf_from_images(folder_path, output_pdf, jpeg_quality, max_dimension)