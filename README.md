# Naive-Bayes-Classifier
File nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data.

python nblearn.py /path/to/text/file /path/to/label/file

The arguments are the two training files; the program learns a naive Bayes model, and writes the model parameters to a file called nbmodel.txt. 

The classification program will be invoked in the following way:

python nbclassify.py /path/to/text/file

The argument is the test data file, which has the same format as the training text file. The program reads the parameters of a naive Bayes model from the file nbmodel.txt, classifies each entry in the test data, and writes the results to a text file called nboutput.txt in the same format as the label file from the training data.
