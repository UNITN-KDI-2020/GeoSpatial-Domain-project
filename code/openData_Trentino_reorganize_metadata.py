import os
from shutil import copyfile

SOURCE_FOLDER = "./dataset/Data Integration/data/luoghi e punti di interesse per comune/"
DEST_FOLDER = "./dataset/Data Integration/metadata/luoghi e punti di interesse per comune METADATA/"

if not os.path.exists(DEST_FOLDER): os.mkdir(DEST_FOLDER)

for count, filename in enumerate(os.listdir(SOURCE_FOLDER)):
	# print(filename)
	if "CLASSES" in filename:
		copyfile(SOURCE_FOLDER+filename, DEST_FOLDER+filename)
		os.remove(SOURCE_FOLDER+filename)


