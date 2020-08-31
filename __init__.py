
#local imports
from . import log
from . import screen
from . import search

#third party imports
import pytesseract
from pytesseract import Output

#standard library imports
import time

def init(*, tesseractPath, logFolderPath):
	pytesseract.pytesseract.tesseract_cmd = \
	tesseractPath
	log.init(logFolderPath=logFolderPath)

def lookForSentence(sentence,*, lang='eng', cut=(), \
processing=(), config='--psm 4', ratio=0.8, skip=0):
	log.terminalMessage('Looking for Sentence')
	logName = 'lookFor-' + sentence
	log.start(logName)
	log.write(logName, 'Looking for Sentence: ' + sentence)
	image = screen.prepareImage(cut=cut, processing=processing)
	log.write(logName, 'screeshot processed')
	scanResult = pytesseract.image_to_data(image, lang=lang, \
	output_type=Output.DICT, config=config)
	log.write(logName, 'ocr response recieved')
	log.start('scanResult')
	log.cleanWrite('scanResult', str(scanResult))
	log.end('scanResult')
	image = []
	found, firstWord, lastWord, matchedSentence =\
	search.searchWordList(sentence, ratio, scanResult['text'], skip=skip)
	if found:
		log.terminalMessage('Sentence found')
		log.write(logName, 'Sentence found: ' + matchedSentence)
		log.end(logName)
	else:
		log.terminalMessage('Sentence not found')
		log.write(logName, 'Sentence not found')
		log.end(logName)
	return (found, scanResult, firstWord, lastWord)

def sentenceExists(sentence, **kwargs):
	return lookForSentence(sentence, **kwargs)[0]
	
def waitSentence(sentence, **kwargs):
	found = False
	while True:
		found = sentenceExists(sentence, **kwargs)
		if found:
			break
		time.sleep(0.2)	
		
def locateSentence(sentence, **kwargs):
	while True:
		found, scanResult, firstWord, lastWord =\
		lookForSentence(sentence, **kwargs)
		if found:
			left = min(scanResult['left'][firstWord:lastWord+1])
			top = min(scanResult['top'][firstWord:lastWord+1])
			width = max(scanResult['left'][firstWord:lastWord+1])\
			- left + max(scanResult['width'][firstWord:lastWord+1])
			height = max(scanResult['top'][firstWord:lastWord+1])\
			- top + max(scanResult['height'][firstWord:lastWord+1])
			return (left, top, width, height)
		time.sleep(0.2)	

def clickSentence(sentence,*, cut=(), processing=(), **kwargs):
	left, top, width, height =\
	locateSentence(sentence, cut=cut, processing=processing, **kwargs)
	middle = (left + width/2, top + height/2)
	return screen.click(*middle, cut=cut, processing=processing)
	
def doubleClickSentence(sentence,*, cut=(), processing=(), **kwargs):
	left, top, width, height =\
	locateSentence(sentence, cut=cut, processing=processing, **kwargs)
	middle = (left + width/2, top + height/2)
	return screen.doubleClick(*middle, cut=cut, processing=processing)
