from PIL import Image
import math

def calculate_quality(image_size, max_size=7000*7000, min_quality=30, max_quality=95):
    """
    根据图像尺寸计算压缩质量，使用反向对数函数
    :param image_size: 图像的尺寸（宽度*高度）
    :param max_size: 最大尺寸（宽度*高度），默认值为1000*1000
    :param min_quality: 最小质量，默认值为30
    :param max_quality: 最大质量，默认值为95
    :return: 压缩质量
    """
    if image_size > max_size:
        quality = min_quality
    else:
        scale = image_size / max_size
        quality = max_quality - (max_quality - min_quality) * math.log10(scale + 1)
        quality = min(quality, max_quality)
        quality = max(quality, min_quality)
    return int(quality)

def compress_image(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        # 获取图像的尺寸（宽度*高度）
        image_size = img.width * img.height
        # 计算压缩质量
        quality = calculate_quality(image_size)
        # 检查图像格式
        img_format = img.format
        if img_format in ['JPEG', 'JPG', 'PNG']:
            # 压缩并保存图像
            img.save(output_image_path, format=img_format, quality=quality, optimize=True)
            print(f"Image saved with quality={quality}")
        else:
            print("Unsupported image format")

""" # 示例使用
input_path = 'in_test.JPG'  # 输入图像的路径
output_path = 'out_test.JPG'  # 输出压缩后图像的路径
compress_image(input_path, output_path)
 """