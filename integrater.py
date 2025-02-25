import os
import csv

def read_danmaku_from_files(output_dir="output"):
    """
    从output文件夹中读取所有弹幕文件，并返回去重后的弹幕列表
    """
    danmaku_set = set()  
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"):  
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    danmaku_set.add(line.strip())  
    return list(danmaku_set) 

def save_to_csv(danmaku_list, output_file="combined_danmaku.csv"):
    """
    将去重后的弹幕列表保存为CSV文件
    """
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["弹幕内容"])  # 写入CSV表头
        for danmaku in danmaku_list:
            writer.writerow([danmaku])  # 每行写入一条弹幕
    print(f"去重后的弹幕已保存到: {output_file}")

if __name__ == "__main__":
    danmaku_list = read_danmaku_from_files()
    print(f"共读取到{len(danmaku_list)}条去重后的弹幕")
    
    save_to_csv(danmaku_list)