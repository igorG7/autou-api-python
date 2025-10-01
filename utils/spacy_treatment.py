
import spacy
nlp = spacy.load("pt_core_news_sm")

def spacyTreatment(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]