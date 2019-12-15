'''
webvtt to srt
'''
with open('Accessibility in SwiftUI/fileSequence.webvtt', 'r') as file:
    data = file.read()
    strs = data.split('\n')[3:]
    first = int(strs[0].split('-')[-1])
    print('\n'.join(strs[first:]))