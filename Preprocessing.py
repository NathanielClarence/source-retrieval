import re
from string import digits
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def process(txtString):
    factory = StopWordRemoverFactory()
    stopwords = factory.create_stop_word_remover()

    remove_digits = str.maketrans('','',digits)
    doc = txtString.translate(remove_digits)
    doc = re.sub('[^A-Za-z0-9]+', ' ', doc)
    doc = doc.lower()

    return stopwords.remove(doc)