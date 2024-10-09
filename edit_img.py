import os
from PIL import Image

def concatenate_images_horizontal(image1_path, image2_path, output_path):
    """左右拼接图片"""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # 获取两张图片的宽度和高度
    width1, height1 = img1.size
    width2, height2 = img2.size

    # 计算拼接后图片的宽度和高度
    total_width = width1 + width2
    max_height = max(height1, height2)

    # 创建一个新的空白图片
    new_image = Image.new('RGB', (total_width, max_height))

    # 将第一张图片粘贴到新图片的左侧
    new_image.paste(img1, (0, 0))
    # 将第二张图片粘贴到新图片的右侧
    new_image.paste(img2, (width1, 0))

    # 保存拼接后的图片
    new_image.save(output_path)
    print(f"左右拼接后的图片已保存为: {output_path}")

def concatenate_images_vertical(image1_path, image2_path, output_path):
    """上下拼接图片"""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # 获取两张图片的宽度和高度
    width1, height1 = img1.size
    width2, height2 = img2.size

    # 计算拼接后图片的宽度和高度
    max_width = max(width1, width2)
    total_height = height1 + height2

    # 创建一个新的空白图片
    new_image = Image.new('RGB', (max_width, total_height))

    # 将第一张图片粘贴到新图片的上方
    new_image.paste(img1, (0, 0))
    # 将第二张图片粘贴到新图片的下方
    new_image.paste(img2, (0, height1))

    # 保存拼接后的图片
    new_image.save(output_path)
    print(f"上下拼接后的图片已保存为: {output_path}")

def process_folders(base_path):
    """遍历指定路径下的所有文件夹并合并图片"""
    for root, dirs, files in os.walk(base_path):
        # 过滤出图片文件（假设为 jpg 和 png 格式）
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # 确保至少有两张图片进行拼接
        if len(image_files) >= 2:
            # 取前两张图片进行拼接
            image1_path = os.path.join(root, image_files[0])
            image2_path = os.path.join(root, image_files[1])

            # 定义输出路径
            output_horizontal_path = os.path.join(root, "output_horizontal.jpg")
            output_vertical_path = os.path.join(root, "output_vertical.jpg")

            # 调用拼接函数
            concatenate_images_horizontal(image1_path, image2_path, output_horizontal_path)
            concatenate_images_vertical(image1_path, image2_path, output_vertical_path)

if __name__ == "__main__":
    # 设置图片根路径
    base_path = input("请输入包含多个文件夹的路径: ")  # 输入路径
    process_folders(base_path)