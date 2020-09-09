import glob
import csv
import os
import math

def tfidf(tf, df, totalDoc, smooth = False):
    idf = math.log10(totalDoc/(df+int(smooth)))
    return tf * idf

def docCount():
    ttlDoc = 0
    subdirs = []
    for x in os.walk('input'):
        try:
            print(x[1][0])
            subdirs = x[1]
        except:
            print("NaN")
            break

    for subdir in subdirs:
        filenames = glob.glob("input/" + str(subdir) + "/*.txt")
        ttlDoc += len(filenames)

    return ttlDoc

def openFiles(dirFilename):
    with open(dirFilename, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                dicc[row[0]] = row[1]
            except:
                dicc = {row[0]: row[1]}
            finally:
                if "Terms" in dicc:
                    dicc.pop("Terms")
                if "Source" in dicc:
                    dicc.pop("Source")
                try:
                    dicc[row[0]] = eval(dicc.get(row[0]))
                except:
                    print("Do Nothing")

    return dicc

def Merge(dict1,dict2):
    res = {**dict1, **dict2}
    return res

def openResult(filename):
    with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x = row[1]
            y = row[2]
            z = []
            try:
                z.append(eval(x))
                z.append(eval(y))
            except:
                print("unable to eval")
                print(row[0])
            try:
                dicc[row[0]] = z
            except:
                dicc = {row[0]: z}
            finally:
                if "TestDocs" in dicc:
                    dicc.pop("TestDocs")
    return dicc

def precision(ret, src, dupsrc):
    intersection = set(ret).intersection(set(src+dupsrc))

    return len(intersection)/len(set(ret))

def recall(ret, src, dupret):
    intersection = set(ret+dupret).intersection(set(src))

    try:
        return len(intersection)/len(set(src))
    except ZeroDivisionError:
        return 0

def F1mes(prec, rec):
    F1 = 2*(prec*rec)/(prec+rec)
    return F1

def allmeasure(ret, dupRet, src, dupSrc):
    prec = precision(ret, src, dupSrc)
    rec = recall(ret, src, dupRet)
    try:
        f1 = F1mes(prec, rec)
    except ZeroDivisionError:
        f1 = 0
    return prec, rec, f1