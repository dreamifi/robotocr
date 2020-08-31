# third party imports
import pyautogui
import numpy
import skimage
from skimage import color
from skimage import transform
from skimage import filters
from skimage import morphology

#local imports
import robotocr.log as log

class RgbToGray:
	def process(self, image):
		return color.rgb2gray(image)
	def name(self):
		return 'RgbToGray'
		
class Rescale:
	def __init__(self, scale):
		self.scale= scale
	def process(self, image):
		return transform.rescale(image, self.scale)
	def scaleEffect(self):
		return (self.scale, self.scale)
	def name(self):
		return 'Rescale'
		
class RescaleIfBelow:
	def __init__(self, targetHeight):
		width, height = pyautogui.size()
		scale = 1
		while(height * scale < targetHeight):
			scale = scale + 1
		self.scale= scale
	def process(self, image):
		return transform.rescale(image, self.scale)
	def condition(self):
		return not self.scale == 1
	def scaleEffect(self):
		return (self.scale, self.scale)
	def name(self):
		return 'RescaleIfBelow'
		
class WidenTo16by10:
	def __init__(self):
		width, height = pyautogui.size()
		self.screenIsThin = width / height < 1.6
		self.scale= 1.6 / (width / height)
	def process(self, image):
		return transform.rescale(image, (1, self.scale))
	def condition(self):
		return self.screenIsThin
	def scaleEffect(self):
		return (1, self.scale)
	def name(self):
		return 'WidenTo16by10'
		
class Floor:
	def __init__(self, threshold=0.5):
		self.threshold= threshold
	def process(self, image):
		return image * (image > self.threshold)
	def name(self):
		return 'Floor'
		
class MaxFloor:
	def __init__(self, range=0.05):
		self.range= range
	def process(self, image):
		return image * ((image + self.range) >= numpy.amax(image))
	def name(self):
		return 'MaxFloor'
		
class LocalMaxFloor:
	def __init__(self, range=0.2, squareSize=20):
		self.range= range
		self.squareSize= squareSize
	def process(self, image):
		processor = LocalMax(self.squareSize)
		localMax = skimage.img_as_float(processor.process(image))
		log.saveNumpyImage(localMax, processor.name())
		return image * ((image + self.range) >= localMax)
	def name(self):
		return 'LocalMaxFloor'
		
class LocalMax:
	def __init__(self, squareSize=20):
		self.squareSize= squareSize
	def process(self, image):
		square = morphology.square(self.squareSize)
		localMax = filters.rank.maximum(image, square)
		return localMax
	def name(self):
		return 'LocalMax'
		
class AutoLevel:
	def __init__(self, squareSize=5):
		self.squareSize= squareSize
	def process(self, image):
		return filters.rank.autolevel(image, morphology.square(self.squareSize))
	def name(self):
		return 'AutoLevel'
		
class Thin:
	def __init__(self, iterations=1):
		self.iterations= iterations
	def process(self, image):
		return morphology.thin(image, max_iter=self.iterations)
	def name(self):
		return 'Thin'