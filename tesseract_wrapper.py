
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

def scanImage(image, lang='eng'):
	global _tesseractPath
	words = []
	bboxes = {'left': [], 'top': [], 'width': [], 'height': []}
	output = None
	with TemporaryDirectory(prefix='robotocr_') as tempPath:
		outputPath = path.join(tempPath, 'outputFile')
		log.terminalMessage('Tesseract output target: ' + outputPath)
		imagePath = path.join(tempPath, 'inputFile.bmp')
		image.save(imagePath)
		result = run(_tesseractPath + ' ' + imagePath + ' ' \
		+ outputPath + ' hocr')
		if result.returncode == 0:
			with open(outputPath + '.html', encoding='utf-8') as outputFile:
				output = outputFile.read()
				log.start('scanResult')
				log.cleanWrite('scanResult', output)
				log.end('scanResult')
	if output is not None:
		for match in finditer("<span class='ocrx_word' id='[^']+' " \
		+ 'title="bbox (\d+) (\d+) (\d+) (\d+)">([^<]+)</span>', output):
			word = match.group(5)
			if word == ' ':
				continue
			bboxes['left'].append(int(match.group(1)))
			bboxes['top'].append(int(match.group(2)))
			bboxes['width'].append(int(match.group(3)))
			bboxes['height'].append(int(match.group(4)))
			words.append(word)
	return words, bboxes	