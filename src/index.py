from xml.dom import minidom
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import pandas as pd

PATH_DATA = '../data'

# read xml file
def read_xml_file(xml_file):
   # parse an xml file by name
   mydoc = minidom.parse(PATH_DATA + '/' + xml_file)

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
   
   
   print('predicate: ', predicate)
   print('roleset: ', roleset)
   print('text: ', text)
   print('example: ', example)
   
      

read_xml_file('abolish_full.xml')
