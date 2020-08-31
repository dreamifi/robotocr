
#third party imports
import numpy

#local imports
from . import log

def searchWordList(term, targetRatio, wordList,*, skip=0):
	perfectingMatch = False
	skippingMatch = False
	logName = 'search-' + term
	log.start(logName)
	matrixHeight = len(term)
	targetDistance = (1 - targetRatio) * matrixHeight
	distanceMatrix = [numpy.arange(1, matrixHeight + 1, 1)]
	horizontalIndex = 0
	for listindex in range(len(wordList)):
		word = ' ' + wordList[listindex]
		for localCharIndex in range(len(word)):
			horizontalIndex = horizontalIndex + 1
			distanceMatrix.append(numpy.zeros(matrixHeight))
			candidateChar = word[localCharIndex]
			if(term[0] != candidateChar):
				distanceMatrix[horizontalIndex][0] = 1
			for verticalIndex in range(1, matrixHeight):
				if(term[verticalIndex] == candidateChar):
					distanceMatrix[horizontalIndex][verticalIndex] = \
					distanceMatrix[horizontalIndex -1][verticalIndex -1]
				else:
					substituteCost = \
					distanceMatrix[horizontalIndex -1][verticalIndex -1] + 1
					deleteCost = \
					distanceMatrix[horizontalIndex][verticalIndex -1] + 1
					if(candidateChar.isspace()):
						insertCost = distanceMatrix\
						[horizontalIndex -1][verticalIndex] + 0.3
					else:
						insertCost = distanceMatrix\
						[horizontalIndex -1][verticalIndex] + 1
					distanceMatrix[horizontalIndex][verticalIndex] \
					= min(substituteCost, deleteCost, insertCost)
			arrayAsString = \
			numpy.array2string(distanceMatrix[horizontalIndex], \
			precision = 1, suppress_small=True, floatmode='fixed')
			log.cleanWrite(logName, candidateChar + '  ' + arrayAsString)
			if skippingMatch:
				if distanceMatrix[horizontalIndex][matrixHeight - 1] \
				> targetDistance:
					skippingMatch = False
			elif perfectingMatch:
				if distanceMatrix[horizontalIndex][matrixHeight - 1] >\
				distanceMatrix[horizontalIndex-1][matrixHeight - 1]:
					listindex, localCharIndex = \
					goBackOne(listindex, localCharIndex -1, wordList)
					distanceMatrix = distanceMatrix[:len(distanceMatrix) -1]
					return finishingTouches(listindex, localCharIndex,\
					wordList, distanceMatrix, logName)
			elif(distanceMatrix[horizontalIndex][matrixHeight - 1] \
			<= targetDistance):
				if skip > 0:
					log.write(logName, 'Skipping Match')
					skippingMatch = True
					skip = skip - 1
				else:
					log.write(logName, 'Perfecting Match')
					perfectingMatch = True
	if perfectingMatch:
		finalIndex = len(wordList) -1
		word = wordList[finalIndex]
		finalCharIndex = len(word) -1
		return finishingTouches(finalIndex, finalCharIndex, wordList,\
		distanceMatrix, logName)
	log.write(logName, 'No Match!')
	log.end(logName)
	return (False, False, False, False)
	
def finishingTouches(listindex, localCharIndex, wordList,\
 distanceMatrix, logName):
	firstWord, lastWord, matchedSentence =\
	pickOutSentence(wordList, listindex, localCharIndex, distanceMatrix)
	log.write(logName, 'Match Found: ' + matchedSentence)
	log.end(logName)
	return (True, firstWord, lastWord, matchedSentence)
	
def goBackOne(listindex, localCharIndex, wordList):
	if localCharIndex <= 0:
		listindex = listindex -1
		word = wordList[listindex]
		localCharIndex = len(word) -1
		return (listindex, localCharIndex)
	else:
		return (listindex, localCharIndex - 1)
	
def pickOutSentence(wordList, lastWord, lastLetter, distanceMatrix):
	length = matchedSentenceLength(distanceMatrix)
	if length -1 <= lastLetter:
		firstWord = lastWord
		firstLetter = lastLetter -length +1
		matchedSentence = wordList[lastWord][firstLetter:lastLetter+1]
		return (firstWord, lastWord, matchedSentence)
	else:
		remainingLength = length -lastLetter -2
		matchedSentence = ' ' + wordList[lastWord][:lastLetter+1]
		for wordIndex in range(lastWord -1, -1, -1):
			wordLength = len(wordList[wordIndex])
			if remainingLength <= wordLength:
				firstWord = wordIndex
				firstLetter = wordLength - remainingLength
				matchedSentence = \
				wordList[firstWord][firstLetter:]\
				+ matchedSentence
				return (firstWord, lastWord, matchedSentence)
			else:
				remainingLength = remainingLength -wordLength -1
				matchedSentence = ' ' + wordList[wordIndex] \
				+ matchedSentence
				
def matchedSentenceLength(distanceMatrix):
	length = 0
	verticalIndex = len(distanceMatrix[0]) -1
	for horizontalIndex in range(len(distanceMatrix) -1, -1, -1):
		length = length + 1
		while True:
			if(verticalIndex == 0):
				return length
			diagonal = distanceMatrix[horizontalIndex -1][verticalIndex -1]
			above = distanceMatrix[horizontalIndex][verticalIndex -1]
			left = distanceMatrix[horizontalIndex -1][verticalIndex]
			lowestPreceding = min(diagonal, above, left)
			if diagonal == lowestPreceding:
				verticalIndex = verticalIndex - 1
				break
			elif above == lowestPreceding:
				verticalIndex = verticalIndex - 1
			else:
				break
