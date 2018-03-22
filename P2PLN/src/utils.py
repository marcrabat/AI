import os
from string import punctuation
from collections import Counter
from collections import OrderedDict
import re

class Classifier():
	def __init__(self, dataset_dir, num_freq_words):
		self.dataset_dir  = dataset_dir
		self.files = []
		self.N = num_freq_words
		self.most_frequent = []
		self.initialize_files()
		self.parse_files()
		self.num_words_corpus = 0

	def initialize_files(self):
		for file_name in os.listdir(self.dataset_dir):
			self.files.append(FileInstance(self.dataset_dir,str(file_name),self.N))

	def parse_files(self):
		for file in self.files:
			file.parse()
			file.remove_stopwords()
		#self.files[0].parse()
		#self.files[0].remove_stopwords()
	def most_frequent_words(self):
		for file in self.files:
			for word in file.parsed_text:
				self.num_words_corpus += 1
				self.most_frequent.append(word)
		self.most_frequent = Counter(self.most_frequent).most_common(self.N)
		aux = []
		for item in self.most_frequent:
			aux.append(item[0].lower())
		self.most_frequent = aux
		#print(self.most_frequent)
		#print(self.num_words_corpus)

	def compute_features(self):
		for file in self.files:
		#self.files[0].compute_vector()
			#print(self.most_frequent)
			print(file.file_name)
			file.compute_vector(self.most_frequent)

			#print(file.gender)
			#print(file.features)

	def generate_arff(self):
		with open("results.arff", "w") as results:
			results.write("%1. Title: Results of Features")
			results.write("\n%2. Sources:")
			results.write("\n%\tAuthors: Ferran Cantarino i Marc Rabat")
			results.write("\n@RELATION " + str(self.N) + " Features")
			for item in self.most_frequent:
				results.write("\n@ATTRIBUTE " + str(item) + " NUMERIC")
			results.write("\n@ATTRIBUTE class {male, female}")

		results.close()




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
		self.gender = re.sub('^[^A-Za-z]*', '', self.file_name)
		self.file_descriptor = dataset_dir + file_name
		self.input_text = []
		
		with open(self.file_descriptor) as fd:
			self.input_text = fd.read().split()
		fd.close()
		
		self.N = N_freq
		self.number_of_words = 0
		self.parsed_text = []
		self.features = OrderedDict()
		#self.features = OrderedDict()

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

	def compute_vector(self, most_frequent):
		#print(most_frequent)
		counter = Counter(self.parsed_text).most_common(self.N)
		for item in most_frequent:
			self.features[item] = 0.0
		for item in counter:
			for k,v in self.features.items():
				if item[0] == k:
					frequency = item[1]
					value = (frequency / self.number_of_words) #sobre 100? sobre 1?
					self.features[k] = value
		print(self.features.keys())




		

		'''for item in counter:
			value = 0.0
			#print(item)
			if item[0].lower() in most_frequent:
				frequency = item[1]
				value = (frequency / self.number_of_words) #sobre 100? sobre 1?
				self.features[item[0].lower()] = value
			else:
				self.features[item[0].lower()] = value'''
			
		#print(str(self.features.keys()) #TODO: Fer printing ben fet???
