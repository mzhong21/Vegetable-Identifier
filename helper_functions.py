import cv, color_matching, texture_matching

def image_path(num):
	path = "./images/i"
	if(num < 10):
		path = path + "0" + str(num) + ".jpg"
	else:
		path = path + str(num) + ".jpg"
	return path

def findMatches(image_to_bins_colors, image_to_bins_texture):
	for i in xrange(1,41):
		bestImage = 0
		worstImage = 0
		closestMatch = 1
		worstMatch = 0
		for j in xrange(1,41):
			if i != j:
				colorSimilarity = color_matching.compare_bins(image_to_bins_colors[i],image_to_bins_colors[j])
				textureSimilarity = texture_matching.compare_bins(image_to_bins_texture[i], image_to_bins_texture[j])
				similarity = colorSimilarity
				if closestMatch > similarity:
					bestImage = j
					closestMatch = similarity
				if worstMatch < similarity:
					worstImage = j
					worstMatch = similarity
		print i, bestImage, worstImage

def go_through_images():
	image_to_bins_colors = {}
	image_to_bins_texture = {}
	for i in xrange(1,41):
		im = cv.LoadImageM(image_path(i))
		image_to_bins_colors[i] = color_matching.get_bins(im)
		image_to_bins_texture[i] = texture_matching.get_bins(texture_matching.grayscale_image(im))
	
	findMatches(image_to_bins_colors, image_to_bins_texture)
	
	
	