import requests
import json
from fake_useragent import UserAgent
import time
import urllib.parse
import datetime
import os
import subprocess
import configparser
import zhconv
# from upload_video import user_upload
 
def run_cmd(command, vedio_path, b_title):
    # 打开命令提示符窗口
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  
    # 读取命令输出
    output, error = process.communicate()
    
    if output:
        if (os.path.exists(vedio_path)):
            # user_upload(vedio_path,title)
            filepath = vedio_path
            video_list = os.listdir(filepath)
            for v in video_list:
            	v_type = v[-4:]
            	v_name = v[:-4]
            	if (v_type != '.mp4'):
            		continue
            	meta_file = b_title + '.info.json'
            	if (os.path.exists(filepath+'/'+meta_file)):
            		pass
            	else:
            		print(filepath+'/'+meta_file)
            		print('文件不存在')
            		continue
            	with open(filepath+'/'+meta_file, 'r', encoding='utf8')as js:
            		meta_info = json.load(js)
            		v_id = meta_info['id']
            		source_title = meta_info['title']
            		dst_title = zhconv.convert(source_title, 'zh-cn')
            		v_title = dst_title
            		v_tag = meta_info['tags']
            		v_desc = meta_info['description']
            		video_path = filepath + '/'+v
            		uploader_id = meta_info['uploader_id']
            		
            	s_tag = ", ".join(v_tag)
            	up_data = {}
            	up_data['title'] = v_title
            	up_data['description'] = v_desc
            	up_data['keywords'] = s_tag
            	up_data['category'] = '24'
            	up_data['privacyStatus'] = 'public'
            	up_data['id'] = v_id
            	up_data['uploader_id'] = uploader_id
            	up_data['file'] = video_path
            	up_data['path'] = filepath
            	
            	# 没有下载过，把上传的标题、路径保存下载
            	config = configparser.ConfigParser()
            	config['upList'] = up_data
            	
            	# 清空文件内容
            	with open('data.ini', 'w') as configfile:
            		configfile.write('')
            		
            	# 保存数据到 INI 文件
            	with open('data.ini', 'a',encoding='utf-8') as configfile:
            		config.write(configfile)
            print('路径存在：'+vedio_path)
            # ======================调用上传=====================
            # 要调用的Python文件和命令模板
            python_file = 'upload_video.py'
            command_ = 'python3 {file} --file="{video_file}" --title="{title}" --description="{description}" --keywords="{keywords}" --category="{category}" --privacyStatus="{privacy}"'
            # 创建 ConfigParser 实例
            config = configparser.ConfigParser()
            # 读取 INI 文件
            config.read('data.ini',encoding='utf-8')
            # 获取指定节（section）下的键值对
            vendor_data = config['upList']
            # 填充命令模板的参数
            video_file = vendor_data['file']
            title = vendor_data['title']
            description = vendor_data['description']
            keywords = vendor_data['keywords']
            category = vendor_data['category']
            privacy =  vendor_data['privacystatus']
            command = command_.format(file=python_file,video_file=video_file,title=title,description=description,keywords=keywords,category=category,privacy=privacy)
            # 调用其他Python文件并执行命令
            subprocess.run(command, shell=True)
        else:
            print('路径不存在：'+vedio_path)
    if error:
        print(error.decode('gbk', 'ignore'))

