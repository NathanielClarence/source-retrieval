import TestDocProcessing
import GlobalFunctions
import math
import tkinter
import operator
import ntpath
import os
import csv

def getSource(testTF, queries,dicc,df):
    queryResult = {}

    for x in queries:
        queryResult[x] = dicc.get(x)
    print(queryResult)

    totalDoc = GlobalFunctions.docCount()
    for word in testTF:
        try:
            try:
                testTF[word] = round(GlobalFunctions.tfidf(testTF[word], df[word], totalDoc),3)#, smooth=True), 3)
            except KeyError:
                testTF[word] = round(GlobalFunctions.tfidf(testTF[word], 1, totalDoc),3)#, smooth=True))
        except:
            print(dicc[word])
            print(df[word])
            print(totalDoc)

    sr = testTF.copy()
    testTF = {}

    for x in queries:
        if x in sr:
            testTF[x] = sr.get(x)

    normalizedTest = 0
    dotProduct = {}
    normalizedDoc = {}

    for q in testTF:
        try:
            for doc in queryResult[q]:
                if doc in dotProduct:
                    dotProduct[doc] += testTF.get(q) * queryResult.get(q).get(doc)
                else:
                    dotProduct[doc] = testTF.get(q) * queryResult.get(q).get(doc)
                try:
                    normalizedDoc[doc] += math.pow(queryResult.get(q).get(doc), 2)
                except:
                    normalizedDoc[doc] = math.pow(queryResult.get(q).get(doc), 2)
        except TypeError:
            print(q)
        finally:
            normalizedTest += math.pow(testTF.get(q), 2)

    for doc in normalizedDoc:
        normalizedDoc[doc] = math.sqrt(normalizedDoc[doc])
    normalizedTest = math.sqrt(normalizedTest)

    cosineSim = {}
    for doc in dotProduct:
        cosineSim[doc] = dotProduct[doc] / (normalizedDoc[doc] * normalizedTest)

    sortResult = sorted(cosineSim.items(), key=lambda kv: kv[1])
    sortResult.reverse()
    return sortResult[:10]

