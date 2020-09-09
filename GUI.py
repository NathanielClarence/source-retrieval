import tkinter
import mergePostingList
import convertAll
import FindSourceDoc
import os
import glob
import ParseXML
import DuplicateSearch
import GlobalFunctions as g
import ntpath
import matplotlib.pyplot as plt

class Application(tkinter.Frame):
    def __init__(self,master=None,):
        super().__init__(master)
        self.master = master

        self.convertdoc = tkinter.Button(text="Convert Documents",command = self.convertDocs, width = 20)
        self.convertdoc.grid(row=0, column=0, padx=25,pady=(20,10), columnspan=2)

        self.libupdate = tkinter.Button(text="Update Posting List", command=self.UpdateLibrary, width=20)
        self.libupdate.grid(row=0, column=2, padx=25, pady=(20,10), columnspan=2)

        self.findsource = tkinter.Button(text="Find Source Document",command = self.findSourceDoc, width = 20)
        self.findsource.grid(row=1, column=0, pady=10, padx = 25, columnspan=2)

        self.finddupes = tkinter.Button(text="Find Duplicates in Source", command=self.findDuplicates, width=20)
        self.finddupes.grid(row=1, column=2, pady=10, padx=25, columnspan=2)

        tkinter.Label(text= "Document Filter:").grid(row=2, column=0, padx=(15, 0))
        tkinter.Label(text="Document Category:").grid(row=2, column=2)

        self.filtervar = tkinter.StringVar(tkinter.Toplevel(root))
        self.filtervar.set(filteropt[0])
        self.ffvar = tkinter.OptionMenu(master, self.filtervar, *filteropt)
        self.ffvar.config(width=5)
        self.ffvar.grid(row=2, column=1, pady=10, sticky='w')

        self.docvar = tkinter.StringVar(tkinter.Toplevel(root))
        self.docvar.set(fileopt[0])
        self.ddocvar = tkinter.OptionMenu(master, self.docvar, *fileopt)
        self.ddocvar.config(width=8)
        self.ddocvar.grid(row=2, column=3, pady=10, sticky = 'w',padx=(0, 15))

        self.sourceretrieve = tkinter.Button(text = "Evaluate Test Document", command=lambda : simul(int(self.filtervar.get()), self.docvar.get()), width=20)
        self.sourceretrieve.grid(row = 3, column = 2, pady = 10, padx =25, columnspan=2)

        #self.findartificial = tkinter.Button(text="Test Artificial", command=self.artificialZero, width=20)
        #self.findartificial.grid(row=2, column=0, pady=10, padx=25)

        #self.findsimulated = tkinter.Button(text="Test Simulated", command=self.simulatedZero, width=20)
        #self.findsimulated.grid(row=2, column=1, pady=10, padx=25)

        #self.findartificial5 = tkinter.Button(text="Test Artificial Filter 5", command=self.artificialSource, width=20)
        #self.findartificial5.grid(row=3, column=0, pady=10, padx=25)

        #self.findsimulated5 = tkinter.Button(text="Test Simulated Filter 5", command=self.simulatedSource, width=20)
        #self.findsimulated5.grid(row=3, column=1, pady=10, padx=25)

        #self.findartificial10 = tkinter.Button(text="Test Artificial Filter 10", command=self.artificialTen, width=20)
        #self.findartificial10.grid(row=4, column=0, pady=10, padx=25)

        #self.findsimulated10 = tkinter.Button(text="Test Simulated Filter 10", command=self.simulatedTen, width=20)
        #self.findsimulated10.grid(row=4, column=1, pady=10, padx=25)

        self.quit = tkinter.Button(text="QUIT", fg='red', command=self.master.destroy)
        self.quit.grid(row=4, column=0,pady=(10,20),columnspan =4)

    def convertDocs(self):
        updated = tkinter.Toplevel(root)
        updated.resizable(0, 0)
        convertAll.run()
        tkinter.Label(updated, text="Documents Converted").grid(column=0, row=0, padx=20, pady=10)
        tkinter.Button(updated, text="OK", command=updated.destroy).grid(column = 0, row = 1, pady =10)
        updated.grab_set()

    def UpdateLibrary(self):
        updated = tkinter.Toplevel(root)
        updated.resizable(0, 0)
        mergePostingList.run(root)
        tkinter.Label(updated, text="Posting List Updated").grid(column=0, row=0, padx=20, pady=10)
        tkinter.Button(updated, text="OK", command=updated.destroy).grid(column=0, row=1, pady=10)
        updated.grab_set()

    def findSourceDoc(self):
        root.filename = tkinter.filedialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),title = "Select file to search",
                                                           filetypes = (("txt files","*.txt"),("all files","*.*")))

        if root.filename == '':
            print("cancelled")
        else:
            srcCandidate, dupl = FindSourceDoc.run(root.filename, root,filter = False, filamt=0)
            try:
                ParseXML.run(root.filename)
            except:
                print("already in annotation")

            dicc = g.openResult('output/annotation.csv')

            annoSource = dicc.get(ntpath.basename(root.filename[:-4]))[0]
            annoDup = dicc.get(ntpath.basename(root.filename[:-4]))[1]

            p, r, f = g.allmeasure(srcCandidate, dupl, annoSource, annoDup)
            print(p)
            print(r)
            print(f)
            result = tkinter.Toplevel(root)
            result.minsize(200, 200)
            result.title("Evaluation " + ntpath.basename(root.filename))
            tkinter.Label(result, text="Precision ").grid(row=0, column=0, padx=3)
            tkinter.Label(result, text="Recall ").grid(row=1, column=0, padx=3)
            tkinter.Label(result, text="F1 Score ").grid(row=2, column=0, padx=3)
            tkinter.Label(result, text=round(p,3)).grid(row=0, column=1, padx=3)
            tkinter.Label(result, text=round(r,3)).grid(row=1, column=1, padx=3)
            tkinter.Label(result, text=round(f,3)).grid(row=2, column=1, padx=3)

    def findDuplicates(self):
        updated = tkinter.Toplevel(root)
        updated.resizable(0, 0)
        DuplicateSearch.runANew()
        tkinter.Label(updated, text="Duplicates Checked").grid(column=0, row=0, padx=20, pady=10)
        tkinter.Button(updated, text="OK", command=updated.destroy).grid(column=0, row=1, pady=10)
        updated.grab_set()

    #def artificialSource(self):
    #    file = glob.glob("testdoc/artificialFile/*.txt")
    #    simul(5, file)

    #def artificialZero(self):
    #    file = glob.glob("testdoc/artificialFile/*.txt")
    #    simul(0, file)

    #def artificialTen(self):
    #    file = glob.glob("testdoc/artificialFile/*.txt")
    #    simul(10, file)

    #def simulatedSource(self):
    #    file = glob.glob("testdoc/simulatedFiles/*.txt")
    #    simul(5, file)

    #def simulatedZero(self):
    #    file = glob.glob("testdoc/simulatedFiles/*.txt")
    #    simul(0, file)

    #def simulatedTen(self):
    #    file = glob.glob("testdoc/simulatedFiles/*.txt")
    #    simul(10, file)

