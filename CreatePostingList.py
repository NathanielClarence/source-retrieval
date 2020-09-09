import glob
import Preprocessing
import csv
import os
import nltk
import ntpath
import tkinter

def run(root):
    subdirs = []
    for x in os.walk('input'):
        try:
            print(x[1][0])
            subdirs=x[1]
        except:
            print("NaN")
            break

    dfdict = {}
    ttlDoc = 0

    for subdir in subdirs:
        unprocessed = []
        #print(subdir)
        filenames = glob.glob("input/"+str(subdir)+"/*.txt")
        tfdict = {}
        #print(filenames)

        for file in filenames:
            #print(file)
            try:
                input = open(file, 'r',encoding='utf-8')
                string = input.read()
                ttlDoc = ttlDoc+1
                input.close()

                fname = ntpath.basename(file)
                tokens = nltk.word_tokenize(Preprocessing.process(string))

                for x in tfdict:
                    tfdict[x][fname]= 0

                for x in tokens:
                    #print(x)
                    if str(x) in tfdict:
                        if fname in tfdict.get(x):
                            tfdict[x][fname]=tfdict.get(x).get(fname)+1
                        else:
                            tfdict[x][fname]=1
                    else:
                        try:
                            for n in tfdict.get(next(iter(tfdict))):
                                try:
                                    tfdict[x][n] = 0
                                except:
                                    tfdict[x] = {n:0}
                            tfdict[x][fname]=1
                        except:
                            tfdict[x] = {fname: 1}
            except:
                unprocessed.append(file)
                print(file)

        for x in tfdict:
            #dfdict[x] = len(tfdict[x].keys())
            dfdict[x] = 0
            for n in tfdict[x]:
                if tfdict[x][n] is not 0:
                    dfdict[x] = dfdict[x]+1
            #print(dfdict)

        newDict = {}
        for word in tfdict:
            for name in tfdict[word]:
                try:
                    if tfdict[word].get(name) != 0:
                        newDict[word][name] = tfdict[word].get(name)
                except:
                    newDict[word] = {name:tfdict[word].get(name)}
            #print(newDict[word])
            #newDict[word] = list(newDict[word].items())

        if not os.path.exists('PLs/'):
            os.makedirs('PLs/')

        with open('PLs/postingList'+subdir+'.csv','w', encoding='utf-8', newline='')as csvfile:
            fieldname = ['Terms','Posting_List']
            writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            writer.writeheader()
            for word in newDict:
                writer.writerow({'Terms':word,'Posting_List':newDict[word]})
        csvfile.close()
        if len(unprocessed)>0:
            win = tkinter.Toplevel(root)
            row = 1
            column = 0
            tkinter.Label(win, text="Unable to process:").grid(row = 0,column = 0, padx=5, pady=5)
            for x in unprocessed:
                tkinter.Label(win, text=ntpath.basename(x)).grid(row = row,column=column, padx=5,pady=5)
                row+=1
                if row==11:
                    row = 1
                    column+=1
            win.minsize(200,200)

    if not os.path.exists('PLs/dictionary/'):
        os.makedirs('PLs/dictionary/')

    with open('PLs/dictionary/documentFreq.csv', 'w', encoding='utf-8', newline='')as csvfile:
        fieldname = ['Terms', 'Document_Frequency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for word in dfdict:
            writer.writerow({'Terms': word, 'Document_Frequency': dfdict[word]})
    csvfile.close()