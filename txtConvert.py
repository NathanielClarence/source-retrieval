import os
import re

def con(filenames, counter, subdir):
    if not os.path.exists('input/'+subdir):
        os.makedirs('input/'+subdir)
    for file in filenames:
        try:
            input = open(file, 'rb')
            counter +=1
            string = str(input.read())[2:-1]
            #print(string)
            string = re.sub(r'\\t|\\n|\\r|\\x[a-z0-9]{2}', ' ', string)
            string = re.sub(r'\\\'', '\'', string)
            #print(string)
            saveFile = open("input/" + subdir + '//' +str(counter)+ ".txt", 'w', encoding='utf-8')
            #print(string)
            saveFile.write(string)
            saveFile.close()
        except:
            print(file)

    return counter