import csv
import glob
import GlobalFunctions
import CreatePostingList
import os

def Merge(dict1,dict2):
    return GlobalFunctions.Merge(dict1,dict2)

def run(root):
    files = glob.glob("PLs/*.csv")
    for x in files:
        os.remove(x)

    CreatePostingList.run(root)
    filenames = glob.glob("PLs/*.csv")
    dfdict = GlobalFunctions.openFiles('PLs/dictionary/documentFreq.csv')
    totalDoc = GlobalFunctions.docCount()
    print(totalDoc)

    for file in filenames:
        try:
            d = GlobalFunctions.openFiles(file)
            for items in dicc:
                for ditem in d:
                    if items == ditem:
                        dicc[items] = Merge(dicc[items],d[ditem])
                try:
                    d.pop(items)
                    print("Value Exist and has been removed")
                except:
                    print("Value not Exist")

            dicc = Merge(dicc, d)
        except:
            print("Dictionary not Exist")
            dicc = d

    for word in dicc:
            for name in dicc[word]:
                try:
                    dicc[word][name]=round(GlobalFunctions.tfidf(dicc[word][name],dfdict[word],totalDoc),3)
                except:
                    print(dicc[word][name])
                    print(dfdict[word])
                    print(totalDoc)

    if not os.path.exists('PLs/CompiledPLs/'):
        os.makedirs('PLs/CompiledPLs/')

    with open('PLs/CompiledPLs/postingList.csv','w', encoding='utf-8', newline='')as csvfile:
        fieldname = ['Terms','Posting_List']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for word in dicc:
            writer.writerow({'Terms':word,'Posting_List':dicc[word]})
    csvfile.close()