def run(filename, root, show = True, filter = True, filamt = 5):
    dicc = GlobalFunctions.openFiles('PLs/CompiledPLs/postingList.csv')
    df = GlobalFunctions.openFiles('PLs/dictionary/documentFreq.csv')
    testTF, queries = TestDocProcessing.queryExtract(filename)
    querySources = []
    counter = 0
    if show:
        win = tkinter.Toplevel(root)
        win.minsize(200, 200)
        win.title("Search Query for "+ntpath.basename(filename))
    c=0
    for que in queries:
        r=0
        counter +=1
        querySources.append(getSource(testTF,que,dicc,df))
        if show:
            tkinter.Label(win, text = "Search Query "+str(counter)).grid(row=r, column = c, padx = 3)
        r+=1
        try:
            for q in que:
                if show:
                    tkinter.Label(win, text=q).grid(row=r, column = c, padx= 3)
                r +=1
        except:
            print("unable to call new window")
        c += 1

    if show:
        qwin = tkinter.Toplevel(win)
        qwin.minsize(200, 200)
        qwin.title("Query Result for " + ntpath.basename(filename))
        c=0
        counter = 0
        for src in querySources:
            r=0
            counter+=1
            tkinter.Label(qwin, text = "Query Result "+str(counter)).grid(row=r, column = c, padx = 3)
            tkinter.Label(qwin, text="Percentage " + str(counter)).grid(row=r, column=c+1, padx=3)
            r+=1
            try:
                for s in src:
                    tkinter.Label(qwin, text = s[0]).grid(row=r, column = c, padx = 3)
                    tkinter.Label(qwin, text = round(s[1]*100,2)).grid(row=r,column = c+1, padx=3)
                    r+=1
            except:
                print("no val")
            c+=2

    result =[]
    for n in querySources:
        for x in n:
            result.append(x)

    result.sort(key=operator.itemgetter(1))
    result.reverse()
    filters = []
    copyResult = result.copy()
    result = []
    for x in copyResult:
        if x[0] not in filters:
            filters.append(x[0])
            result.append(x)
    print(result)

    if 'testdoc2' in filename:
        dupes = GlobalFunctions.openFiles('duplicate/FirstDuplicates.csv')
    else:
        dupes = GlobalFunctions.openFiles('duplicate/NumericDuplicate.csv')
    duplicate = []

    copyRes = result.copy()
    result = []
    for res in copyRes:
        result.append(res[0])

    for res in result.copy():
        try:
            for x in dupes.get(res):
                if x not in duplicate and res not in duplicate:
                    duplicate.append(x)
                    result.remove(x)
        except:
            pass

    if 'testdoc2' in filename:
        dupes = GlobalFunctions.openFiles('duplicate/NumericDuplicate.csv')
    else:
        dupes = GlobalFunctions.openFiles('duplicate/FirstDuplicates.csv')

    for res in result.copy():
        try:
            for x in dupes.get(res):
                if x not in duplicate and res not in duplicate:
                    duplicate.append(x)
                    result.remove(x)
        except:
            pass

    print(result)
    print(duplicate)

    if filter:
        result = result[:filamt]
        if 'testdoc2' in filename:
            dupes = GlobalFunctions.openFiles('duplicate/FirstDuplicates.csv')
        else:
            dupes = GlobalFunctions.openFiles('duplicate/NumericDuplicate.csv')
        duplicate = []
        for res in result:
            try:
                for x in dupes.get(res):
                    duplicate.append(x)
            except:
                pass

    if show:
        fres = tkinter.Toplevel(qwin)
        fres.minsize(200, 200)
        fres.title("Source Candidate for " + ntpath.basename(filename))
        c = 0
        r = 0
        dr = 0
        counter += 1
        tkinter.Label(fres, text="Query Result").grid(row=r, column=c, padx=3)
        r += 1
        try:
            for s in result:
                tkinter.Label(fres, text=s).grid(row=r, column=c, padx=3)
                r += 1
            for d in duplicate:
                dr+=1
                tkinter.Label(fres, text="Duplicate").grid(row=0, column=c+1, padx=3)
                tkinter.Label(fres,text = d).grid(row=dr, column=c+1, padx=3)
        except:
            print("no val")

    if not os.path.exists('output/'):
        os.makedirs('output/')

    copyResult = []
    for res in result.copy():
        copyResult.append(res)
    copyDupe = []
    for dupes in duplicate.copy():
        copyDupe.append(dupes)
    tupleS = [copyResult, copyDupe]
    print(tupleS)

    print(result)
    print(duplicate)

    if filter and filamt == 5:
        saveResult = 'output/resultsFilter5.csv'
    elif filter and filamt ==10:
        saveResult = 'output/resultsFilter10.csv'
    else:
        saveResult = 'output/resultsNoFil.csv'

    try:
        dicc = GlobalFunctions.openResult(saveResult)
        dicc[ntpath.basename(filename[:-4])] = tupleS
    except:
        dicc = {ntpath.basename(filename[:-4]):tupleS}

    if filter:
        with open('output/resultsFilter'+str(filamt)+'.csv', 'w', encoding='utf-8', newline='')as csvfile:
            fieldname = ['TestDocs', 'Source_Candidate','Duplicates']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            writer.writeheader()
            for x in dicc:
                try:
                    writer.writerow({'TestDocs':x, 'Source_Candidate':dicc.get(x)[0],'Duplicates':dicc.get(x)[1]})
                except:
                    writer.writerow({'TestDocs': x, 'Source_Candidate': dicc.get(x)[0]})
        csvfile.close()
    else:
        with open('output/resultsNoFil.csv', 'w', encoding='utf-8', newline='')as csvfile:
            fieldname = ['TestDocs', 'Source_Candidate','Duplicates']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            writer.writeheader()
            for x in dicc:
                try:
                    writer.writerow({'TestDocs':x, 'Source_Candidate':dicc.get(x)[0],'Duplicates':dicc.get(x)[1]})
                except:
                    writer.writerow({'TestDocs': x, 'Source_Candidate': dicc.get(x)[0]})
        csvfile.close()

    return copyResult,copyDupe