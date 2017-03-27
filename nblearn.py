import sys
import re
import math


class Document:
    label1 = ''
    label2 = ''
    data = ''
    id1 = ''

    def __init__(self, label1, label2, data, id1):
        self.label1 = label1
        self.label2 = label2
        self.data = data
        self.id1 = id1

    def count_terms_in_doc(self, data):
        dict1 = {}
        words = data.strip().split(' ')
        for word in words:
            if not dict1.has_key(word):
                dict1[word] = 1
            else:
                dict1[word] += 1
        return dict1


def rep(s, line):
    regex = "[0-9]+" + s
    spe = re.search(regex, line)
    if spe is not None:
        findst = spe.group()
        findst = findst.replace(s, "")
        l = re.sub(regex, findst, line)
        return l
    else:
        return line


def open_and_preprocess(path):
    proc_data = []
    with open(path, 'r') as f:
        contents = f.read().strip().split("\n")
        for line in contents:
            words = line.strip().split(" ")
            l1 = re.sub(r'-', ' ', ' '.join(words[1:]))
            l2 = re.sub(r'\.', ' ', l1)
            l3 = re.sub(r',', ' ', l2)
            l4 = re.sub(r"'", ' ', l3)
            l5 = re.sub(r"/", ' ', l4)
            line_noPunctuation = re.sub(r'[^a-zA-Z ]', r' ', l5)
            line_noPunctuation = rep("st", line_noPunctuation)
            line_noPunctuation = rep("nd", line_noPunctuation)
            line_noPunctuation = rep("rd", line_noPunctuation)
            line_noPunctuation = rep("th", line_noPunctuation)
            words1 = line_noPunctuation.strip().split(" ")
            words1 = filter(None, words1)
            words1 = map(lambda x: x.lower(), words1)
            words1.insert(0, words[0])
            proc_data.append(' '.join(words1))
    return proc_data


def train_model(text, label):
    '''dict_d = {}
    dict_t = {}
    count_dt = {}
    dict_p = {}
    dict_n = {}
    count_pn = {}'''
    bow = {}
    bagOfWords = ''
    Documents = []
    len_doc = 0
    for doc in text:
        words = doc.strip().split(' ')
        id_doc = words[0]
        data_doc = ' '.join(words[1:])
        for l in label:
            wrds = l.strip().split(' ')
            id_l = wrds[0]
            if id_l == id_doc:
                bagOfWords = bagOfWords + data_doc + ' '
                bow = list(set(bagOfWords.strip().split(' ')))
                Documents.append(Document(wrds[1], wrds[2], data_doc, id_doc))
    len_doc = len(Documents)
    dict_d, dict_t, count_dt = check_dt(bow, Documents)
    dict_p, dict_n, count_pn = check_pn(bow, Documents)
    return dict_d, dict_t, count_dt, dict_p, dict_n, count_pn, bow, len_doc


def check_dt(bow, Documents):
    dict_d = {}
    dict_t = {}
    count_dt = [0, 0]
    for word in bow:
        dict_d[word] = 0
        dict_t[word] = 0
    for i in Documents:
        if i.label1 == 'deceptive':
            count_dt[0] += 1
            for k, v in i.count_terms_in_doc(i.data).iteritems():
                dict_d[k] += v
        elif i.label1 == 'truthful':
            count_dt[1] += 1
            for k, v in i.count_terms_in_doc(i.data).iteritems():
                dict_t[k] += v
    return dict_d, dict_t, count_dt


def check_pn(bow, Documents):
    dict_p = {}
    dict_n = {}
    count_pn = [0, 0]
    for word in bow:
        dict_p[word] = 0
        dict_n[word] = 0
    for i in Documents:
        if i.label2 == 'positive':
            count_pn[0] += 1
            for k, v in i.count_terms_in_doc(i.data).iteritems():
                dict_p[k] += v
        elif i.label2 == 'negative':
            count_pn[1] += 1
            for k, v in i.count_terms_in_doc(i.data).iteritems():
                dict_n[k] += v
    return dict_p, dict_n, count_pn


