import os
from collections import Counter
from collections import OrderedDict
import re


# nums i comes: aux.append(re.split('a-zA-Z_+', word))

class Classifier:
    def __init__(self, dataset_dir, N, flag_stopwords):
        self.dataset_dir = dataset_dir
        self.files = []  # instancies de files
        self.N = N
        self.most_frequent = []
        self.remove_stopwords = True
        if flag_stopwords is 'n':
            self.remove_stopwords = False
        self.initialize_files()
        self.parse_files()

    def initialize_files(self):
        for file_name in os.listdir(self.dataset_dir):
            self.files.append(FileInstance(self.dataset_dir, file_name, self.N))

    def parse_files(self):
        for file in self.files:
            file.parse()
            if self.remove_stopwords:
                file.remove_stopwords()
            # print(file.parsed_vocabulary)

    def most_frequent_words(self):
        for file in self.files:
            for word in file.parsed_vocabulary:
                self.most_frequent.append(word)
        self.most_frequent = Counter(self.most_frequent).most_common(self.N)
        aux = []
        for item in self.most_frequent:
            aux.append(item[0].lower())
        self.most_frequent = aux
        print(self.most_frequent)

    def compute_features(self):
        for file in self.files:
            file.compute_vector(self.most_frequent)


    def generate_arff(self):
        file_name = str(self.N) + "- results - StopwordsRemoved: " + str(self.remove_stopwords) + ".arff"
        with open(file_name, "w") as results:
            results.write("%1. Title: Results of Features")
            results.write("\n%2. Sources:")
            results.write("\n%\tAuthors: Ferran Cantarino i Marc Rabat")
            results.write("\n@RELATION " + str(self.N) + "_Features")
            for item in self.most_frequent:
                aux = item
                if "\'" in item:
                    aux = item.replace("\'", ".")
                results.write("\n@ATTRIBUTE " + str(aux) + " NUMERIC")
            results.write("\n@ATTRIBUTE class {male, female}")
            results.write("\n@DATA\n")
            for file in self.files:
                for k, v in file.features.items():
                    results.write(str(str(v) + ","))
                results.write(file.gender)
                results.write("\n")

        results.close()


class FileInstance:
    # shared variables among all the file instances
    punctuation = str("!#$%&()*+\"/:;<=>@?[\].,^_—`{|}~")  # no cometa simple, si tota la resta

    with open("stopwords.txt", "r") as sw:
        stopwords = sw.read().splitlines()
    sw.close()

    # instance variables
    def __init__(self, dataset_dir, file_name, N):
        # File Information
        self.file_name = file_name
        self.gender = re.sub('^[^A-Za-z]*', '', self.file_name)
        self.file_descriptor = dataset_dir + file_name
        # File data
        with open(self.file_descriptor) as fd:
            self.vocabulary = fd.read().lower().split()
        fd.close()

        self.N = N
        self.vocabulary_length = 0
        self.parsed_vocabulary = []
        self.features = OrderedDict()

    def compute_vector(self, most_frequent):
        for item in most_frequent:
            self.features[item] = 0

        for word in self.parsed_vocabulary:
            for item in most_frequent:
                count = 0
                if word == item:
                    count += 1
                    self.features[item] = count

        for k,v in self.features.items():
            self.features[k] = (v / self.vocabulary_length)


    def parse(self):
        self.first_pass()
        self.second_pass()
        self.vocabulary_length = len(self.parsed_vocabulary)

    def first_pass(self):
        # primera passada es carrega guionets sueltus i abans d'afegir a llista treu puntuacio
        # per evitar que es quedin paraules enganxades, faig un return per gestionarlo dps
        for word in self.vocabulary:
            if word is not '-':
                new_word = re.sub('[' + self.punctuation + ']', '\n', word)
                self.parsed_vocabulary.append(new_word)

    def second_pass(self):
        # faig un split amb el caracter de return i no afegeixo els resultants que quedin en blanc
        # ja que l'split genera una llista separada per aquests caracters
        aux_parsed = []
        for word in self.parsed_vocabulary:
            aux = word.split("\n")
            for item in aux:
                if item is not "":
                    aux_parsed.append(item)
        self.parsed_vocabulary = aux_parsed

    def remove_stopwords(self):
        newlist = []
        for word in self.parsed_vocabulary:
            if word not in self.stopwords:
                newlist.append(word)
        self.parsed_vocabulary = newlist
