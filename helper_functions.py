import cv, color_matching, texture_matching, Printing

def image_path(num):
	path = "./images/i"
	if(num < 10):
		path = path + "0" + str(num) + ".jpg"
	else:
		path = path + str(num) + ".jpg"
	return path
	
def getSimilarity(colorSimilarity, textureSimilarity):
	magic_r = .25
	return magic_r*textureSimilarity+(1-magic_r)*colorSimilarity

def findMatches(image_to_bins_colors, image_to_bins_texture):
	outputs = []
	for i in xrange(1,41):
		bestImage = 0
		worstImage = 0
		closestMatch = 1
		worstMatch = 0
		for j in xrange(1,41):
			if i != j:
				colorSimilarity = color_matching.compare_bins(image_to_bins_colors[i],image_to_bins_colors[j])
				textureSimilarity = texture_matching.compare_bins(image_to_bins_texture[i], image_to_bins_texture[j])
				similarity = getSimilarity(colorSimilarity,textureSimilarity)
				if closestMatch > similarity:
					bestImage = j
					closestMatch = similarity
				if worstMatch < similarity:
					worstImage = j
					worstMatch = similarity
		outputs.append([i,bestImage,worstImage])
	Printing.printOutputs(outputs)

def generatePairMappings(image_to_bins_colors, image_to_bins_texture):
	mapping = {}
	for i in xrange(1,41):
		for j in xrange(1,41):
			if i!= j:
				colorSimilarity = color_matching.compare_bins(image_to_bins_colors[i],image_to_bins_colors[j])
				textureSimilarity = texture_matching.compare_bins(image_to_bins_texture[i], image_to_bins_texture[j])
				similarity = getSimilarity(colorSimilarity,textureSimilarity)
				mapping[i,j] = similarity
	return mapping

def generateDendrogram(image_to_bins_colors, image_to_bins_texture):
	fp = open('Single Link Dendrogram.txt', 'w')
	clusters = []
	mapping = generatePairMappings(image_to_bins_colors, image_to_bins_texture)
	for imageNum in xrange(1,41):
		clusters.append([imageNum])
	fp.write(str(clusters) + "\n")
	while len(clusters) > 1:
		nearestScore = 1
		bestCluster1 = []
		bestCluster2 = []		
		for cluster1 in clusters:
			for cluster2 in clusters:
				if cluster1 != cluster2:
					worstScore = 1
					for i in cluster1:
						for j in cluster2:
							if mapping[i,j] < worstScore:
								worstScore = mapping[i,j]
					if worstScore < nearestScore:
						nearestScore = worstScore
						bestCluster1 = cluster1
						bestCluster2 = cluster2
		indexPop = clusters.index(bestCluster2)
		indexPush = clusters.index(bestCluster1)
		clusters[indexPush] += clusters.pop(indexPop)
		fp.write(str(clusters) + "\n")
	fp.close()			
			

def go_through_images():
	image_to_bins_colors = {}
	image_to_bins_texture = {}
	for i in xrange(1,41):
		im = cv.LoadImageM(image_path(i))
		image_to_bins_colors[i] = color_matching.get_bins(im)
		image_to_bins_texture[i] = texture_matching.get_bins(texture_matching.grayscale_image(im))
	
	#findMatches(image_to_bins_colors, image_to_bins_texture) #Step 1 / Step 2
	#generateDendrogram(image_to_bins_colors, image_to_bins_texture) # Step 3
	Printing.printOnAxes(image_to_bins_colors, image_to_bins_texture) #Step 4
	
	