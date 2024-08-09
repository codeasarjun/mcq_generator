import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

class MCQ:
    def __init__(self, ques, choices, correct_ans):
        self.ques = ques
        self.choices = choices
        self.correct_ans = correct_ans

    def to_dict(self):
        return {
            'ques': self.ques,
            'choices': self.choices,
            'correct_ans': self.correct_ans
        }

def process_text(txt):
    txt = txt.lower().replace('\n', ' ').strip()

    doc = nlp(txt)
    sentences = [sent.text for sent in doc.sents]

    def clean_text(text):
        cleaned_text = []
        for token in nlp(text):
            if not token.is_stop and not token.is_punct and not token.text.isdigit():
                cleaned_text.append(token.lemma_)
        return " ".join(cleaned_text)

    filtered_sentences = [clean_text(sent) for sent in sentences]

    vectorizer = TfidfVectorizer(min_df=2, max_df=0.8, ngram_range=(1, 2))
    vectorized_sentences = vectorizer.fit_transform(filtered_sentences)

    feat_names = vectorizer.get_feature_names_out()
    scores = [vectorizer.idf_[vectorizer.vocabulary_.get(word)] for word in feat_names]

    sorted_indices = np.argsort(scores)[::-1]
    feat_names_sorted = [feat_names[i] for i in sorted_indices]

    num_ques = 3
    mcqs = feat_names_sorted[:num_ques]

    questions = []

    for mcq in mcqs:
        for doc in filtered_sentences:
            if mcq in doc:
                fil_index = filtered_sentences.index(doc)
                for token in nlp(sentences[fil_index]):
                    if not token.is_stop and not token.is_punct and token.lemma_ == mcq:
                        correct_ans = token.text
                        ques = sentences[fil_index].replace(token.text, "____", 1).capitalize()

                        choices = set()
                        while len(choices) < 3:
                            option = np.random.choice(feat_names_sorted, 1, replace=False)[0]
                            if option not in choices and option != correct_ans:
                                choices.add(option)
                        choices.add(correct_ans)

                        choices = list(choices)
                        np.random.shuffle(choices)

                        choices_dict = dict(zip('abcd', choices))
                        correct_letter = [key for key, value in choices_dict.items() if value == correct_ans][0]

                        ques_object = MCQ(ques, choices_dict, correct_ans)
                        if not any(q.ques == ques_object.ques for q in questions):
                            questions.append(ques_object)

    return [q.to_dict() for q in questions]  # Convert to dict for easier handling
