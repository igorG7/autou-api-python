import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

nlp = spacy.load("pt_core_news_sm")
keywords = {"sistema", "suporte"}

def spacyTreatment(text):

    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_alpha]