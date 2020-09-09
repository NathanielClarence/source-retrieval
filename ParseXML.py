from xml.dom import minidom
import GlobalFunctions
import ntpath
import csv

def run(filename):
    xmldoc = minidom.parse(filename[:-4]+'.xml')

    if "simulatedFiles" in filename:
        plg = xmldoc.getElementsByTagName('plagiarized')
        srcs = []
        for x in plg:
            print(x.attributes['sourceid'].value)
            y = x.attributes['sourceid'].value
            if str(y)+'.txt' not in srcs:
                srcs.append(str(y)+'.txt')
    else:
        plg = xmldoc.getElementsByTagName('features')
        srcs = []
        for x in plg:
            print(x.attributes['source_reference'].value)
            y = x.attributes['source_reference'].value
            if str(y) + '.txt' not in srcs:
                srcs.append(str(y) + '.txt')

    if 'testdoc2' in filename:
        dupesDict = GlobalFunctions.openFiles('duplicate/FirstDuplicates.csv')
    else:
        dupesDict = GlobalFunctions.openFiles('duplicate/NumericDuplicate.csv')
    dupes = []
    for dupe in dupesDict:
        for x in srcs:
            if x in dupesDict.get(dupe) and dupe not in srcs:
                dupes.append(dupe)
    for x in srcs:
        print(dupesDict.get(x))
        try:
            if len(dupesDict.get(x)) > 1:
                for dupe in dupesDict.get(x):
                    if dupe not in dupes:
                        dupes.append(dupe)
            else:
                try:
                    if dupesDict.get(x)[0] not in dupes:
                        dupes = dupes + dupesDict.get(x)
                except:
                    continue
        except:
            print("not in dictionary")
    print(dupes)

    tupleS = [srcs, dupes]
    print(tupleS)
    try:
        dicc = GlobalFunctions.openResult('output/annotation.csv')
        dicc[ntpath.basename(filename[:-4])] = tupleS
    except:
        dicc = {ntpath.basename(filename[:-4]):tupleS}

    with open('output/annotation.csv', 'w', encoding='utf-8', newline='')as csvfile:
        fieldname = ['TestDocs', 'Source','Duplicates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for x in dicc:
            try:
                writer.writerow({'TestDocs':x, 'Source':dicc.get(x)[0],'Duplicates':dicc.get(x)[1]})
            except:
                writer.writerow({'TestDocs': x, 'Source': dicc.get(x)[0]})
    csvfile.close()