import os
from string import punctuation
from collections import Counter
import re

class FeatureExtractor():
	def __init__(self, dataset_dir, num_freq_words):
		self.dataset_dir  = dataset_dir
		self.files = []
		self.N = num_freq_words
		self.initialize_files()
		self.parse_files()

	def initialize_files(self):
		for file_name in os.listdir(self.dataset_dir):
			self.files.append(FileInstance(self.dataset_dir,str(file_name),self.N))

	def parse_files(self):
		for file in self.files:
			file.parse()
			file.remove_stopwords()
		#self.files[0].parse()
		#self.files[0].remove_stopwords()
	def compute_features(self):
		for file in self.files:
		#self.files[0].compute_vector()
			file.compute_vector()
			print(file.file_name)
			print(file.features)
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
		#print("File: ", self.file_name)
		#print(len(self.input_text))
		#print(self.input_text)

		for word in self.input_text:
			if len(re.findall(r"[\w,(?:,+)*]+", word)) > 1: #do not eliminate commas like in that's
				compound = re.findall(r"[\w,(?:,+)*]+", word)
				for item in compound:
					self.parsed_text.append(item.translate(self.punct))
			else:
				self.parsed_text.append(word.translate(self.punct))
		while '' in self.parsed_text:
			self.parsed_text.remove('')
		#update the number of legal words in the text before eliminate stopwords
		self.number_of_words = len(self.parsed_text)
		#print(self.number_of_words)
		#print(self.parsed_text)
		del self.input_text[:] #after the input is analyzed, it is not needed anymore
	
	def remove_stopwords(self):
		newlist = []
		for word in self.parsed_text:
			if word.lower() not in self.stopwords:
				newlist.append(word)
		self.parsed_text = newlist
		#print(self.parsed_text) ##############amb aquest print es veu be com queden les paraules despres de parsejar-lo!
		#print(len(self.parsed_text))

	def compute_vector(self):
		counter = Counter(self.parsed_text).most_common(self.N)
		for item in counter:
			value = 0.0
			#word = (item[0]).lower ##canvio a minus
			frequency = item[1]
			value = (frequency / self.number_of_words)*100 #sobre 100? sobre 1?
			dim = str(value) + " " + item[0]
			#print(dim)
			#dim = str(repr(value) + " " + word)
			self.features.append(dim)
