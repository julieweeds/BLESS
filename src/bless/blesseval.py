__author__ = 'Julie'

import thesaurus,conf,sys
from db import blessDB, untag

class BlessThes(thesaurus.Thesaurus):

    metric="lin"
    thesaurus.Thesaurus.byblo=True

    def __init__(self,simcachefile,k):
        #create basic Thesaurus
        thesaurus.Thesaurus.__init__(self,"",simcachefile,True,False,k,1,1,False)



    def allsims(self,entrylist):
        print"Reading sim file "+self.simcachefile
        linesread=0
        instream=open(self.simcachefile,'r')
        for line in instream:
            if untag(line.split('\t')[0],'/') in entrylist:#check this is a word in blessDB
                self.processsimline(line.rstrip())
            linesread+=1
            if (linesread%1000 == 0):
                print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" similarity vectors"
                sys.stdout.flush()
                #return
        self.topk(self.k)
        print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" vectors"
        instream.close()


def gettopsim(self,wordlist):
        #return rank and sim of nearest neighbour in wordlist
        return
if __name__== "__main__":
    parameters=conf.configure(sys.argv)

    if parameters["thes_override"]:
        blessDB.thesdir=parameters["thesdir"]
        blessDB.countfile=parameters["countfile"]

    blessDB.datadir=parameters["datadir"]
    print "Loading blessDB from "+blessDB.datadir
    print "Filter file is "+blessDB.thesdir+blessDB.countfile
    print "Filter applied: "+str(parameters["filter"])
    myBless=blessDB(parameters["filter"])
    print "Created blessDB"
    myBless.printstats()
    print "Loading thesaurus with parameters "+parameters["simfile"]+" k = "+str(parameters["k"])
    myThes=BlessThes(parameters["simfile"],parameters["k"])
    myThes.allsims(myBless.entrydict.keys())

    ##test##
    for concept in myBless.entrydict.keys():
        myThes.displayneighs((concept,'N'),10)