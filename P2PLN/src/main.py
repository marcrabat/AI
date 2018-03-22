
from utils import Classifier


class Main():
	dataset_dir = "dataset/"
	N = 100 #number of frequent words to be extracted

	classifier = Classifier(dataset_dir, N)
	classifier.most_frequent_words()
	classifier.compute_features()
	classifier.generate_arff()