def main(api_url, author, total_pages,cookie):
    # 创建伪装用户代理
    iswrite = False
    ua = UserAgent()
    base_video_url = "https://www.bilibili.com/video"
 
    # 清空已存在的文件内容或创建新文件
    # file_name = f"{author}.txt"
    # with open(file_name, "w", encoding="utf-8") as file:
    #     file.write("")
 
    # 解析URL中的查询参数
    query_params = urllib.parse.parse_qs(urllib.parse.urlparse(api_url).query)
    # 创建一个新的字典，将查询参数转换为键值对，排除 'pn' 参数
    params = {key: value[0] for key, value in query_params.items() if key != 'pn'}
 
    # 解析URL中的基础部分（去除参数部分）
    parsed_url = urllib.parse.urlparse(api_url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
 
    # 发送GET请求获取每个页面的内容
    for page in range(1, total_pages + 1):  # 从第1页到总页数
        # 设置分页参数
        params["pn"] = str(page)
 
        # 伪装用户代理头和其他请求头
        headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.bilibili.com/",
            "Cookie": cookie  # 添加 Cookie
        }
 
        # 发送GET请求获取JSON数据
        response = requests.get(base_url, params=params, headers=headers)
        print(response.url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON数据
            data = response.json()
            # print(data)
            # 获取包含视频信息的列表
            video_list = data['data']['list']['vlist']
             
            # 遍历视频信息列表，提取bvid和author字段，并保存到文件中
            if len(video_list) > 0:
                print(f"请求第 {page} 页成功。获取到" + str(len(video_list)) + "个链接\n")
                for video in video_list:
                    bvid = video.get("bvid", "")
                    title = video.get("title", "")

                    if bvid and not iswrite:
                        # with open(file_name, "a", encoding="utf-8") as file:
                        #     file.write(base_video_url + "/" + bvid + "\n")
                        # 保存视频
                        date = datetime.datetime.now()
                        date = date.strftime('%Y%m%d')
                        vedio_path = author + '/vedio/' + date
                        command_ = save_path + 'yt-dlp_linux --playlist-end 1 --download-archive ' + save_path + 'DownLoadFile --write-info-json --write-sub --sub-format srt --sub-lang zh-Hans -S res,ext:mp4:m4a --recode mp4 -o ' + save_path + vedio_path + '/' + '%\(title\)s.%\(ext\)s ' + base_video_url + "/" + bvid
                        print(command_)
                        run_cmd(command_, save_path + vedio_path, title)
                        iswrite = True
                        break
                        #print(f"成功保存 bvid: {bvid} 到 {file_name}")
            else:
                print(f"请求第 {page} 页无数据。\n")
                break
        else:
            print(f"请求第 {page} 页失败。")
 
        # 随机休眠一段时间，模拟人类行为
        time.sleep(10)
 
    print("下载完成.")
 
save_path = os.getcwd() + '/'
if __name__ == "__main__":
    # 定义 API URL、作者和总页数
    api_url = "https://api.bilibili.com/x/space/wbi/arc/search?mid=194024972&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&dm_img_list=[%7B%22x%22:738,%22y%22:179,%22z%22:0,%22timestamp%22:156,%22type%22:0%7D,%7B%22x%22:907,%22y%22:125,%22z%22:79,%22timestamp%22:332,%22type%22:0%7D]&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgKDB4MDAwMDlCNDEpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKEludGVsKQ&w_rid=9c462d83882c62e0a8f4154d6d03c9c6&wts=1699605889"
    author = ""
    total_pages = 1  # 你在最前面定义的总页数
    # 定义 Cookie
    cookie = (
        "b_nut=1656031316; buvid3=63A52786-2439-C710-40E7-7038B3535FC439181infoc; buvid4=62CCB7CC-5181-1A16-1DE3-2C5304D33B0239181-022062408-0bHjNvpdrqQHqPoB61I9wA%3D%3D; buvid_fp=74f668f9d485981f111c4a1d80da3313; CURRENT_FNVAL=4048; rpdid=|(k|kl)lRkY|0J'uY~mJY~Jlk; CURRENT_PID=94c03f90-e31c-11ed-acc2-09d3a3069e7b; i-wanna-go-back=-1; _uuid=BA755DDE-10BA9-6227-31F4-2EA3C8EF66F245991infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; b_ut=5; innersign=0; b_lsid=ED9AF24A_18BB84740A4; enable_web_push=DISABLE; home_feed_column=4; bp_video_offset_3546391240510141=844871774252302344; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk4NjUwNDQsImlhdCI6MTY5OTYwNTc4NCwicGx0IjotMX0.ywIsGT9Xn1EBCc4x4YOcQgiPfyuXSar_bscKtoGI8sg; bili_ticket_expires=1699864984; browser_resolution=1218-556; sid=8187a919"
    )
    # 调用主函数
    main(api_url, author, total_pages,cookie)

    
    

    

