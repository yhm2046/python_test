from PIL import Image
import os

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

if __name__ == "__main__":
    # 设置图片路径
    image1_path = input("请输入第一张图片的路径: ")  # 第一张图片
    image2_path = input("请输入第二张图片的路径: ")  # 第二张图片
    output_horizontal_path = "output_horizontal.jpg"  # 输出左右拼接后图片的路径
    output_vertical_path = "output_vertical.jpg"  # 输出上下拼接后图片的路径

    # 调用拼接函数
    concatenate_images_horizontal(image1_path, image2_path, output_horizontal_path)
    concatenate_images_vertical(image1_path, image2_path, output_vertical_path)