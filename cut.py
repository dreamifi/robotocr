
def left(left, top, width, height):
	return (left, top, width/3, height)
	
def top(left, top, width, height):
	return (left, top, width, height/3)
	
def wideMiddle(left, top, width, height):
	return (left, top + height/3, width, height/3)
	
def tallMiddle(left, top, width, height):
	return (left + width/3, top, width/3, height)
	
def right(left, top, width, height):
	return (left + 2*width/3, top, width/3, height)
	
def bottom(left, top, width, height):
	return (left, top + 2*height/3, width, height/3)
	
def leftHalf(left, top, width, height):
	return (left, top, width/2, height)
	
def topHalf(left, top, width, height):
	return (left, top, width, height/2)
	
def wideMiddleHalf(left, top, width, height):
	return (left, top + height/4, width, height/2)
	
def tallMiddleHalf(left, top, width, height):
	return (left + width/4, top, width/2, height)
	
def rightHalf(left, top, width, height):
	return (left + 3*width/4, top, width/2, height)
	
def bottomHalf(left, top, width, height):
	return (left, top + 3*height/4, width, height/2)