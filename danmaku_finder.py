import requests
import re
import os
import time
from bs4 import BeautifulSoup

def get_cid(bvid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": "your cookie"
    }
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}"
    response = requests.get(url, headers=headers)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text[:200]}")
    try:
        data = response.json()
        if data["code"] == 0:
            return data["data"][0]["cid"]
        else:
            print(f"API返回错误: {data['message']}")
            return None
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的JSON格式")
        return None

def get_danmaku(cid):
    """
    根据视频的cid获取弹幕数据
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Cookie": "your cookie"
    }
    url = f"https://comment.bilibili.com/{cid}.xml"
    
    # 发送HTTP请求
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"  # 确保中文不乱码
    
    # 解析XML数据
    soup = BeautifulSoup(response.text, "lxml-xml")
    danmaku_list = soup.find_all("d")
    
    # 正则表达式匹配列表形式的弹幕
    pattern = re.compile(r'\["[^"]+","[^"]+","[^"]+","[^"]+","([^"]+)",[^\]]+\]')

    danmaku_contents = []
    for danmaku in danmaku_list:
        text = danmaku.text
        match = pattern.search(text)
        if match:
            # 提取第五个元素（弹幕内容）
            danmaku_contents.append(match.group(1))
        else:
            danmaku_contents.append(danmaku.text)
    
    return danmaku_contents

def save_to_file(danmaku_list, cid, output_dir="output"):
    """
    将弹幕保存到文件，文件名为cid，保存到output文件夹
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f"{cid}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for danmaku in danmaku_list:
            f.write(danmaku + "\n")
    print(f"弹幕已保存到: {filename}")

def read_bvid_from_file(input_dir="input"):
    """
    从input文件夹中的bvid.txt文件中读取所有bvid
    """
    file_path = os.path.join(input_dir, "bvid.txt")
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        bvid_list = [line.strip() for line in f if line.strip()]  
        return bvid_list

def get_existing_cids(output_dir="output"):
    """
    获取output文件夹中已经存在的cid列表
    """
    existing_cids = set()
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"): 
            cid = filename[:-4]
            existing_cids.add(cid)
    return existing_cids

if __name__ == "__main__":
    existing_cids = get_existing_cids()
    print(existing_cids)

    bvid_list = read_bvid_from_file()
    if bvid_list:
        for bvid in bvid_list:
            print(f"正在处理bvid: {bvid}")
            cid = get_cid(bvid)
            if cid:
                if str(cid) in existing_cids:
                    print(f"cid {cid} 已存在，跳过该视频")
                    continue  # 跳过已存在的cid

                print(f"视频的cid为: {cid}")
                danmaku_data = get_danmaku(cid)
                save_to_file(danmaku_data, cid)
                print(f"已爬取{len(danmaku_data)}条弹幕，保存到output/{cid}.txt")
            else:
                print(f"无法获取cid，请检查视频编号 {bvid} 或网络连接。")
            
            print("等待3秒后继续处理下一个视频...")
            time.sleep(3) 
    else:
        print("无法读取bvid，请检查input/bvid.txt文件是否存在且格式正确。")