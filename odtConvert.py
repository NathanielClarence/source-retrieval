from odf.opendocument import load
from odf import text,teletype
import os

def con(filenames, code, counter,subdir):
    if not os.path.exists('input/'+subdir):
        os.makedirs('input/'+subdir)
    for file in filenames:
        counter = counter+1
        txtString = []
        textfile = load(file)
        allparas = textfile.getElementsByType(text.P)
        for texts in allparas:
            txtString.append(teletype.extractText(texts))
        saveFile = open("input/" +subdir+'/'+ str(code)+str(counter).zfill(4) + ".txt", 'w', encoding="utf-8")
        saveFile.write(''.join(txtString))
        saveFile.close()

    return counter