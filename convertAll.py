import docConvert
import odtConvert
import txtConvert
import os
import glob

def run():
    txtCounter = 0
    for x in os.walk('sourcedoc'):
        try:
            print(x[1][0])
            subdirs = x[1]
        except:
            print("NaN")
            break

        for subdir in subdirs:
            counter = 0
            #counter=counter+1
            odt = glob.glob("sourcedoc/" + str(subdir) + "/*.odt")
            doc = glob.glob("sourcedoc/" + str(subdir) + "/*.docx")
            txt = glob.glob("sourcedoc/" + str(subdir) + "/*.txt")
            if txt:
                txtCounter += txtConvert.con(txt, txtCounter, subdir)

            if odt:
                counter = odtConvert.con(odt, str(subdir)[:3].upper(), counter,subdir)

            if doc:
                counter = docConvert.con(doc, str(subdir)[:3].upper(), counter,subdir)
            print(counter)