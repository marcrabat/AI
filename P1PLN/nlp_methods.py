from collections import OrderedDict
from itertools import groupby
import operator
import random

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

def compute_accuracy(path_to_results, path_to_gold_standard):
	results = load_evaluation_format(path_to_results)
	gold_standard = load_evaluation_format(path_to_gold_standard)
	count = 0.0
	for i in xrange(len(results)):
		if results.items()[i] == gold_standard.items()[i]:
			count += 1
		else:
			print results.items()[i], "doesn't match", gold_standard.items()[i]
	precision = (count / len(results)) * 100
	print "ACCURACY: ", precision, "%"

def load_evaluation_format(path):
	with open(path, 'r') as eval:
		values = OrderedDict()
		for line in eval:
			aux = line.decode("latin-1").encode("UTF-8").split()
			values[aux[0].lower()] = aux[1]
		return values

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
			tup_key = (word, gramatical_category);
			loaded_model[tup_key] = frequency
	model.close()
	return loaded_model

def tag_with_model(path_to_test, model, output_filename):
	with open(path_to_test, 'r') as test:
		with open(output_filename, 'w') as results:
			default_gcs = compute_common_gcs(model)
			for line in test:
				word = line.decode("latin-1").encode("UTF-8").split()
				word = word[0].lower()
				prediction = compute_prediction(word, model, default_gcs)

				format_to_print = str(word) + " " + str(prediction) + "\n"
				results.write(format_to_print.decode("UTF-8").encode("latin-1"))
				
		results.close()
	
	test.close()

def compute_prediction(word, model, default_gcs):
	##MIRAR CAS EN QUE NO EXISTEIX EN EL MODEL

	matches = []
	word = word.decode("latin-1").encode("UTF-8") #needed to deal with accent problems
	for key, value in model.items():
		if key[0] == word: #if compara(key[0], word):
			matches.append((key, value))
	best_gc = compute_best_gc(matches)

	if best_gc == "NONE":
		return random.choice(default_gcs)
	else:
		return best_gc
	
def compute_common_gcs(model):
	common_dict = {}
	for k, v in model.items():
	
		if k[1] not in common_dict.keys():
			common_dict[k[1]] = int(v)
		else:
			common_dict[k[1]] += int(v)

	#return most_common_gcs.keys()
	return common_dict.keys()



def compute_best_gc(words_matched):
	best_score = 0
	best_gc = "NONE"
	for item in words_matched:
		if int(item[1]) > best_score:
			best_score = int(item[1])
			best_gc = item[0][1]
	return best_gc
