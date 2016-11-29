import numpy as np
import os
import sys
import argparse
from urllib.request import urlopen
import ast
import xml.etree.ElementTree as ET
import unittest

__all__ = ['calculate']

def calculate(query,return_float=False,output=False):
    try:
        answer = eval(query,{})
        if return_float == True:
            result = float(answer)
        else:
            result = str(answer)
    except:
        query = '%20'.join(query.split())
        result = ET.fromstring(urlopen('http://api.wolframalpha.com/v2/query?input='\
                                        +query+'&appid=UAGAWR-3X6Y8W777Q').read())
        for pod in result.findall('.//pod'):
            if pod.attrib['title'] == 'Result' or pod.attrib['title'] == 'Value':
                answer = pod.findall('.//plaintext')[0].text
        if return_float == True:
            # parse wolframalpha plaintext
            answer = answer.split()
            if '^' in answer[0]:
                coeff = answer[0][:answer[0].find('^')-3]
                exp = answer[0][answer[0].find('^')+1:answer[0].find('^')+3]
                answer[0] = coeff+'e'+exp
            answer = float(answer[0])
        else:
            answer = str(answer)
    print(answer)
    if output == True:
        return answer

class MyTestCase(unittest.TestCase):
            
    def test_1(self):
        # Test normal eval
        self.assertAlmostEqual(calculate('8*8',return_float=True,output=True),64.0)

    def test_2(self):
        # Test eval isn't too strong
        with self.assertRaises(Exception):
            calculate("os.system('echo this_is_to_far')")
    
    def test_3(self):
        # Test numeric floats from WolframAlpha
        self.assertIsInstance(calculate("mass of earth",return_float=True,output=True),float)
    
    def test_4(self):
        # Test random strings from WolframAlpha
        self.assertIsInstance(calculate("author of harry potter",output=True),str)
        
    def test_5(self):
        # Test numeric strings from Wolfram Alpha
        self.assertIsInstance(calculate("mass of earth",output=True),str)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CalcCalc.calculate')
    parser.add_argument('query', help='This argument is the string that is to be evaluated by calculate')
    parser.add_argument('-f', action='store_true', default=False, dest='return_float', help='return float if set, default is return string')
    results = parser.parse_args()

    calculate(results.query,return_float=results.return_float)
