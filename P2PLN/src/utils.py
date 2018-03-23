import os
# import string
from collections import Counter
from collections import OrderedDict
import re


# TODO: nums amb comes i punts es farien aixi crec, aux.append(re.split('a-zA-Z_+', word))


class Classifier:
    def __init__(self, dataset_dir, N):
        self.dataset_dir = dataset_dir
        self.files = []  # instancies de files
        self.N = N
        self.most_frequent = []
        self.initialize_files()
        self.parse_files()

    def initialize_files(self):
        for file_name in os.listdir(self.dataset_dir):
            self.files.append(FileInstance(self.dataset_dir, file_name, self.N))

    def parse_files(self):
        for file in self.files:
            file.parse()
            #print("Original length:" + str(file.vocabulary_length) + "\n")
            #print(file.parsed_vocabulary)
            file.remove_stopwords()
            #print("After stopwords: " + str(len(file.parsed_vocabulary)) + "\n")
            #print(file.parsed_vocabulary)

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
        file_name = str(self.N) + "- results.arff"
        with open(file_name, "w") as results:
            results.write("%1. Title: Results of Features")
            results.write("\n%2. Sources:")
            results.write("\n%\tAuthors: Ferran Cantarino i Marc Rabat")
            results.write("\n@RELATION " + str(self.N) + "_Features")
            for item in self.most_frequent:
                results.write("\n@ATTRIBUTE " + str(item) + " NUMERIC")
            results.write("\n@ATTRIBUTE class {male, female}")
            results.write("\n@DATA\n")
            for file in self.files:
                for k,v in file.features.items():
                    results.write(str(str(v) + ","))
                results.write(file.gender)
                results.write("\n")

        results.close()

    #def data_format(self):
    #    for k, v in file.features.items():
    #        results.write(str(str(v) + ","))
    #    results.write(str(file.gender + "\n"))

class FileInstance:
    # shared variables among all the file instances
    punctuation = str("!#$%&()*+\"/:;<=>?[\].,^_—`{|}~")  # no cometa simple, si tota la resta

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
        # print(most_frequent)
        counter = Counter(self.parsed_vocabulary).most_common(self.N)
        for item in most_frequent:
            self.features[item] = 0
        for item in counter:
            for k, v in self.features.items():
                if item[0] == k:
                    frequency = item[1]
                    value = (frequency / self.vocabulary_length)*100  # sobre 100? sobre 1?
                    self.features[k] = value

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