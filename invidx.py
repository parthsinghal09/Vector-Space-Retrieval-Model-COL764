import os
import math
import string
import pickle
import xml.etree.ElementTree as ET

def invidx_cons(collpath, indexfile):
    
    Dict = {}
    idx = {}
    
    indexfiledict = indexfile + ".dict"
    indexfileidx = indexfile + ".idx"

    tagw = set(["<LOCATION>", "<ORGANIZATION>", "<PERSON>"])
    tagw1 = set(["</LOCATION>", "</ORGANIZATION>", "</PERSON>"])
    
    puncs = set()
    for p in string.punctuation:
        puncs.add(p)
    
    filenames = os.listdir(collpath)
    for file in filenames:
        filename = os.path.join(collpath, file)
        with open(filename, 'r') as f1:
            data = f1.read()
        filen1 = file + "new1"
        filenamenew1 = filen1
        with open(filenamenew1,'w') as f2:
            f2.write("<root>")
        with open(filenamenew1,'a') as f3:
            f3.write("\n")
            f3.write(data)
            f3.write("\n")
            f3.write("</root>\n")       
        delete_list = ["&", "``", "`"]
        filen2 = file + "new2"
        filenamenew2 = filen2
        with open(filenamenew1) as f1, open(filenamenew2, "w+") as f2:
            for line in f1:
                for word in delete_list:
                    line = line.replace(word, "")
                f2.write(line)
        os.remove(filenamenew1)
        os.rename(filenamenew2, filenamenew1)
        with open(filenamenew1,'r') as f:
            root = ET.fromstringlist(f)
            Docs = root.getchildren()
        for ele in Docs:
            docID = ele.find("DOCNO").text
            docID = docID.strip()
            idx[docID] = {}
            text_tokens = []
            x = ET.tostring(ele.find("TEXT"))
            y = x.decode("ASCII")
            y = y.replace("<TEXT>", "")
            y = y.replace("</TEXT>", "")
            text_tokens1 = []
            for word in y.split():
                if word not in puncs:
                    if "</ORGANIZATION>" in word:
                        text_tokens1.append("</ORGANIZATION>")
                    elif "</ORGANISATION>" in word:
                        text_tokens1.append("</ORGANIZATION>")
                    elif "</PERSON>" in word:
                        text_tokens1.append("</PERSON>")
                    elif "</LOCATION>" in word:
                        text_tokens1.append("</LOCATION>")
                    elif "<ORGANIZATION>" in word:
                        text_tokens1.append("<ORGANIZATION>")
                    elif "<ORGANISATION>" in word:
                        text_tokens1.append("<ORGANIZATION>")
                    elif "<PERSON>" in word:
                        text_tokens1.append("<PERSON>")
                    elif "<LOCATION>" in word:
                        text_tokens1.append("<LOCATION>")
                    else:
                        for w1 in word:
                            if w1 in puncs:
                                word = word.replace(w1, "")
                        text_tokens1.append(word.lower())
            w = ""
            count = 0
            j = 0
            i = 0
            count1 = 0
            for words in text_tokens1:
                if i<len(text_tokens1):
                    s = text_tokens1[i]
                    if s in tagw:
                        if (i + 1)<len(text_tokens1):
                            j = i + 1
                            while(text_tokens1[j] not in tagw1):
                                if count == 0:
                                    w = text_tokens1[j]
                                    if w in Dict.keys():
                                        Dict[w].add(docID)
                                    else:
                                        Dict[w] = set([docID])
                                    if w in idx[docID].keys():
                                        idx[docID][w] = idx[docID][w] + 1
                                    else:
                                        idx[docID][w] = 1
                                else:
                                    w = w + " " + text_tokens1[j]
                                    if text_tokens1[j] in Dict.keys():
                                        Dict[text_tokens1[j]].add(docID)
                                    else:
                                        Dict[text_tokens1[j]] = set([docID])
                                    if text_tokens1[j] in idx[docID].keys():
                                        idx[docID][text_tokens1[j]] = idx[docID][text_tokens1[j]] + 1
                                    else:
                                        idx[docID][text_tokens1[j]] = 1 
                                count1 = count1 + 1
                                j = j + 1
                            i = j
                            if (i + 1)<len(text_tokens1):
                                if text_tokens1[i + 1] in tagw and text_tokens1[i + 1] == s:
                                    count = count + 1
                                else:
                                    if count1!=1:
                                        if w in Dict.keys():
                                            Dict[w].add(docID)
                                        else:
                                            Dict[w] = set([docID])
                                        if w in idx[docID].keys():
                                            idx[docID][w] = idx[docID][w] + 1
                                        else:
                                            idx[docID][w] = 1
                                    count1 = 0
                                    count = 0
                            else:
                                if count!=0:
                                    if w in Dict.keys():
                                        Dict[w].add(docID)
                                    else:
                                        Dict[w] = set([docID])
                                    if w in idx[docID].keys():
                                        idx[docID][w] = idx[docID][w] + 1
                                    else:
                                        idx[docID][w] = 1
                                count = 0
                        else:
                            break;
                    elif s not in tagw and s not in tagw1:
                        count = 0
                        count1 = 0
                        if s in Dict.keys():
                            Dict[s].add(docID)
                        else:
                            Dict[s] = set([docID])
                        if s in idx[docID].keys():
                            idx[docID][s] = idx[docID][s] + 1
                        else:
                            idx[docID][s] = 1
                else:
                    break;
                i = i + 1
    d1_file = open(indexfiledict, "wb")
    pickle.dump(Dict, d1_file)
    d1_file.close()
    
    d2_file = open(indexfileidx, "wb")
    pickle.dump(idx, d2_file)
    d2_file.close()

def main():
	collpath = input("Enter collpath: ")
	indexfile = input("Enter indexfile: ")
	invidx_cons(collpath, indexfile)

if __name__=="__main__": 
	main() 