import os

class FilesDealer():
	def __init__(self, dataset_dir, num_freq_words):
		self.dataset_dir  = dataset_dir
		self.files = []
		self.N = num_freq_words

	def initialize_files(self):
		for file_name in os.listdir(self.dataset_dir):
			self.files.append(FileInstance(self.dataset_dir,str(file_name),self.N))

	def print_files(self):
		for file in self.files:
			print(file.text)

	def print_file(self):
		print("Content of file: ", self.files[0].file_name)
		print(self.files[0].text)

class FileInstance():
	
	with open("stopwords.txt", "r") as sw:
		stopwords = sw.read().splitlines()
	sw.close()

	def __init__(self, dataset_dir, file_name, N_freq):
		self.file_name = file_name
		self.file_descriptor = dataset_dir + file_name
		self.text = []
		with open(self.file_descriptor) as fd:
			self.text = fd.read().split()
		fd.close()
		self.N = N_freq
		self.number_of_words = 0
		self.frequent_words = []

	