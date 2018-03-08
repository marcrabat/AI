import time
from nlp_methods import *


def main():
	start_time = time.time()
	#PART 1
	
	print "Generating model from training_set..."
	generate_model_from_training_set('corpus.txt', 'lexic.txt')
	
	#PART 2
	print "Loading model from training_set..."
	model = load_model('lexic.txt')
	print "Tagging..."
	tag_with_model("test_1.txt", model, 'results_1.txt')
	#tag_with_model("test_2.txt", model, 'results_2.txt')
	
	#PART 3
	print "Computing results..."
	compute_accuracy('results_1.txt', 'gold_standard_1.txt')
	print "--- %s seconds ---" % (time.time() - start_time)

########################################################################

main()
