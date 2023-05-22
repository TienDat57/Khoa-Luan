import spacy
sentence = 'A G-to-A transition at the first nucleotide of intron 2 of patient 1 abolished normal splicing.'
nlp = spacy.load('en_core_web_sm')
doc = nlp(sentence)
for token in doc:
   print(
      f"""
TOKEN: {token.text}
=====
{token.tag_ = }
{token.head.text = }
{token.dep_ = }
{spacy.explain(token.dep_) = }""")
   
