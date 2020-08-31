
#standard library imports
import time
import os.path
import os
import glob

#third party imports
from PIL import Image
import skimage

def init(*, logFolderPath):
	global logPath
	global logPathExists
	global logFiles
	global logIncrement
	global fileOrder
	logPath = logFolderPath
	logPathExists = os.path.isdir(logPath)
	startupClear()
	logFiles = {}
	logIncrement = {}
	fileOrder = 0

def startupClear():
	global logPath
	global logPathExists
	if logPathExists:
		imageFiles = glob.glob(os.path.join(logPath, '*.bmp'))
		for image in imageFiles:
			os.remove(image)
		textFiles = glob.glob(os.path.join(logPath, '[!0]*.txt'))
		for text in textFiles:
			os.remove(text)

def terminalMessage(message):
	print(str(time.perf_counter()) + ': ' + message)

def start(logName):
	global logPath
	global logFiles
	global logIncrement
	global fileOrder
	global logPathExists
	if logPathExists:
		if logName in logIncrement:
			logIncrement[logName] = logIncrement[logName] + 1
		else:
			logIncrement[logName] = 1
		fileOrder = fileOrder + 1
		filePath = os.path.join(logPath, str(fileOrder) + '-' + \
		logName + str(logIncrement[logName]) + '.txt')
		logFiles[logName] = open(filePath, 'w', encoding='utf-8')

def write(logName, message):
	global logFiles
	global logPathExists
	if logPathExists:
		logFiles[logName].write(str(time.perf_counter()) + '\n' + message + '\n')
	
def cleanWrite(logName, message):
	global logFiles
	global logPathExists
	if logPathExists:
		logFiles[logName].write(message + '\n')
 
def end(logName):
	global logFiles
	global logPathExists
	if logPathExists:
		logFiles[logName].close()
	
def saveImage(image, name):
	global logPath
	global fileOrder
	global logPathExists
	if logPathExists:
		fileOrder = fileOrder + 1
		filePath = os.path.join(logPath, str(fileOrder) + '-' + name + '.bmp')
		image.save(filePath)
		return image
		
def saveNumpyImage(image, name):
	global logPath
	global fileOrder
	global logPathExists
	if logPathExists:
		fileOrder = fileOrder + 1
		filePath = os.path.join(logPath, str(fileOrder) + '-' + name + '.bmp')
		image = Image.fromarray(skimage.img_as_ubyte(image))
		image.save(filePath)
		return image