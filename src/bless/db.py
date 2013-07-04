__author__ = 'juliewe'
#read in BLESS.txt, store in db and write to different file formats for different evaluations

import sys,json,random,math

def untag(word,d):
    parts=word.split(d)
    res=parts[0]
    if(len(parts)>2):
        for part in parts[1:len(parts)-1]:
            res=res+'-'+part
        #print res
    return res

class Entry:

    relratio=0.2

    def __init__(self,word,group=""):
        self.word=word
        self.group=group
        self.hypers=[]
        self.coords=[]
        self.randoms=[]
        self.meros=[]
        self.hypos=[]
        self.zeros=[]



    def addRel(self,relation,word):
        if relation == "hyper":
            self.hypers.append(word)
        elif relation == "coord":
            self.coords.append(word)
        elif relation == "mero":
            self.meros.append(word)
        elif relation == "random-n":
            self.randoms.append(word)
        else:
            print "Warning: ignoring unknown relation "+relation

    def makehypos(self):
        random.shuffle(self.hypers)
        d= int(math.ceil(Entry.relratio*len(self.hypers)))
        self.hypos=self.hypers[0:d]
        self.hypers=self.hypers[d:len(self.hypers)]
        #print self.hypos,self.hypers

    def makezeros(self):
        self.makehypos()
        random.shuffle(self.coords)
        random.shuffle(self.randoms)
        random.shuffle(self.meros)
        self.others=self.coords[0:len(self.hypos)]+self.randoms[0:len(self.hypos)]+self.meros[0:len(self.hypos)]
        for hypo in self.hypos:
            self.zeros.append([hypo,self.word,0])
        for other in self.others:
            if len(self.zeros)%2==0:
                self.zeros.append([self.word,other,0])
            else:
                self.zeros.append([other,self.word,0])
        random.shuffle(self.zeros)

class blessDB:

    knownRels=["coord","hyper","mero","random-n"]

    datadir="/Volumes/LocalScratchHD/juliewe/Documents/workspace/BLESS/data/"
    blessfile=datadir+"BLESS"
    countfile=datadir+"entries_t10.strings"

    def __init__(self):
        self.entrydict={}
        self.entList=[]
        self.countdict={}
        self.discards=[]

        self.readtotals()
        self.readfile()

    def readtotals(self):
        #read freq info
        instream=open(blessDB.countfile,'r')
        print "Reading "+blessDB.countfile
        linesread=0
        for line in instream:
            fields=line.rstrip().split('\t')
            if len(fields) < 2:
                print "Discarding line "+line+" : "+str(len(fields))
            else:
                fields[0]=untag(fields[0],'/')
                self.countdict[fields[0]]=fields[1]
            linesread+=1
        print "Read "+str(linesread)+" lines"
        print "Size of countdict is "+str(len(self.countdict))
        instream.close()


    def readfile(self):
        #read pair info
        with open(blessDB.blessfile+'.txt','r') as instream:
            linesread=0
            for line in instream:
                line=line.rstrip()
                fields=line.split('\t')
                if len(fields) != 4:
                    print "Warning: invalid line format "+line
                else:
                    fields[0]=untag(fields[0],'-')
                    if fields[0] in self.countdict.keys():
                        fields[3]=untag(fields[3],'-')
                        if fields[0] not in self.entrydict.keys():
                            self.entrydict[fields[0]] = Entry(fields[0],fields[1])
                        if fields[2] in blessDB.knownRels and fields[3] in self.countdict.keys():
                            self.entrydict[fields[0]].addRel(fields[2],fields[3])
                    else:
                        if fields[0] not in self.discards:
                            self.discards.append(fields[0])
                linesread+=1
                if linesread %1000 == 0:
                    print "Read "+str(linesread)+" lines"


    def printstats(self):
        print "Size of entrydict is "+str(len(self.entrydict))


    def genEntail(self):

        self.entList=[]
        count=0
        for entry in self.entrydict.values():
            #print entry
            #print entry.word,entry.group
            entry.makezeros()
            for hyper in entry.hypers:
                self.entList.append([entry.word,hyper,'1'])
                count+=1
            for triple in entry.zeros:
                if count>0:
                    if triple not in self.entList:
                        self.entList.append(triple)
                        count-=1
        print self.entList
        print "Number of pairs is "+str(len(self.entList))
        print "BLESS concepts discarded are "
        print self.discards
        outfile=blessDB.blessfile+"_ent-pairs.json"
        with open(outfile,'w') as outstream:
            json.dump(self.entList,outstream)


if __name__ == "__main__":
    myBless=blessDB()
    myBless.printstats()
    if "entail" in sys.argv:
        myBless.genEntail()
