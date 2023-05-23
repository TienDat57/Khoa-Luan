import pandas as pd
from xml.dom import minidom
import spacy
import os
from tqdm import tqdm

PATH_DATA = '../../dataset/'

# create class to preprocess data
class Preprocessing:
   def __init__(self, file_name):
      self.file_name = file_name
      self.data_arg = None
      self.predicate = None
      self.roles = []
      self.data_role = None
      self.min_threshold = 0.1
      self.output_data = PATH_DATA + 'interim/' + file_name.split('.')[0] + '.csv'
      
   def read_xml_file(self):
      mydoc = minidom.parse(PATH_DATA + 'raw/' + self.file_name)
      self.predicate = mydoc.getElementsByTagName('predicate')[0].getAttribute('lemma')
      self.roles = [role.getAttribute('descr') for role in mydoc.getElementsByTagName('role')]
      examples = mydoc.getElementsByTagName('example')
      ids = [i for i in range(len(examples))]
      srcs, texts, args = [], [], []
      for example in examples:
         text = example.getElementsByTagName('text')[0].firstChild.nodeValue
         src = example.getAttribute('src')
         # arg_temp = ["" for i in range(len(self.roles))]
         arg_temp = dict()
         for role in self.roles:
            arg_temp[role] = ""
         print(arg_temp)
         # print(arg_temp)
         for arg in example.getElementsByTagName('arg'):
            # arg_temp.append(arg.firstChild.nodeValue)
            arg_temp[int(arg.getAttribute('n')) - 1] = arg.firstChild.nodeValue
         texts.append(text)
         srcs.append(src)
         args.append(arg_temp)
      data_arg = pd.DataFrame({'id': ids, 'source': srcs, 'text': texts, 'arguments': args})
      self.data_arg = data_arg

   def __remove_argument__(self, index_role):
      print(index_role)
      if index_role < 0 or index_role >= len(self.roles):
         return
      for i in range(len(self.roles)):
         self.data_arg['arguments'][i].pop(index_role)
         
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
      
      max_len_arg = max([len(arg) for arg in self.data_arg['arguments']])
      count_args = [0 for i in range(max_len_arg)]
      nlp = spacy.load('en_core_web_sm')
      lst_index_remove = []
      for i in tqdm(range(len(self.data_arg))):
         doc = nlp(self.data_arg['text'][i])
         root = [token for token in doc if token.head == token][0]
         for token in doc:
            for j in range(len(self.data_arg['arguments'][i])):
               if token.text in self.data_arg['arguments'][i][j] and token.head.text == root.text:
                  count_args[j] += 1
      for j in range(len(count_args)):
         if count_args[j] < len(self.data_arg) * self.min_threshold:
            lst_index_remove.append(j)
      for index in sorted(lst_index_remove, reverse=True):
         self.__remove_argument__(index)


# filenames = os.listdir(PATH_DATA + 'raw')
# for filename in filenames:
#    print(filename)
#    preprocessor = Preprocessing(filename)
#    preprocessor.read_xml_file()
#    data_arg = preprocessor.data_arg
#    preprocessor.dependency_parsing()
#    data_arg.to_csv(preprocessor.output_data, index=False)

preprocessor = Preprocessing('alter_full.xml')
preprocessor.read_xml_file()
data_arg = preprocessor.data_arg
preprocessor.dependency_parsing()
data_arg.to_csv(preprocessor.output_data, index=False)