from utils import Classifier


class Main():
    dataset_dir = "dataset/"

    print("Enter the number of frequent words to use:")
    N = int(input())

    print("Remove stopwords? [y/n]")
    flag_stopwords = str(input())

    classifier = Classifier(dataset_dir, int(N), flag_stopwords)
    classifier.most_frequent_words()
    classifier.compute_features()
    classifier.generate_arff()
