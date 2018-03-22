
from utils import FilesDealer


class Main():
	dataset_dir = "dataset/"
	N = 5 #number of frequent words to be extracted

	files_dealer = FilesDealer(dataset_dir, N)
	files_dealer.initialize_files()
	files_dealer.print_file()