from xml.dom import minidom
import pandas as pd

# get home path contain all Khoa-luan files

PATH_DATA = '../../dataset/'

# create class to preprocess data
class Preprocessing:
   def __init__(self, file_name):
      self.file_name = file_name
      self.data = None
      self.output_data = PATH_DATA + 'interim/' + file_name
      
   def read_xml_file(self):
      # parse an xml file by name
      mydoc = minidom.parse(PATH_DATA + 'raw/' + self.file_name)

      # DOM predicates
      predicate = mydoc.getElementsByTagName('predicate')
      predicate = [predicate[i].attributes['lemma'].value for i in range(len(predicate))]

      # get all the roleset in the xml file
      roleset = mydoc.getElementsByTagName('roles')
      roleset = [roleset[i].getElementsByTagName('role') for i in range(len(roleset))]
      roleset = [[roleset[i][j].attributes['descr'].value for j in range(len(roleset[i]))] for i in range(len(roleset))]
      
      # get all the examples in the xml file
      example = mydoc.getElementsByTagName('example')
      text = [example[i].getElementsByTagName('text')[0].firstChild.data for i in range(len(example))]
      example = [example[i].getElementsByTagName('arg') for i in range(len(example))]
      example = [[example[i][j].firstChild.data for j in range(len(example[i]))] for i in range(len(example))]
      
      self.data = pd.DataFrame({'predicate': predicate, 'roleset': roleset, 'text': text, 'example': example})
      return self.data
      

# test
pre = Preprocessing('abolish_full.xml')
data = pre.read_xml_file()
print(data.head())
