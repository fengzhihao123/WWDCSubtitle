from requests_html import HTMLSession
import urllib.request
import os
import requests

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



def download_subtitles_file(subtitle_urls, video_name):
  '''
  根据字幕链接下载字幕文件
  '''
  file_path = root_path 
  cur_file_name = root_path + video_name + '.webvtt'
  if os.path.exists(cur_file_name):
    print(f'''{video_name} is already download''')
    # 已经存在此文件
    return

  total_file_names = []
  for subtitle_url in subtitle_urls:
    if '<' in subtitle_url:
      print(f'''{video_name} subtitle url is error''')
      return
    file_name = file_path + subtitle_url.split('/')[-1]
    total_file_names.append(file_name)
  # 合并当前视频所有的字幕文件
  combine_multiple_files(file_path, total_file_names, video_name)



def combine_multiple_files(file_path, file_names, video_name):
  '''
  1、将字幕文件内容 - 》 string
  2、去除 webvtt 字符
  3、写入到总 subtitle 文件中
  4、删除片段字幕文件
  '''
  # 此处待优化：将文件直接依次写入一个文件中
  target_file = video_name + '.webvtt'
  with open(file_path + target_file, 'w') as outfile:
    for i, fname in enumerate(file_names):
      with open(fname) as infile:
        result = list()
        lines = infile.readlines()
        if i != 0:
          empty_line = 0
          for line in lines:
            if empty_line > 1:
              result.append(line)
            if len(line) == 1:
              empty_line += 1
          content = "".join(result)
        else:
          content = "".join(lines)
        outfile.write(content)
        os.remove(fname)
    print(f"complete {file_path}")



def remove_webvtt_repetition_content(fname, is_remove_head):
  '''
  移除webvtt中重复内容
  example: `WEBVTT
           X-TIMESTAMP-MAP=MPEGTS:181083,LOCAL:00:00:00.000`
  is_remove_head: 是否移除头部重复部分,除第一个文件后面的文件需移除头部重复部分
  '''
  with open(fname) as file:
    content = file.read()
    if is_remove_head:
      result = list()
      empty_line = 0
      lines = file.readlines()
      for line in lines:
        if empty_line > 1:
          result.append(line)
        if len(line) == 1:
          empty_line += 1
      content = "".join(result)
  return content



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



def get_subtitle_count(prefix, prog_index_url, video_name):
  '''
  获取当前视频的字幕个数，及字幕名字
  '''
  file_path = root_path + video_name
  if os.path.exists(file_path):
    # 已经存在此文件夹
    return

  r = requests.get(prog_index_url)
  content = str(r.content)[1:]
  total_list = content.split('\\n')[6:-1]
  subtitles = total_list[0::2]
  complete_subtitles = []
  for subtitle in subtitles:
    complete_subtitles.append(prefix + '/subtitles/zho/' + subtitle)
  print(f'''start {video_name}''')
  download_subtitles_file(complete_subtitles, video_name)


root_path = '/Users/fzh/workspace/WWDCSubtitle/srt_substitle/wwdc2019/'

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
  prog_index_url = prefix + '/subtitles/zho/prog_index.m3u8'
  get_subtitle_count(prefix, prog_index_url, video_names[i])



'''
keynote

'''
