from PIL import Image, ImageDraw, ImageFont

# 在图片上添加文本
def add_text_to_image(image_path, text, font_path, font_size):
    try:
        # 打开图片
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # 加载指定字体
        font = ImageFont.truetype(font_path, font_size)  # 使用指定字体和大小
        text_position = (10, 10)  # 文本位置
        
        # 在图片上绘制文本
        draw.text(text_position, text, fill="white", font=font)
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# 主程序
def main():
    image_path = "girl.png"  # 当前目录下的图片文件名
    text = "联系电话：0755-33374608 \n全国空降"  # 要添加的文本
    font_path = "SourceHanSansHC-Normal.otf"  # 字体文件路径（请替换为您的 OTF 字体文件名）
    font_size = 60  # 字体大小

    # 在图片上添加文本
    image_with_text = add_text_to_image(image_path, text, font_path, font_size)
    
    if image_with_text is None:
        print("Failed to process image.")
        return
    
    # 显示或保存图片
    image_with_text.show()  # 显示图片
    image_with_text.save("girl_with_text.png")  # 保存为新文件

if __name__ == "__main__":
    main()