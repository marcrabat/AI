from collections import Counter
from itertools import groupby



def main():
	with open('corpus.txt', 'r') as training_set:	
		generate_model(training_set)
	training_set.close()

	#print training_set.read() #treure output fitxer

	

def generate_model(training_set):
	ocurrencies_dict = count_ocurrencies(training_set)
	with open('lexic.txt', 'w') as model:
		for key,value in ocurrencies_dict.items():
			format_to_print = str(key + " " + str(value) + "\n") 
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


main()