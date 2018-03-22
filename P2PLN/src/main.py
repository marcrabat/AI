import os
from utils import FileDealer


class Main():
	
	dataset_dir = "dataset/"
	#Initializing the list of instances
	files = []
	for file_name in os.listdir(dataset_dir):
		files.append(FileDealer(str(dataset_dir),str(file_name)))

	print(files[0].stopwords)

	
