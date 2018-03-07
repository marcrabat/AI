from collections import OrderedDict
from itertools import groupby



def main():
	#PART 1
	print "Generating model from training_set..."
	generate_model_from_training_set('corpus.txt', 'lexic.txt')
	#PART 2
	print "Loading model from training_set..."
	model = load_model('lexic.txt')
	print "Tagging..."
	tag_with_model("test_prova.txt", model, 'results_prova.txt')
	#tag_with_model("test_2.txt", model, 'results_2.txt')

	#PART 3
	print "Computing results..."
	compute_accuracy('results_prova.txt', 'gold_standard_prova.txt')


def compute_accuracy(path_to_results, path_to_gold_standard):
	results = load_evaluation_format(path_to_results)
	gold_standard = load_evaluation_format(path_to_gold_standard)
	count = 0.0
	for i in xrange(len(results)):
		if results.items()[i] == gold_standard.items()[i]:
			count += 1
		else:
			print results.items()[i], "doesn't match", gold_standard.items()[i]
	precision = (count / len(results))
	print "Precision of the approximation: ", precision

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

	#print word, " doesn't appear in the model"
	matches = []
	for key, value in model.items():
		if key[0] == word:
			print key, value
			matches.append((key, value))
	#print "Matches of ", word, "--> ", matches
	best_gc = compute_best_gc(matches)
	#print "Returned: ", best_gc 
	if best_gc == "NONE":
		print "no trobat"
	else:
		return best_gc
	

def compute_best_gc(words_matched):
	best_score = 0
	best_gc = "NONE"
	print words_matched
	return ""


main()


'''('en', 'NP') doesn't match ('en', 'Prep')
('los', 'Pron') doesn't match ('los', 'Det')
('la', 'NP') doesn't match ('la', 'Det')
('editoriales', 'Adj') doesn't match ('editoriales', 'NC')
('europa', 'Adj') doesn't match ('europa', 'NP')
('por', 'NP') doesn't match ('por', 'Prep')
('primera', 'NC') doesn't match ('primera', 'Adj')
('las', 'NP') doesn't match ('las', 'Det')
('venezuela', 'NC') doesn't match ('venezuela', 'NP')
('espa\xc3\x83\xc2\xb1a', 'NC') doesn't match ('espa\xc3\x83\xc2\xb1a', 'NP')'''