import spacy

nlp = spacy.load("pt_core_news_sm")

def spacyTreatment(text):

    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_alpha]