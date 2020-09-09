import docxpy
import os

def con(filenames, code, counter,subdir):
    if not os.path.exists('input/'+subdir):
        os.makedirs('input/'+subdir)
    for file in filenames:
        counter = counter+1
        text = docxpy.process(file)
        saveFile = open("input/"+subdir+'/'+str(code)+str(counter).zfill(4)+ ".txt", 'w', encoding="utf-8")
        saveFile.write(text)
        saveFile.close()

    return counter

#con()