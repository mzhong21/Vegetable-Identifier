import cv
import buckets

def image_path(num):
	path = "./images/i"
	if(num < 10):
		path = path + "0" + str(num) + ".jpg"
	else:
		path = path + str(num) + ".jpg"
	return path

def main():
	image_to_bins = {}
	for i in xrange(1,41):
		im = cv.LoadImageM(image_path(i))
		bins = buckets.get_bins(im)
		image_to_bins[i] = bins
	
	for i in xrange(1,41):
		closest_image = 0
		furthest_image = 0
		closest_match = 1
		furthest_match = 0
		for j in xrange(1,41):
			if(i != j):
				similarity = buckets.compare_bins(image_to_bins[i], image_to_bins[j])
				if(closest_match > similarity):
					closest_match = similarity
					closest_image = j
				if(furthest_match < similarity):
					furthest_match = similarity
					furthest_image = j
		print i, closest_image, furthest_image
				

if __name__ == '__main__':
	main()