import pandas as pd
from xml.dom import minidom

PATH_DATA = '../../dataset/'

# create class to preprocess data
class Preprocessing:
   def __init__(self, file_name):
      self.file_name = file_name
      self.data_arg = None
      self.data_role = None
      self.output_data = PATH_DATA + 'interim/' + file_name.split('.')[0] + '.csv'
      
   def read_xml_file(self):
      # parse an xml file by name
      mydoc = minidom.parse(PATH_DATA + 'raw/' + self.file_name)
      
      # Get the examples from the XML
      examples = mydoc.getElementsByTagName('example')
      
      # Create empty lists to store the data
      ids = [i for i in range(len(examples))]
      srcs = []
      texts = []
      arg0s = []
      arg1s = []
      
      # Iterate over each example and extract the required information
      for example in examples:
         text = example.getElementsByTagName('text')[0].firstChild.nodeValue
         src = example.getAttribute('src')
         arg0 = example.getElementsByTagName('arg')[0].firstChild.nodeValue
         arg1 = example.getElementsByTagName('arg')[1].firstChild.nodeValue
         
         # Append the extracted data to the respective lists
         texts.append(text)
         srcs.append(src)
         arg0s.append(arg0)
         arg1s.append(arg1)
      
      # Create the data frame
      data_arg = pd.DataFrame({
         'id': ids,
         'src': srcs,
         'text': texts,
         'arg0': arg0s,
         'arg1': arg1s
      })
      
      self.data_arg = data_arg


preprocessor = Preprocessing('abolish_full.xml')
preprocessor.read_xml_file()
data_arg = preprocessor.data_arg
data_arg.to_csv(preprocessor.output_data, index=False)
