
from utils import FeatureExtractor


class Main():
	dataset_dir = "dataset/"
	N = 5 #number of frequent words to be extracted

	f_extractor = FeatureExtractor(dataset_dir, N)
	f_extractor.compute_features()
	#f_extractor.compute_features()