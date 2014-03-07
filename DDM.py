from urllib import request
import time
from os import path
import os

def urlRequest(url):
	try:
		u = request.urlopen(request.Request(url,method="HEAD"))
		return u
	except:
		print("Please check the url entered and try again.")

def fileInput(url,mode):
	try:
		folder = input("Enter Folder Path : ")
		if not path.exists(folder) and path.isdir(folder):
			os.mkdir(folder)
		fileName = input("Enter File Name (Default : " + url.split("/")[-1] +") : ")
		if fileName == "":
			fileName = url.split("/")[-1]
		f = open(folder + "/" + fileName, 'a+b') if mode == 0 else open(folder + "/" + fileName, 'w+b')
		return f
	except:
		print("A problem occured while creating file and try again.")
		fileInput(url,mode)

def download(f,url,seek):
	req = request.Request(url)
	if seek != 0:
		req.add_header("Range", "bytes=" + str(seek) +"-")
	u = request.urlopen(req)
	meta = u.info()
	file_size = int(meta.__getitem__("Content-Length"))
	print("Downloading: %s Bytes : " % (file_size))
	file_size_dl = 0
	block_sz = 8096
	millis = int(round(time.time() * 1000))
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break
		file_size_dl += len(buffer)
		f.write(buffer)
		newt = int(round(time.time() * 1000))
		t = newt-millis if newt-millis!=0 else 1
		status = "%12d [%3.2f%%] [%7.2f kbps]" % (file_size_dl, file_size_dl * 100. / file_size, file_size_dl * 1. / t);
		print(status,end="\r")
	

def main():
	url = input("Enter Download URL : ")
	u = urlRequest(url)
	if u != None:
		meta = u.info()
		downloadSize = int(meta.__getitem__("Content-Length"))/1024
		resumable = "resumable" if meta.__getitem__("Accept-Ranges") == "bytes" else "not resumable"
		print("This is a %s download of %10.3f kb" % (resumable, downloadSize))
		f = fileInput(url,0) if resumable == "resumable" else fileInput(url,1)
		seek = f.seek(0,2)
		if seek > 0:
			print("Resuming Download")
		download(f,url,seek)
		f.close()
	

if __name__ == "__main__":
	main()
