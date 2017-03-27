from nblearn import open_and_preprocess
import sys


def import_model(path):
    dict_d = {}
    dict_t = {}
    dict_p = {}
    dict_n = {}
    with open(path,'r') as f:
        content = filter(None,f.read().strip().split('\n'))
        prior = [float(x.strip().split()[2]) for x in content[:4]]
        index = content.index("ConditionalProbability")
        for doc in content[index+2:]:
            words = filter(None,doc.strip().split(' '))
            dict_d[words[0]] = words[1]
            dict_t[words[0]] = words[2]
            dict_p[words[0]] = words[3]
            dict_n[words[0]] = words[4]
    return dict_d, dict_t, dict_p, dict_n, prior


def classify(dict_d, dict_t, dict_p, dict_n, prior, test_data):
    ans = ''
    for doc in test_data:
        prob_d, prob_t, prob_p, prob_n = 0.0, 0.0, 0.0, 0.0
        words = doc.strip().split(' ')
        for word in words[1:]:
            if word in dict_d.keys():
                prob_d += float(dict_d[word])
            if word in dict_t.keys():
                prob_t += float(dict_t[word])
            if word in dict_p.keys():
                prob_p += float(dict_p[word])
            if word in dict_n.keys():
                prob_n += float(dict_n[word])
        prob_d += prior[0]
        prob_t += prior[1]
        prob_p += prior[2]
        prob_n += prior[3]
        dec = decision(prob_d, prob_t, prob_p, prob_n)
        ans += str(words[0]+' '+dec+'\n')
    return ans


def decision(a, b, c, d):
    if a>b:
        ans = 'deceptive '
    else:
        ans = 'truthful '
    if c>d:
        ans += 'positive'
    else:
        ans += 'negative'
    return ans


def main():
    dict_d, dict_t, dict_p, dict_n, prior = import_model("nbmodel.txt")
    test_text = open_and_preprocess(sys.argv[1])
    result = classify(dict_d, dict_t, dict_p, dict_n, prior, test_text)
    with open("nboutput.txt", "w+") as f:
        f.write(result)

if __name__ == '__main__':
    main()