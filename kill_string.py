import os
import re

def rename_mp3_files():
    # 要删除的字符串模式
    remove_pattern = r'【游鸿明】音乐歌曲视频MV合集\s*p?\d*\s*'
    
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 遍历当前目录下的所有文件
    for filename in os.listdir(current_dir):
        # 检查文件是否是 .mp3 文件
        if filename.endswith('.mp3'):
            # 使用正则表达式删除指定模式
            new_filename = re.sub(remove_pattern, '', filename)
            
            # 如果文件名有变化
            if new_filename != filename:
                # 构建完整的文件路径
                old_file = os.path.join(current_dir, filename)
                new_file = os.path.join(current_dir, new_filename)
                
                # 重命名文件
                try:
                    os.rename(old_file, new_file)
                    print(f"已重命名: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"重命名 {filename} 时出错: {str(e)}")
            else:
                print(f"跳过: {filename} (不包含要删除的字符串)")

if __name__ == "__main__":
    rename_mp3_files()
    input("按任意键退出...")