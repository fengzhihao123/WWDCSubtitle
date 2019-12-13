from requests_html import HTMLSession
session = HTMLSession()
section_class = 'column large-8 small-8  padding-top-small padding-bottom-small gutter no-padding-top no-padding-bottom'
r = session.get('https://developer.apple.com/videos/wwdc2019/')
video_link_section_list = r.html.find('section.column.large-4.small-4.no-padding-top.no-padding-bottom')
video_name_section_list = r.html.find('section.column.large-8.small-8.padding-top-small.padding-bottom-small.gutter.no-padding-top.no-padding-bottom')
video_links = []
for section in video_link_section_list:
	video_link = section.find('a.video-image-link', first = True).attrs['href']
	video_links.append(video_link)

video_names = []
for section in video_name_section_list:
	h4_list = section.find('h4')
	for h4 in h4_list:
		video_names.append(h4.text)

for i, name in enumerate(video_names):
	video_combine = name + video_links[i]
	print(video_combine)


# https://developer.apple.com/videos/play/wwdc2019/257/ 
# /videos/play/wwdc2019/510/ 
