
#local imports
from . import log
from . import screen
from . import search
from . import tesseract_wrapper

#standard library imports
import time

def init(*, tesseractPath, logFolderPath):
	tesseract_wrapper.init(tesseractPath = tesseractPath)
	log.init(logFolderPath=logFolderPath)

def lookForSentence(sentence,*, lang='eng', psm=3, cut=(), \
processing=(), ratio=0.8, skip=0):
	log.terminalMessage('Looking for Sentence')
	logName = 'lookFor-' + sentence
	log.start(logName)
	log.write(logName, 'Looking for Sentence: ' + sentence)
	image = screen.prepareImage(cut=cut, processing=processing)
	log.write(logName, 'screeshot processed')
	words, bboxes = tesseract_wrapper.scanImage(image, lang=lang, psm=psm)
	log.write(logName, 'ocr response recieved')
	image = []
	found, startWord, endWord, matchedSentence =\
	search.searchWordList(sentence, ratio, words, skip=skip)
	if found:
		log.terminalMessage('Sentence found')
		log.write(logName, 'Sentence found: ' + matchedSentence)
		log.end(logName)
	else:
		log.terminalMessage('Sentence not found')
		log.write(logName, 'Sentence not found')
		log.end(logName)
	return (found, bboxes, startWord, endWord)

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
		found, bboxes, startWord, endWord \
		= lookForSentence(sentence, **kwargs)
		if found:
			left = min(bboxes['left'][startWord:endWord+1])
			top = min(bboxes['top'][startWord:endWord+1])
			width = max(bboxes['left'][startWord:endWord+1])\
			- left + max(bboxes['width'][startWord:endWord+1])
			height = max(bboxes['top'][startWord:endWord+1])\
			- top + max(bboxes['height'][startWord:endWord+1])
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
