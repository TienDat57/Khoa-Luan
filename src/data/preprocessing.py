import pandas as pd
from xml.dom import minidom
import spacy

PATH_DATA = '../../dataset/'

# create class to preprocess data
class Preprocessing:
   def __init__(self, file_name):
      self.file_name = file_name
      self.data_arg = None
      self.predicate = None
      self.data_role = None
      self.min_threshold = 0.1
      self.output_data = PATH_DATA + 'interim/' + file_name.split('.')[0] + '.csv'
      
   def read_xml_file(self):
      mydoc = minidom.parse(PATH_DATA + 'raw/' + self.file_name)
      self.predicate = mydoc.getElementsByTagName('predicate')[0].getAttribute('lemma')
      examples = mydoc.getElementsByTagName('example')
      ids = [i for i in range(len(examples))]
      srcs, texts, args = [], [], []
      for example in examples:
         text = example.getElementsByTagName('text')[0].firstChild.nodeValue
         src = example.getAttribute('src')
         arg_temp = []
         for arg in example.getElementsByTagName('arg'):
            arg_temp.append(arg.firstChild.nodeValue)
         texts.append(text)
         srcs.append(src)
         args.append(arg_temp)
      data_arg = pd.DataFrame({'id': ids, 'source': srcs, 'text': texts, 'arguments': args})
      self.data_arg = data_arg
      
   def __remove_example__(self, index):
      self.data_arg.drop(index, inplace=True)
      self.data_arg.reset_index(drop=True, inplace=True)
      
   def dependency_parsing(self):
      def print_dependency_parsing(token):
         print(
            f"""
               TOKEN: {token.text}
               =====
               {token.tag_ = }
               {token.head.text = }
               {token.dep_ = }
               {spacy.explain(token.dep_) = }""")
      
      # count_args = [0 for i in range(len(self.data_arg['arguments'][0]))]
      nlp = spacy.load('en_core_web_sm')
      for i in range(len(self.data_arg)):
         doc = nlp(self.data_arg['text'][i])
         root = [token for token in doc if token.head == token][0]
         for token in doc:
            for j in range(len(self.data_arg['arguments'][i])):
               if token.text in self.data_arg['arguments'][i][j] and token.head.text == root.text:
                  # print(self.data_arg['arguments'][i][j])
                  # count_args[j] += 1
                  print('hello')

# preprocessor = Preprocessing('abolish_full.xml')
# preprocessor.read_xml_file()
# data_arg = preprocessor.data_arg
# data_arg.to_csv(preprocessor.output_data, index=False)
# preprocessor.dependency_parsing()

import os
filenames = os.listdir(PATH_DATA + 'raw')
for filename in filenames:
   print(filename)
