import cv, math, helper_functions

BLACK_VALUE = 17.0
MAX_PIXEL_VALUE = 2040 #8*255
NUM_BINS = 28
PIXEL_STEP = MAX_PIXEL_VALUE/(NUM_BINS-1)

def grayscale_image(im):
	imWidth, imHeight = cv.GetSize(im)
	grayIm = cv.CreateMat(imHeight,imWidth, cv.CV_32FC1)
	for j in xrange(imWidth):
		for k in xrange(imHeight):
			red = im[k,j][0]
			green = im[k,j][1]
			blue = im[k,j][2]
			grayIm[k,j] = int(red+green+blue)/3
	return grayIm

def get_bins(im):
	bins = {}
	imWidth, imHeight = cv.GetSize(im)
	for i in xrange(NUM_BINS):
		bins[i] = 0
	for j in xrange(1,imWidth-1):
		for k in xrange(1,imHeight-1):
			value = 8*im[k,j]-im[k-1,j]-im[k+1,j]-im[k,j-1]-im[k,j+1]-im[k+1,j-1]-im[k+1,j+1]-im[k-1,j+1]-im[k-1,j-1]
			if value > 30 or im[k,j] > BLACK_VALUE: #removes black background from texture consideration
				bins[int(math.fabs(value / PIXEL_STEP))] += 1
	return bins

def compare_bins(hist1,hist2):
	sum = 0
	dissimilarity = 0
	for i in xrange(NUM_BINS):
		dissimilarity += math.fabs(hist1[i]-hist2[i])
		sum += hist1[i]+hist2[i]
	return float(dissimilarity)/sum
