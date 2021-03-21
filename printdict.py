import os
import math
import string
import pickle
import xml.etree.ElementTree as ET

def printdict(indexfiledict):
    
    d_file = open(indexfiledict, "rb")
    Dict = pickle.load(d_file)
    d_file.close()
    
    sorted_d = sorted(Dict.keys())
    i = 0
    for w in sorted_d:
        s = w + ":" + str(len(Dict[w])) + ":" + str(i)
        print(s)
        i = i + 1

def main():
	indexfiledict = input("Enter dictfile: ")
	printdict(indexfiledict)

if __name__=="__main__": 
	main() 