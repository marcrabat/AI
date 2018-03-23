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
			#print(file.input_text)
			file.parse()
			file.remove_stopwords()
		#self.files[0].parse()
		#self.files[0].remove_stopwords()
	def most_frequent_words(self):
		for file in self.files:
			for word in file.parsed_text:
				self.num_words_corpus += 1
				self.most_frequent.append(word.lower())
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
			#print(file.file_name)
			file.compute_vector(self.most_frequent)

			#print(file.gender)
			#print(file.features)

	def generate_arff(self):
		with open("results.arff", "w") as results:
			results.write("%1. Title: Results of Features")
			results.write("\n%2. Sources:")
			results.write("\n%\tAuthors: Ferran Cantarino i Marc Rabat")
			results.write("\n@RELATION " + str(self.N) + "_Features")
			for item in self.most_frequent:
				results.write("\n@ATTRIBUTE " + str(item) + " NUMERIC")
			results.write("\n@ATTRIBUTE class {male, female}")
			results.write("\n@DATA\n")
			for file in self.files:
				for k,v in file.features.items():
					results.write(str(str(v) + ","))
				results.write(str(file.gender+"\n"))


		results.close()




class FileInstance():
	#shared variables among all the file instances
	with open("stopwords.txt", "r") as sw:
		stopwords = sw.read().splitlines()
	sw.close()
	to_remove = punctuation + "—"
	#to_remove = to_remove.replace("@","")
	punct = str.maketrans('','', to_remove) #create translation in order to use with translate, this erase the unnecessary symbols

	#instance variables
	def __init__(self, dataset_dir, file_name, N_freq):
		self.file_name = file_name
		self.gender = re.sub('^[^A-Za-z]*', '', self.file_name)
		self.file_descriptor = dataset_dir + file_name
		self.input_text = []
		self.vocabulary = []
		self.parsed_list = []
		
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
		self.first_pass()

		self.parsed_text
		while '' in self.parsed_text:
			self.parsed_text.remove('')
		#update the number of legal words in the text before eliminate stopwords
		self.number_of_words = len(self.parsed_text)
		#print(self.number_of_words)
		#print(self.parsed_text)
		del self.input_text[:] #after the input is analyzed, it is not needed anymore

	def first_pass(self):
		for word in self.input_text:
			first_pass = word.lower().split()
			for word1 in first_pass:
				word2 = re.sub('[\\\\/*?()"<>|]', '', word1) #falten punts i comes (mirar números i merdes)
				if(word2 != None):
					self.parsed_list.append(word2)
		for item in self.parsed_list:
			if(item != '-'):
				print(item)

		


	
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
			self.features[item] = 0
		for item in counter:
			for k,v in self.features.items():
				if item[0] == k:
					frequency = item[1]
					value = (frequency / self.number_of_words) #sobre 100? sobre 1?
					self.features[k] = value
		#print(self.features.keys())
