from pytube import YouTube
import enquiries
import sys
from pathlib import Path

url = input('url: ')

def progressBar(stream, _chunk, bytes_remaining):
	current = ((stream.filesize - bytes_remaining	) / stream.filesize)
	percent = ('{0:.0f}').format(current * 100)
	bytess = ('{0:.3f}').format(round((stream.filesize - bytes_remaining) / (10**6), 3))
	progress = int(50 * current)
	status = '█' * progress
	sys.stdout.write('↳ {bar} {percent}% - {downloadedMB}MB / {fileMB}MB\r'.format(
		bar = status,
		percent = percent,
		downloadedMB = bytess,
		fileMB = round(stream.filesize / (10**6))
	))

def completeCb(stream, file_path):
	print('\n\nVideo downloaded at ' + file_path)

def yesNo(question):
	options = ['yes', 'no\n']
	confirm = enquiries.choose(question, options)
	return True if confirm == 'yes' else False

try: 
	video = YouTube(
		url,
		on_progress_callback=progressBar,
		on_complete_callback=completeCb
	)
except Exception as err:
	print('unvalid url')
	print(err)
	exit()

print('\ntitle: ' + video.title)
print('views: ' + str(video.views))
myVideo = video.streams.filter(file_extension='mp4', progressive=True)
resolution = [ stream.resolution for stream in myVideo ]
resChoice = enquiries.choose('\nChoose the resolution of the video: ', resolution)
print('Video resolution: ' + str(resChoice))

fileName = input('File name: ')

fileDest = yesNo('\nSpecify file destination (default: /video)')
if (fileDest):
	x = input('/')
	path = '/' + x
	print('File Destination: ' + path)
else:
	path = str(Path().absolute()) + '/videos'
	print('File Destination: ' + path)

def youtubeDownloader(video, resolution, path, fileName):
	try:
		video.streams.filter(res=resolution).first().download(path, fileName)
	except ValueError as err:
		print(err)
		print('impossible connexion')
		exit()

print('\n')
youtubeDownloader(video,
	resChoice,
	path,
	fileName
) if yesNo('Start downloading?') else exit()