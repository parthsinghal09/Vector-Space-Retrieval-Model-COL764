# Vector-Space-Retrieval(VSM)-Model
All the three codes(invidx_cons.py, printdict.py and vecsearch.py) make use of the following basic python libraries/packages - os, string, math, pickle and xml.etree.ElementTree

The programs are to be executed in the following order - invidx_cons.py --> printdict.py --> vecsearch.py

invidx.py 
- python program with the help of which inverted index files are generated
- it outputs two binary files 
  1.) indexfile.dict - contains a dictionary with keys as uniques words present in all the documents and values as list containing the document IDs of the documents in which the key is present
  2.) indexfile.idx - contains a dictionary with keys as unique document IDs and values as dictionaries(containing keys as words present in the document and values as the term frequency f of the key)
- function invidx_cons present inside this file takes user input for the path of the directory conatining the collection files and the name of indexfile that has to be saved
- upon executing the program, the console will show the user the dialogue, "Enter collpath: ", upon which the path of the folder conatining the collection files has to be entered
- after successfully giving the path to the folder containing the collection files a new dialogue will be seen, "Enter indexfile: ", upon which the user as to input the path/name of the indexfile that has to be saved


printdict.py 
- prints the indexfile.dict file generated using invidx_cons.py in a human-readable sorted form to the screen
- parameter to this function is the binary file, indexfile.dict, generated using the invidx_cons.py program
- upon executing this program, the user will see a dialogue on the console, "Enter dictfile: ", upon which the user will have to input the path to the file indefile.dict generated using invidx_cons.py
- format on the screen(each line) -- "<indexterm>:<df>:<offset-to-its-postingslist-in-idx-file>"

vecsearch.py 
- this is the implementation of vector space retrieval model and makes use of the files indexfile.idx and indexfile.dict
- upon executing this program, the user will have to provide 5 inputs: 
  1.) queryfile - input the path to the queryfile, dialogue that will appear for this is "Enter queryfile: "
  2.) k - input the value of k, dialogue that will appear for this is "Enter k value: "
  3.) resultfile - input the path/name to the resultfile, dialogue that will appear for this is "Enter resultfile: "
  4.) indexfile.idx - input the path to the indexfile.idx generated using invidx_cons.py, dialogue that will appear for this is "Enter indexfile: "
  5.) indexfile.dict - input the path to the indexfile.dict generated using invidx_cons.py, dialogue that will appear for this is "Enter dictfile: "
- outputs a resultfile in the format(each line) -- "qid iter docno rank sim run id"

Report.pdf 
- algorithmic details documentation
