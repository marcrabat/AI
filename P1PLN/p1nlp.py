from collections import Counter
from itertools import groupby



def main():
	generate_model_from_training_set('corpus.txt', 'lexic.txt')
	
	model = load_model('lexic.txt')
	tag_with_model("test_prova.txt", model, 'results_1.txt')
	#tag_with_model("test_2.txt", model, 'results_2.txt')


def generate_model_from_training_set(path_to_training_set, output_filename):
	with open(path_to_training_set, 'r') as training_set:	
		write_model_to_file(training_set, output_filename)
	training_set.close()

def write_model_to_file(training_set, output_filename):
	ocurrencies_dict = count_ocurrencies(training_set)
	with open(output_filename, 'w') as model:
		for key,value in ocurrencies_dict.items():
			format_to_print = str(key + " " + str(value) + "\n") 
			format_to_print.decode("UTF-8").encode('latin-1')
			model.write(format_to_print) 
	model.close()

def count_ocurrencies(training_set):
	words_and_tags_dict = {}
	for line in training_set:
		aux = line.decode("latin-1").encode("UTF-8").split()
		aux[0] = aux[0].lower()
		string = str(aux[0] + " " + aux[1])
		if string not in words_and_tags_dict:
			words_and_tags_dict[string] = 1
		else:
			words_and_tags_dict[string] += 1
	return words_and_tags_dict

def load_model(path_to_model):
	with open(path_to_model, 'r') as model:
		loaded_model = {}
		for line in model:
			aux = line.decode("latin-1").encode("UTF-8").split()
			word = aux[0].lower()
			gramatical_category = aux[1]
			frequency = aux[2]
			loaded_model[word, gramatical_category] = frequency
	model.close()
	return loaded_model

def tag_with_model(path_to_test, model, output_filename):
	with open(path_to_test, 'r') as test:
		words = []
		with open(output_filename, 'w') as results:
			for line in test:
				word = line.decode("latin-1").encode("UTF-8").split()
				word = word[0].lower()
				prediction = compute_prediction(word, model)
				tup = (word, prediction)
				format_to_print = tup[0] + " " + tup[1] + "\n"
				results.write(format_to_print.decode("UTF-8").encode("latin-1"))
				
		results.close()
	
	test.close()

def compute_prediction(word, model):
	##MIRAR CAS EN QUE NO EXISTEIX EN EL MODEL
	matches = []
	for key, value in model.items():
		if key[0] == word:
			matches.append((key[1], value))  
	return compute_best_gc(matches)

def compute_best_gc(words_matched):
	best_score = 0
	best_gc = "NONE"
	for item in words_matched:
		if int(item[1]) > best_score:
			best_score = int(item[1])
			best_gc = item[0]
	return best_gc
			


main()