def disp_and_store(dict_d, dict_t, count_dt, dict_p, dict_n, count_pn, bow, len_doc):
    fileContents = []
    width_col0 = max([len(word) for word in list(bow)]) + 5
    width_col1 = len('deceptive') + 4
    width_col2 = len('deceptive') + 4
    width_col3 = len('deceptive') + 4
    width_col4 = len('deceptive') + 4
    # print count_dt[0]+count_dt[1]
    # print "P(Deceptive and Positive) = " + str(round(float(count[0]) / len_doc, 9))
    fileContents.append("P(Deceptive) = " + str(math.log(float(count_dt[0]) / len_doc)))

    # print "\nP(Deceptive and Negative) = " + str(round(float(count[1]) / len_doc, 9))
    fileContents.append("\nP(Truthful) = " + str(math.log(float(count_dt[1]) / len_doc)))

    # print "\nP(Truthful and Positive) = " + str(round(float(count[2]) / len_doc, 9))
    fileContents.append("\nP(Positive) = " + str(math.log(float(count_pn[0]) / len_doc)))

    # print "\nP(Truthful and Negative) = " + str(round(float(count[3]) / len_doc, 9))
    fileContents.append("\nP(Negative) = " + str(math.log(float(count_pn[1]) / len_doc)))

    # print '\nBefore smoothing'
    fileContents.append('\n\nBefore smoothing')
    # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "Deceptive", "Truthful", "Positive", "Negative",
    #                                                                              Word=width_col0, class1=width_col1,
    #                                                                              class2=width_col2, class3=width_col3,
    #                                                                              class4=width_col4)
    fileContents.append(
        "\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "Deceptive",
                                                                                        "Truthful", "Positive",
                                                                                        "Negative",
                                                                                        Word=width_col0,
                                                                                        class1=width_col1,
                                                                                        class2=width_col2,
                                                                                        class3=width_col3,
                                                                                        class4=width_col4))

    for word in list(bow):
        # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(dict_dp[word]),  str(dict_dn[word]), str(dict_tp[word]), str(dict_tn[word]), Word=width_col0, class1=width_col1, class2=width_col2, class3=width_col3, class4=width_col4)
        fileContents.append(
            "\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(dict_d[word]),
                                                                                            str(dict_t[word]),
                                                                                            str(dict_p[word]),
                                                                                            str(dict_n[word]),
                                                                                            Word=width_col0,
                                                                                            class1=width_col1,
                                                                                            class2=width_col2,
                                                                                            class3=width_col3,
                                                                                            class4=width_col4))
    # Smoothing
    for k in dict_d.iterkeys():
        dict_d[k] += 1
    for k in dict_t.iterkeys():
        dict_t[k] += 1
    for k in dict_p.iterkeys():
        dict_p[k] += 1
    for k in dict_n.iterkeys():
        dict_n[k] += 1
    sum_d = sum(dict_d.values())
    sum_t = sum(dict_t.values())
    sum_p = sum(dict_p.values())
    sum_n = sum(dict_n.values())
    # print '\nAfter smoothing'
    fileContents.append('\n\nAfter smoothing')
    # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "DP", "DN", "TP", "TN",
    #                                                                              Word=width_col0, class1=width_col1,
    #                                                                              class2=width_col2, class3=width_col3,
    #                                                                              class4=width_col4)
    fileContents.append(
        "\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "Deceptive",
                                                                                        "Truthful", "Positive",
                                                                                        "Negative",
                                                                                        Word=width_col0,
                                                                                        class1=width_col1,
                                                                                        class2=width_col2,
                                                                                        class3=width_col3,
                                                                                        class4=width_col4))

    for word in list(bow):
        # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(dict_dp[word]),  str(dict_dn[word]), str(dict_tp[word]), str(dict_tn[word]), Word=width_col0, class1=width_col1, class2=width_col2, class3=width_col3, class4=width_col4)
        fileContents.append(
            "\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(dict_d[word]),
                                                                                            str(dict_t[word]),
                                                                                            str(dict_p[word]),
                                                                                            str(dict_n[word]),
                                                                                            Word=width_col0,
                                                                                            class1=width_col1,
                                                                                            class2=width_col2,
                                                                                            class3=width_col3,
                                                                                            class4=width_col4))
    # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Total", str(sum(dict_dp.values())),
    #                                                                              str(sum(dict_dn.values())),
    #                                                                              str(sum(dict_tp.values())),
    #                                                                              str(sum(dict_tn.values())),
    #                                                                              Word=width_col0, class1=width_col1,
    #                                                                              class2=width_col2, class3=width_col3,
    #                                                                              class4=width_col4)
    fileContents.append("\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Total", str(
        sum(dict_d.values())),
                                                                                                        str(sum(
                                                                                                            dict_t.values())),
                                                                                                        str(sum(
                                                                                                            dict_p.values())),
                                                                                                        str(sum(
                                                                                                            dict_n.values())),
                                                                                                        Word=width_col0,
                                                                                                        class1=width_col1,
                                                                                                        class2=width_col2,
                                                                                                        class3=width_col3,
                                                                                                        class4=width_col4))

    # print "\nConditionalProbability"
    width_col0 = max([len(word) for word in list(bow)]) + 15
    width_col1 = len('deceptive') + 14
    width_col2 = len('deceptive') + 14
    width_col3 = len('deceptive') + 14
    width_col4 = len('deceptive') + 14
    fileContents.append("\n\nConditionalProbability")

    # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "DP", "DN", "TP", "TN",
    #                                                                              Word=width_col0, class1=width_col1,
    #                                                                              class2=width_col2, class3=width_col3,
    #                                                                              class4=width_col4)
    fileContents.append(
        "\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format("Words", "Deceptive",
                                                                                        "Truthful", "Positive",
                                                                                        "Negative",
                                                                                        Word=width_col0,
                                                                                        class1=width_col1,
                                                                                        class2=width_col2,
                                                                                        class3=width_col3,
                                                                                        class4=width_col4))

    for word in bow:
        # print "{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(
        #    round(float(dict_dp[word]) / sum_dp, 9)), str(round(float(dict_dn[word]) / sum_dn, 9)), str(
        #    round(float(dict_tp[word]) / sum_tp, 9)), str(round(float(dict_tn[word]) / sum_tn, 9)), Word=width_col0,
        #                                                                              class1=width_col1, class2=width_col2,
        #                                                                              class3=width_col3, class4=width_col4)
        fileContents.append("\n{0:<{Word}} {1:<{class1}} {2:<{class2}} {3:<{class3}} {4:<{class4}} ".format(word, str(
            math.log(float(dict_d[word]) / sum_d)), str(math.log(float(dict_t[word]) / sum_t)), str(
            math.log(float(dict_p[word]) / sum_p)), str(math.log(float(dict_n[word]) / sum_n)), Word=width_col0,
                                                                                                            class1=width_col1,
                                                                                                            class2=width_col2,
                                                                                                            class3=width_col3,
                                                                                                            class4=width_col4))
    with open("nbmodel.txt", "w+") as f:
        f.write("".join(fileContents))


def main():
    train_text = open_and_preprocess(sys.argv[1])
    train_label = open_and_preprocess(sys.argv[2])
    dict_d, dict_t, count_dt, dict_p, dict_n, count_pn, bow, len_doc = train_model(train_text, train_label)
    disp_and_store(dict_d, dict_t, count_dt, dict_p, dict_n, count_pn, bow, len_doc)


if __name__ == '__main__':
    main()