def simul(filteramt, file):
    if file == "Simulated":
        file = glob.glob("testdoc/simulatedFiles/*.txt")
    else:
        file = glob.glob("testdoc/artificialFile/*.txt")

    #print(file)
    #print(filteramt)

    precision = []
    recall = []
    F1 = []
    docname = []
    count = 0
    for fi in file:
        count += 1
        docname.append(count)
        if fi == '':
            print('cancelled')
        else:
            if filteramt == 0:
                srcCandidate, dupl = FindSourceDoc.run(fi, root, show=False, filter = False, filamt=0)
            else:
                srcCandidate, dupl = FindSourceDoc.run(fi, root, show=False, filamt=filteramt)
            try:
                ParseXML.run(fi)
            except:
                print("already in annotation")
            dicc = g.openResult('output/annotation.csv')

            annoSource = dicc.get(ntpath.basename(fi[:-4]))[0]
            annoDup = dicc.get(ntpath.basename(fi[:-4]))[1]

            p, r, f = g.allmeasure(srcCandidate, dupl, annoSource, annoDup)
            precision.append(p)
            recall.append(r)
            F1.append(f)

    plt.subplot(2, 2, 1)
    plt.bar(docname, precision)
    plt.title('Precision = ' + str(round(sum(precision) / len(precision), 3)))
    plt.ylim(top=1.05)

    plt.subplot(2, 2, 2)
    plt.bar(docname, recall)
    plt.title('Recall = ' + str(round(sum(recall) / len(recall), 3)))
    plt.ylim(top=1.05)

    plt.subplot(2, 2, 3)
    plt.bar(docname, recall)
    plt.title('F1 Score = ' + str(round(sum(F1) / len(F1), 3)))
    plt.ylim(top=1.05)

    plt.subplots_adjust(hspace=0.3)
    plt.show()

filteropt = ['0','1','2','3','4','5','6','7','8','9','10']
fileopt = ["Simulated", "Artificial"]

root = tkinter.Tk()
app = Application(master=root)
root.resizable(0,0)
root.minsize(200,100)

app.pack_propagate(0)
app.mainloop()
