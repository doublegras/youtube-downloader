from pytube import YouTube
import enquiries
import sys
from pathlib import Path

url = input('url: ')

def progress_bar(stream, _chunk, bytes_remaining):
	current = ((stream.filesize - bytes_remaining	) / stream.filesize)
	percent = ('{0:.0f}').format(current * 100)
	bytess = ('{0:.3f}').format(round((stream.filesize - bytes_remaining) / (10**6), 3))
	progress = int(50 * current)
	status = '█' * progress
	sys.stdout.write('↳ {bar} {percent}% - {downloaded_MB}MB / {fileMB}MB\r'.format(
		bar = status,
		percent = percent,
		downloaded_MB = bytess,
		fileMB = round(stream.filesize / (10**6))
	))

def complete_cb(stream, file_path):
	print('\n\nVideo downloaded at ' + file_path)

def yes_no(question):
	options = ['yes', 'no\n']
	confirm = enquiries.choose(question, options)
	return True if confirm == 'yes' else False

try: 
	video = YouTube(
		url,
		on_progress_callback=progress_bar,
		on_complete_callback=complete_cb
	)
except Exception as err:
	print('unvalid url')
	print(err)
	exit()

print('\ntitle: ' + video.title)
print('views: ' + str(video.views))
my_video = video.streams.filter(file_extension='mp4', progressive=True)
resolution = [ stream.resolution for stream in my_video ]
res_choice = enquiries.choose('\nChoose the resolution of the video: ', resolution)
print('Video resolution: ' + str(res_choice))

file_name = input('File name: ')

file_dest = yes_no('\nSpecify file destination (default: /video)')
if (file_dest):
	x = input('/')
	path = '/' + x
	print('File Destination: ' + path)
else:
	path = str(Path().absolute()) + '/videos'
	print('File Destination: ' + path)

def youtube_downloader(video, resolution, path, file_name):
	try:
		video.streams.filter(res=resolution).first().download(path, file_name)
	except ValueError as err:
		print(err)
		print('impossible connexion')
		exit()

print('\n')
youtube_downloader(video,
	res_choice,
	path,
	file_name
) if yes_no('Start downloading?') else exit()