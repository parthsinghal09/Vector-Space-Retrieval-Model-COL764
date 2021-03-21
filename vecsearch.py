import os
import math
import string
import pickle
import xml.etree.ElementTree as ET

def vecsearch(queryfile, k, resultfile, indexfileidx, indexfiledict):
    
    d1_file = open(indexfiledict, "rb")
    Dict = pickle.load(d1_file)
    d1_file.close()
    
    lk = list(Dict.keys())
    lk.sort()
    
    d2_file = open(indexfileidx, "rb")
    idx = pickle.load(d2_file)
    d2_file.close()
    
    tagw = set(["L:", "N:", "O:", "P:"])
    
    puncs = set()
    for p in string.punctuation:
        puncs.add(p)
    N = len(idx)
    
    doc_m = {}
    for doc in idx.keys():
        tfidf = 0
        for w in idx[doc].keys():
            aa = 1 + math.log2(idx[doc][w])
            bb = math.log2(1 + N/len(Dict[w]))
            if aa>0:
                cc = aa*bb
            else:
                cc = 0
            tfidf = tfidf + cc**2
        tfidf = math.sqrt(tfidf)
        doc_m[doc] = tfidf
        
    qid = [] 
    data = []
    
    with open(queryfile) as f:
        for line in f:
            if "<num>" in line:
                s = line.strip()
                s = s.replace("<num>", "")
                s = s.replace("Number:", "")
                s = s.strip()
                if s[0] == "0":
                    s = s[1:]
                qid.append(s)
            elif "<title>" in line:
                s = line.strip()
                s = s.replace("<title>", "")
                s = s.replace("Topic:", "")
                s = s.strip()
                data.append(s)
        
    with open(resultfile, "w+") as f1:
        ij = 0
        for line in data:
            q_tf = {}
            k1 = int(k)
            score = {}
            s = line.strip()
            text_tokens1 = []
            for word in s.split():
                if word not in puncs:
                    if "L:" in word:
                        text_tokens1.append("L:")
                    elif "N:" in word:
                        text_tokens1.append("N:")
                    elif "O:" in word:
                        text_tokens1.append("O:")
                    elif "P:" in word:
                        text_tokens1.append("P:")
                    else:
                        if word[-1]!="*":
                            for w1 in word:
                                if w1 in puncs :
                                    word = word.replace(w1, "")
                            text_tokens1.append(word.lower())
                        elif word[-1] == "*":
                            for w1 in word:
                                if w1 in puncs:
                                    word = word.replace(w1, "")
                            pre = list(filter(lambda x: x.startswith(word), lk))
                            for wor in pre:
                                text_tokens1.append(wor.lower())
            x = set()
            m = 0
            n = 0
            ww = ""
            count = 0
            count1 = 0
            for word in text_tokens1:
                if m<len(text_tokens1):
                    ss = text_tokens1[m]
                    if ss in tagw:
                        if (m + 1)<len(text_tokens1):
                            n = m + 1
                            if count == 0:
                                ww = text_tokens1[n]
                                x.add(ww)
                                if ww in q_tf:
                                    q_tf[ww] = q_tf[ww] + 1
                                else:
                                    q_tf[ww] = 1
                            else:
                                ww = ww + " " + text_tokens1[n]
                                x.add(text_tokens1[n])
                                if text_tokens1[n] in q_tf:
                                    q_tf[text_tokens1[n]] = q_tf[text_tokens1[n]] + 1
                                else:
                                    q_tf[text_tokens1[n]] = 1
                            n = n + 1
                            count1 = count1 + 1
                            m = n
                            if m<len(text_tokens1):
                                if text_tokens1[m] in tagw:
                                    if text_tokens1[m] == ss:
                                        count = count + 1
                                    else:
                                        count = 0
                                else:
                                    if count1!=1:
                                        x.add(ww)
                                        if ww in q_tf:
                                            q_tf[ww] = q_tf[ww] + 1
                                        else:
                                            q_tf[ww] = 1
                                    count = 0
                                    count1 = 0
                            else:
                                if count!=0:
                                    x.add(ww)
                                count = 0
                        else:
                            break
                    elif ss not in tagw:
                        count = 0
                        count1 = 0
                        x.add(ss)
                        if ss in q_tf:
                            q_tf[ss] = q_tf[ss] + 1
                        else:
                            q_tf[ss] = 1
                        m = m + 1
                else:
                    m = m + 1
                    break
            q_m = 0
            for w in x:
                if w in Dict.keys():
                    df = len(Dict[w])
                    idf = math.log2(1 + N/df)
                    tfq = 1 + math.log2(q_tf[w])
                    dd = tfq*idf
                    setw = Dict[w]
                    for docs in setw:
                        if docs in score.keys():
                            tf = 1 + math.log2(idx[docs][w])
                            if tf>0:
                                xyz = (1 + math.log2(idx[docs][w]))*idf
                                score[docs] = score[docs] + xyz*dd 
                        else:
                            tf = 1 + math.log2(idx[docs][w])
                            if tf>0:
                                xyz = (1 + math.log2(idx[docs][w]))*idf
                                score[docs] = xyz*dd
                            else:
                                score[docs] = 0
                    q_m = q_m + dd**2
            
            q_m = math.sqrt(q_m)
                    
            for d in score.keys():
                rr = score[d]/(q_m*doc_m[d])
                score[d] = rr
                
            sorted_score = sorted(score.items(), key = lambda x: x[1], reverse = True)
            l1 = []
            l2 = []
            j = 0
            for i in sorted_score:
                l2.append(score[i[0]])
                if j>0 and abs(l2[j - 1] - l2[j])>pow(10, -9):
                    k1 = k1 - 1
                    if k1>0:
                        l1.append(i[0] + " " + "0 " + str(score[i[0]]))
                    else:
                        break
                else:
                    l1.append(i[0] + " " + "0 " + str(score[i[0]]))
                j = j + 1
            
            for e in l1:
                ee = qid[ij] + " " + "Q0 " + e + " abc"
                f1.write(ee)
                f1.write("\n")
            f1.write("\n")
            f1.write("\n")
            ij = ij + 1

def main():
	queryfile = input("Enter queryfile: ")
	k = input("Enter k value: ")
	resultfile = input("Enter resultfile: ")
	indexfileidx = input("Enter indexfile: ")
	indexfiledict = input("Enter dictfile: ")
	vecsearch(queryfile, k, resultfile, indexfileidx, indexfiledict)

if __name__=="__main__": 
	main() 