import nude
from nude import Nude
import glob
import itertools

# Example of usage
# n = Nude('./images/filename.extension')
# n.parse()
# print(n.result, n.inspect())

#n = Nude('./images/p1.jpg')
#n.parse()

#images format 
images_format = ['jpg', 'png', 'gif', 'tiff']

#getting list of images in folder images in different format
images_jpg = glob.glob("./images/*.jpg")
images_png = glob.glob("./images/*.png")
images_gif = glob.glob("./images/*.gif")
images_tiff = glob.glob("./images/*.tiff")

images_list = itertools.chain(images_jpg, images_png, images_gif, images_tiff)

#loop for checking images nude or not
#for index in range(len(images_list)):
#	n = Nude( images_list[index] )
for i in images_list:
	print i
	n = Nude(i)
	n.parse()
	print(n.result, n.inspect())

