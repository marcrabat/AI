from utils import Classifier
import sys


class Main():
    dataset_dir = "dataset/"
    # N = 5  # number of frequent words to be extracted
    #TODO: Gestionar que input sigui correcte
    #classifier = Classifier(dataset_dir, int(sys.argv[1]))  # agafar N en cridar programa
    classifier = Classifier(dataset_dir, int(20))  # agafar N en cridar programa
    classifier.most_frequent_words()
    classifier.compute_features()
    classifier.generate_arff()
