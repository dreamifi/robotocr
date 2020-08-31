# Third party imports
import pyautogui
import numpy
from PIL import Image
import skimage

# Local application imports
from . import log

def prepareImage(*, cut=(), processing=()):
	region = calculateCut(cut=cut)
	image = pyautogui.screenshot(region=region)
	log.saveImage(image, 'raw')
	if not processing:
		return image
	logName = 'processing'
	log.start(logName)
	log.write(logName, 'processing starting')
	image = numpy.asarray(image)
	log.write(logName, 'asarray')
	for processor in processing:
		if hasattr(processor, 'condition'):
			if not processor.condition():
				log.write(logName, processor.name() + ' skipped')
				continue
		image = processor.process(image)
		log.write(logName, processor.name())
		log.saveNumpyImage(image, processor.name())
	image = Image.fromarray(skimage.img_as_ubyte(image))
	log.write(logName, 'fromArray')
	log.end(logName)
	return image
	
def calculateCut(*, cut=()):
	width, height = pyautogui.size()
	region = (0,0, width, height)
	for section in cut:
		region = section(*region)
	return region
	
def calculateScale(*, processing=()):
	verticalScale = 1
	horizontalScale = 1
	for processor in processing:
		if hasattr(processor, 'scaleEffect'):
			verticalChange, horizontalChange = processor.scaleEffect()
			horizontalScale = horizontalScale * horizontalChange
			verticalScale = verticalScale * verticalChange
	return verticalScale, horizontalScale
	
def click(x, y, *, cut=(), processing=()):
	left, top = calculateCut(cut=cut)[:2]
	verticalScale, horizontalScale = calculateScale(processing=processing)
	x = left + (x/horizontalScale)
	y = top + (y/verticalScale)
	pyautogui.click(x=x, y=y)
	return (x, y)
	
def doubleClick(x, y, *, cut=(), processing=()):
	left, top = calculateCut(cut=cut)[:2]
	verticalScale, horizontalScale = calculateScale(processing=processing)
	x = left + (x/horizontalScale)
	y = top + (y/verticalScale)
	pyautogui.doubleClick(x=x, y=y)
	return (x, y)