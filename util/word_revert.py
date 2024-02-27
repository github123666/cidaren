import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

def word_revert(word: str) -> str:
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(word)
    for token in doc:
        return token.lemma_


if __name__ == '__main__':
    print(word_revert('underwent'))
