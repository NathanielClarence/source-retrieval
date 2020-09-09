import Preprocessing
import nltk

def queryExtract(filename):
    input = open(filename,'r',encoding='utf-8')#'input/Bahasa/'+filename+'.txt','r', encoding='utf-8')
    content = input.read()
    input.close()

    tokens = nltk.word_tokenize(Preprocessing.process(content))
    single = []
    segments = []
    counter = 0
    ttlCount = 0
    sectionToken = []
    termFrequency = {}
    for token in tokens:
        try:
            termFrequency[token]+=1
        except:
            termFrequency[token]=1

    for token in tokens:
        single.append(token)
        counter+=1
        ttlCount+=1
        if counter == 250 or ttlCount==len(tokens):
            segments.append(single)
            sectionToken.append(counter)
            single = []
            counter =0

    sCount = {}
    relativeTF = {}
    section = 0
    ttlScore = []

    for seg in segments:
        section +=1
        for token in seg:
            if str(token) in relativeTF:
                if section in relativeTF.get(token):
                    relativeTF[token][section]=relativeTF.get(token).get(section)+1
                else:
                    relativeTF[token][section]=1
            else:
                try:
                    relativeTF[token][section]=1
                except:
                    relativeTF[token]={section:1}

    for tok in relativeTF:
        try:
            sCount[tok]=len(relativeTF.get(tok))
        except:
            sCount={tok:len(relativeTF.get(tok))}

    for token in relativeTF:
        for seg in relativeTF[token]:
            WLScore = (0.5*relativeTF.get(token).get(seg)/sectionToken[seg-1]) + (0.5 * sCount.get(token)/len(sectionToken))
            relativeTF[token][seg]=WLScore

    print(relativeTF)
    for token in relativeTF:
        for seg in relativeTF[token]:
            try:
                ttlScore[int(seg)-1]=ttlScore[int(seg)-1]+relativeTF.get(token).get(seg)
            except:
                ttlScore.append(relativeTF.get(token).get(seg))

    typesInSection = {}

    for token in relativeTF:
        for seg in relativeTF[token]:
            if seg in typesInSection:
                typesInSection[seg]=typesInSection.get(seg)+1
            else:
                typesInSection[seg]=1

    threshold = []
    pointer = 1
    for t in ttlScore:
        threshold.append(t/typesInSection.get(pointer)*0.6)
        pointer+=1

    for token in relativeTF.copy():
        for seg in relativeTF[token].copy():
            if relativeTF.get(token).get(seg) < threshold[seg-1]:
                relativeTF[token].pop(seg)
            if not relativeTF[token]:
                relativeTF.pop(token)

    listofDict = []
    for x in relativeTF:
        for y in relativeTF[x]:
            if len(listofDict)<y:
                listofDict.append({x:relativeTF.get(x).get(y)})
            else:
                listofDict[y-1][x]=relativeTF.get(x).get(y)

    selectedQueries = {}
    pointer = 1
    for dict in listofDict:
        sortedDict = sorted(dict.items(), key=lambda kv: kv[1])
        sortedDict.reverse()
        try:
            selectedQueries[pointer]=sortedDict[:10]
        except:
            selectedQueries={pointer:sortedDict[:10]}
        pointer+=1

    queries = []
    secQueries = []
    for q in selectedQueries:
        for x in range(0,10):
            try:
                secQueries.append(selectedQueries.get(q)[x][0])
            except IndexError:
                print(selectedQueries)
        queries.append(secQueries)
        secQueries=[]

    if len(queries)>3:
        pointer = 1
        for line in queries:
            for q in line:
                for x in range(pointer, len(queries)):
                    try:
                        queries[x].remove(q)
                    except ValueError:
                        print("Value not Exist")
            pointer+=1

        newq = []
        for line in queries:
            for q in line:
                newq.append(q)
        pointer = 0
        subquery = []
        queries = []
        for q in newq:
            if pointer >=10:
                queries.append(subquery)
                subquery = []
                pointer = 0
            subquery.append(q)
            pointer+=1

        if pointer>0:
            queries.append(subquery)

    for x in range(len(queries)):
        if len(queries[x])<5:
            for que in queries[x]:
                queries[x-1].append(que)
            queries.pop(x)

    return termFrequency,queries