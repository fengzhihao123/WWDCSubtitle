from requests_html import HTMLSession
import urllib.request
import os

def get_video_subtitle_link(video_link):
  '''
  根据视频链接获取字幕链接前缀
  Example: /videos/play/wwdc2019/257/ -> videos/wwdc/2019/257zstehah872m64ht5/
  Output: https://devstreaming-cdn.apple.com/videos/wwdc/2019/257zstehah872m64ht5/257
  '''
  r = session.get(video_link)
  video_list = r.html.find('video#video')[0].attrs['src']
  strs = video_list.split('/')[:-1]
  subtitle_prefix_url = '/'.join(strs)
  return subtitle_prefix_url

def download_subtitles_file(prefix_subtitle_url, video_name):
  '''
  根据字幕链接下载字幕文件
  '''
  root_path = '/Users/fengzhihao/WorkSpace/Code/Python/WWDCSubtitle/'
  file_path = root_path + video_name
  if not os.path.exists(file_path):
    os.makedirs(file_path)
  # 暂无法得知一个视频共多少个字幕文件，故先写死100个
  total_file_names = []
  for i in range(100):
    subtitle_url = prefix_subtitle_url + '/subtitles/zho/fileSequence{}.webvtt'.format(i)
    file_name = file_path + subtitle_url.split('/')[-1]
    urllib.request.urlretrieve(subtitle_url, file_name)
    # 判断是否为字幕文件
    file_size = os.path.getsize(file_name)
    if file_size > 30000:
      os.remove(file_name)
    # 当遇到不是字幕的文件时，合并之前所有的字幕文件
      combine_multiple_files(file_path, total_file_names)
      break
    
    total_file_names.append(file_name)

def combine_multiple_files(file_path, file_names):
  '''
  1、将字幕文件内容 - 》 string
  2、去除 webvtt 字符
  3、写入到总 subtitle 文件中
  4、删除片段字幕文件
  '''
  # 此处待优化：将文件直接依次写入一个文件中
  with open(file_path + 'fileSequence.webvtt', 'w') as outfile:
    for i, fname in enumerate(file_names):
      with open(fname) as infile:
        data = infile.read()
        new_content = remove_webvtt_repetition_content(data, i != 0)
        outfile.write(new_content)
        os.remove(fname)
    print(f"complete {file_path}")

def remove_webvtt_repetition_content(file_content, is_remove_head):
  '''
  移除webvtt中重复内容
  example: `WEBVTT
           X-TIMESTAMP-MAP=MPEGTS:181083,LOCAL:00:00:00.000`
  is_remove_head: 是否移除头部重复部分,除第一个文件后面的文件需移除头部重复部分
  '''
  data = file_content
  if is_remove_head:
    # 移除前两行 WEBVTT 格式化字符串
    strs = data.split('\n')[3:]
    # 获取头部重复行数
    first = int(strs[0].split('-')[-1])
    strs = strs[first:]
    return '\n'.join(strs)
  return data




def get_video_names(video_name_section_list):
  '''
  根据video_name_section_list来获取视频的名字
  '''
  video_names = []
  for section in video_name_section_list:
    h4_list = section.find('h4')
    for h4 in h4_list:
      video_names.append(h4.text)
  return video_names

session = HTMLSession()
section_class = 'column large-8 small-8  padding-top-small padding-bottom-small gutter no-padding-top no-padding-bottom'
r = session.get('https://developer.apple.com/videos/wwdc2019/')
video_link_section_list = r.html.find('section.column.large-4.small-4.no-padding-top.no-padding-bottom')
video_name_section_list = r.html.find('section.column.large-8.small-8.padding-top-small.padding-bottom-small.gutter.no-padding-top.no-padding-bottom')
video_links = []

wwdc_2019_host = 'https://developer.apple.com'
video_names = get_video_names(video_name_section_list)
for i, section in enumerate(video_link_section_list):
  video_link = wwdc_2019_host + section.find('a.video-image-link', first = True).attrs['href']
  prefix = get_video_subtitle_link(video_link)
  download_subtitles_file(prefix, video_names[i] + '/')

