'''
webvtt to srt
'''
with open('/Users/fengzhihao/Desktop/fileSequence0.webvtt', 'r') as file:
    # data = file.read()
    # strs = data.split('\n')[3:]
    # first = int(strs[0].split('-')[-1])
    # print('\n'.join(strs[first:]))
    result = list()
    empty_line = 0
    lines = file.readlines()
    for line in lines:
      if empty_line > 1:
        result.append(line)
      if len(line) == 1:
        empty_line += 1
    print(result)
          