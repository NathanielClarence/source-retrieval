import Preprocessing
from GlobalFunctions import Merge
import glob
import ntpath
import nltk
import csv

def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def oldNewDupes(sources = glob.glob("duplicate/sources/*.txt"),suspectDupe = glob.glob("duplicate/duplicates/*.txt")):
    dupesDictionary = {}

    for src in sources:
        duplicates = []
        doc = open(src, 'r', encoding='utf-8')
        string = doc.read()
        doc.close()
        src_tokens = nltk.word_tokenize(Preprocessing.process(string))

        for dp in suspectDupe.copy():
            if src == dp:
                continue
            doc = open(dp, 'r',encoding='utf-8')
            dupe = doc.read()
            doc.close()
            dupe = nltk.word_tokenize(Preprocessing.process(dupe))
            if jaccard(set(src_tokens),set(dupe)) > 0.9:
                duplicates.append(ntpath.basename(dp))
                suspectDupe.remove(dp)
                print(ntpath.basename(src))
                print(ntpath.basename(dp))

        try:
            dupesDictionary[ntpath.basename(src)]=duplicates
        except:
            dupesDictionary={ntpath.basename(src):duplicates}

    return dupesDictionary

def runANew():
    dupesDictionary = oldNewDupes()
    dupesDictionary2 = oldNewDupes(glob.glob("duplicate/sources/*.txt"), glob.glob("duplicate/sources/*.txt"))

    newDupes = oldNewDupes(glob.glob("duplicate/duplicates/*.txt"), glob.glob("duplicate/duplicates/*.txt"))
    newDupes2 = oldNewDupes(glob.glob("duplicate/duplicates/*.txt"), glob.glob("duplicate/sources/*.txt"))

    for dupe in dupesDictionary2.copy():
        if dupe in dupesDictionary:
            dupesDictionary[dupe] = dupesDictionary.get(dupe) + dupesDictionary2.get(dupe)
            dupesDictionary2.pop(dupe)

    for dupe in newDupes2.copy():
        if dupe in newDupes:
            newDupes[dupe] = newDupes2.get(dupe) + newDupes.get(dupe)
            newDupes2.pop(dupe)

    dupesDictionary = Merge(dupesDictionary,dupesDictionary2)
    newDupes = Merge(newDupes,newDupes2)

    with open('duplicate/FirstDuplicates.csv', 'w', encoding='utf-8', newline='')as csvfile:
        fieldname = ['Source', 'Duplicate_docs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for doc in dupesDictionary:
            writer.writerow({'Source': doc, 'Duplicate_docs': dupesDictionary[doc]})
    csvfile.close()

    with open('duplicate/NumericDuplicate.csv', 'w', encoding='utf-8', newline='')as csvfile:
        fieldname = ['Source', 'Duplicate_docs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for doc in newDupes:
            writer.writerow({'Source': doc, 'Duplicate_docs': newDupes[doc]})
    csvfile.close()