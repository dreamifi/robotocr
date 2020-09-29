
#local imports
from . import log

#standard library imports
from tempfile import TemporaryDirectory
from subprocess import run
from re import finditer
from os import path, sep

def init(*, tesseractPath):
	global _tesseractPath
	_tesseractPath = tesseractPath

def scanImage(image, lang='eng', psm=4):
	global _tesseractPath
	logName = 'scanImage'
	log.start(logName)
	log.write(logName, 'start of scan')
	words = []
	bboxes = {'left': [], 'top': [], 'width': [], 'height': []}
	output = None
	with TemporaryDirectory(prefix='robotocr_') as tempPath:
		log.write(logName, 'temp dir created')
		outputPath = path.join(tempPath, 'outputFile')
		log.terminalMessage('Tesseract output target: ' + outputPath)
		imagePath = path.join(tempPath, 'inputFile.bmp')
		image.save(imagePath)
		log.write(logName, 'image saved')
		result = run(_tesseractPath + ' ' + imagePath + ' ' \
		+ outputPath + ' hocr -l ' + lang + ' -psm ' + str(psm))
		log.write(logName, 'processed by tesseract')
		if result.returncode == 0:
			with open(outputPath + '.html', encoding='utf-8') as outputFile:
				output = outputFile.read()
				log.write(logName, 'output read')
				log.start('scanResult')
				log.cleanWrite('scanResult', output)
				log.end('scanResult')
				log.write(logName, 'output logged')
	if output is not None:
		for match in finditer("<span class='ocrx_word' id='[^']+' " \
		+ 'title="bbox (\d+) (\d+) (\d+) (\d+)">(?:<strong>)?([^<]+)(?:</strong>)?</span>', output):
			word = match.group(5)
			if word == ' ':
				continue
			startx = int(match.group(1))
			starty = int(match.group(2))
			endx = int(match.group(3))
			endy = int(match.group(4))
			bboxes['left'].append(startx)
			bboxes['top'].append(starty)
			bboxes['width'].append(endx - startx)
			bboxes['height'].append(endy - starty)
			words.append(word)
	log.write(logName, 'matches interpreted')
	log.end(logName)
	return words, bboxes	