import spacy


def word_revert(word: str) -> str:
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(word)  # 示例句子
    for token in doc:
        return token.lemma_
