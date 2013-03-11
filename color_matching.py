import cv, math, helper_functions

#number of buckets per color value (so total number of bins is NUM_BUCKETS^3)
NUM_BUCKETS = 8
#any color with all three R,G,B less than 25 is considered "black"
BLACK = 28.0
PIXEL_SKIP = 256/NUM_BUCKETS

def get_bins(im):
	bins = {}
	for i in xrange(NUM_BUCKETS):
		for j in xrange(NUM_BUCKETS):
			for k in xrange(NUM_BUCKETS):
				bins[i,j,k] = 0

	imWidth, imHeight = cv.GetSize(im)
	for i in xrange(imWidth):
		for j in xrange(imHeight):
			value = im[j,i]
			if(value[0] > BLACK or value[1] > BLACK or value[2] > BLACK):
				red = int(value[0])/PIXEL_SKIP
				green = int(value[1])/PIXEL_SKIP
				blue = int(value[2])/PIXEL_SKIP
				bins[red,green,blue] += 1
	sum = 0
	for i in xrange(NUM_BUCKETS):
		for j in xrange(NUM_BUCKETS):
			for k in xrange(NUM_BUCKETS):
				sum += bins[i,j,k]
	return bins

def compare_bins(bins1, bins2):
	sum = 0
	dissimilarity = 0
	for i in xrange(NUM_BUCKETS):
		for j in xrange(NUM_BUCKETS):
			for k in xrange(NUM_BUCKETS):
				firstbin = bins1[i,j,k]
				secondbin = bins2[i,j,k]
				dissimilarity += math.fabs(firstbin - secondbin)
				sum += firstbin+secondbin
	return float(dissimilarity)/sum

def match_colors():
	image_to_bins = {}
	for i in xrange(1,41):
		im = cv.LoadImageM(helper_functions.image_path(i))
		bins = get_bins(im)
		image_to_bins[i] = bins
	
	for i in xrange(1,41):
		closest_image = 0
		furthest_image = 0
		closest_match = 1
		furthest_match = 0
		for j in xrange(1,41):
			if(i != j):
				similarity = compare_bins(image_to_bins[i], image_to_bins[j])
				if(closest_match > similarity):
					closest_match = similarity
					closest_image = j
				if(furthest_match < similarity):
					furthest_match = similarity
					furthest_image = j
		print i, closest_image, furthest_image