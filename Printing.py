import cv, Image, ImageDraw, ImageFont, helper_functions, color_matching, texture_matching

def printOutputs(outputs):
	
	#initialize
	canvas = Image.new("RGB", (330,3350), (255,255,255))
	step = 80
	row = 1
	font = ImageFont.truetype("Arial.ttf",10)
	draw = ImageDraw.Draw(canvas)
	
	#print header
	headerFont = ImageFont.truetype("Arial.ttf",15)
	draw.text((20,30),"Image",font=headerFont, fill=(0,0,0))
	draw.text((120,30),"Best Match",font=headerFont, fill=(0,0,0))
	draw.text((220,30),"Worst Match",font=headerFont, fill=(0,0,0))
	
	#print images
	for output in outputs:
		imageNum = output[0]
		bestImageNum = output[1]
		worstImageNum = output[2]
		image = Image.open(helper_functions.image_path(imageNum))
		bestImage = Image.open(helper_functions.image_path(bestImageNum))
		worstImage = Image.open(helper_functions.image_path(worstImageNum))
		canvas.paste(image,(10,row*step,99,row*step+60))
		canvas.paste(bestImage,(110,row*step,199,row*step+60))
		canvas.paste(worstImage,(210,row*step,299,row*step+60))
		draw.text((20,row*step+63),"Image: " + str(imageNum),font=font, fill=(0,0,0))
		draw.text((120,row*step+63),"Image: " + str(bestImageNum),font=font, fill=(0,0,0))
		draw.text((220,row*step+63),"Image: " + str(worstImageNum),font=font, fill=(0,0,0))
		row += 1
	canvas.save("Part3Output.jpg", "JPEG")

def getImageWithSmallestAverageDistance(image_to_bins_colors, image_to_bins_texture):
	smallestSum = 10000000000000
	bestImage = 0
	for i in xrange(1,41):
		sum = 0
		for j in xrange(1,41):
			if i != j:
				colorSimilarity = color_matching.compare_bins(image_to_bins_colors[i],image_to_bins_colors[j])
				textureSimilarity = texture_matching.compare_bins(image_to_bins_texture[i], image_to_bins_texture[j])
				similarity = helper_functions.getSimilarity(colorSimilarity,textureSimilarity)
				sum += similarity
		if smallestSum > sum:
			smallestSum = sum
			bestImage = i
	return bestImage

def printAxesGraph(relativeBestImage, image_to_bins_colors, image_to_bins_texture):
	#initialize
	CANVAS_WIDTH = 1200
	canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_WIDTH), (255,255,255))
	imageNum = relativeBestImage
	image = Image.open(helper_functions.image_path(imageNum))
	canvas.paste(image, (0,0,89,60))
	
	for i in xrange(1,41):
		if i != imageNum:
			colorSimilarity = color_matching.compare_bins(image_to_bins_colors[i],image_to_bins_colors[imageNum])
			textureSimilarity = texture_matching.compare_bins(image_to_bins_texture[i], image_to_bins_texture[imageNum])
			xCoord = int(colorSimilarity*CANVAS_WIDTH)
			yCoord = int(textureSimilarity*CANVAS_WIDTH)
			comparedImage = Image.open(helper_functions.image_path(i))
			canvas.paste(comparedImage, (xCoord,yCoord,89+xCoord,60+yCoord))	
	canvas.save("Part4Output.jpg", "JPEG")

def printOnAxes(image_to_bins_colors, image_to_bins_texture):
	relativeBestImage = getImageWithSmallestAverageDistance(image_to_bins_colors, image_to_bins_texture)
	printAxesGraph(relativeBestImage, image_to_bins_colors, image_to_bins_texture)
	
	