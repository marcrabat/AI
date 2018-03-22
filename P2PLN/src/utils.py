import os
from string import punctuation
import re

class FeatureExtractor():
	def __init__(self, dataset_dir, num_freq_words):
		self.dataset_dir  = dataset_dir
		self.files = []
		self.N = num_freq_words
		self.initialize_files()

	def initialize_files(self):
		for file_name in os.listdir(self.dataset_dir):
			self.files.append(FileInstance(self.dataset_dir,str(file_name),self.N))

	def parse_files(self):
		for file in self.files:
			file.parse()
			file.remove_stopwords()


class FileInstance():
	#shared variables among all the file instances
	with open("stopwords.txt", "r") as sw:
		stopwords = sw.read().splitlines()
	sw.close()
	to_remove = punctuation + "—"
	to_remove = to_remove.replace("@","")
	punct = str.maketrans('','', to_remove) #create translation in order to use with translate, this erase the unnecessary symbols

	#instance variables
	def __init__(self, dataset_dir, file_name, N_freq):
		self.file_name = file_name
		self.file_descriptor = dataset_dir + file_name
		self.input_text = []
		
		with open(self.file_descriptor) as fd:
			self.input_text = fd.read().split()
		fd.close()
		
		self.N = N_freq
		self.number_of_words = 0
		self.parsed_text = []
		self.features = []

	def parse(self): #erase the punctuation symbols and after deleting first "-" or any conflictive char
		print("File: ", self.file_name)
		print(self.input_text)
		for word in self.input_text:
			if len(re.findall(r"[\w'(?:'+)*]+", word)) > 1: #do not eliminate commas like in that's
				compound = re.findall(r"[\w'(?:,+)*]+", word)
				for item in compound:
					self.parsed_text.append(item.translate(self.punct))
			else:
				self.parsed_text.append(word.translate(self.punct))
		while '' in self.parsed_text:
			self.parsed_text.remove('')
		#print(self.parsed_text)
		#update the number of legal words in the text
		self.number_of_words = len(self.parsed_text)
		#print(self.number_of_words)
		del self.input_text[:] #after the input is analyzed, it is not needed anymore
	
	def remove_stopwords(self):
		self.parsed_text = (list(set(self.parsed_text) - set(self.stopwords))) #parsed list difference stopwords
		#print(self.parsed_text)
		#print(len(self.parsed_text))
		

