import time
from nlp_methods import *


def main():
	start_time = time.time()
	print "Enter the # of test you want to prove:"
	num = raw_input()
	test = "test_" + str(num) + ".txt"
	gold_standard = "gold_standard_" + str(num) + ".txt"
	results = "results_" + str(num) + ".txt"

	#PART 1
	print "Generating model from training_set..."
	generate_model_from_training_set('corpus.txt', 'lexic.txt')
	
	#PART 2
	print "Loading model from training_set..."
	model = load_model('lexic.txt')
	print "Tagging", test ,"..."
	tag_with_model(test, model, results)
	
	#PART 3
	print "Computing results of ", results , " vs. ", gold_standard, "..."
	compute_accuracy(results, gold_standard)
	print "--- %s seconds ---" % (time.time() - start_time)

########################################################################

main()
