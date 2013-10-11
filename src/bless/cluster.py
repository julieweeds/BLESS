__author__ = 'Julie'

from thesaurus import Thesaurus
import conf, sys, os, json

if __name__=="__main__":

    parameters=conf.configure(sys.argv)

    inputfile="allBLESS-dependencies.json"
    inputpath=os.path.join(parameters['datadir'],inputfile)
    print inputpath
    with open(inputpath,'r') as instream:
        for line in instream:
            print line

    pairs = json.loads(inputpath)

    cluster0=[]
    cluster1=[]
    for (w1,w2,target) in pairs:
        if target==1:
            cluster1.append(w2)
        else:
            cluster0.append(w2)

    print len(cluster0), cluster0
    print len(cluster1),cluster1
    exit()


    words=["chicken","cricket","jaguar"]
    pos="N"

    mythes = Thesaurus("",parameters["simfile"],True,False,parameters["k"],1,1,False)
    mythes.readsomesims(words)
    for word in words:
        mythes.displayneighs((word,pos),100)