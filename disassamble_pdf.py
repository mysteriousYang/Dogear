import os
import fitz  # PyMuPDF
from PIL import Image
import time

def pdf_to_png(pdf_path, output_dir, dpi=150, quality=90):
    """
    将PDF文件拆分为PNG图片
    
    参数:
    pdf_path: PDF文件路径
    output_dir: 输出目录路径
    dpi: 输出图片分辨率 (默认150)
    quality: PNG图片质量 (0-100, 默认90)
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 打开PDF文件
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"开始转换: {os.path.basename(pdf_path)}")
        print(f"总页数: {total_pages}")
        print(f"输出目录: {output_dir}")
        print(f"分辨率: {dpi} DPI")
        
        # 逐页处理
        for i, page in enumerate(doc):
            # 设置缩放因子 (DPI / 72，因为PDF默认是72 DPI)
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # 将页面渲染为Pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # 转换为PIL图像
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # 构建输出路径
            img_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
            
            # 保存为PNG
            img.save(img_path, "PNG", quality=quality, optimize=True)
            
            # 进度报告
            if (i+1) % 10 == 0 or (i+1) == total_pages:
                print(f"已转换第 {i+1}/{total_pages} 页")
        
        # 计算耗时
        elapsed = time.time() - start_time
        pages_per_sec = total_pages / elapsed if elapsed > 0 else total_pages
        
        print(f"\n转换完成! 耗时: {elapsed:.1f}秒, 平均 {pages_per_sec:.1f} 页/秒")
        print(f"图片已保存至: {output_dir}")
        return True
    
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return False
    finally:
        if 'doc' in locals():
            doc.close()

if __name__ == "__main__":
    # 配置参数
    pdf_file = "I_m_all_you_ニクジュディ成人向け再録集.pdf"  # 替换为你的PDF文件路径
    output_directory = "I_m_all_you_ニクジュディ成人向け再録集"  # 替换为输出目录路径
    
    # 高级设置 (根据需要调整)
    resolution = 200  # DPI (推荐150-300)
    image_quality = 95  # PNG质量 (0-100, 越高文件越大)
    
    # 执行转换
    pdf_to_png(pdf_file, output_directory, resolution, image_quality)