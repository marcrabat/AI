class FileDealer():
	
	with open("stopwords.txt", "r") as sw:
		stopwords = sw.read().splitlines()

	def __init__(self, dataset_dir, file_name):
		self.file_name = file_name
		self.file_descriptor = dataset_dir + file_name
		self.current_words = []

	def print_file(self):
		print("Showing content of:" + self.file_name)
		with open(self.file_descriptor, "r") as fd:
			print(fd.read())

	