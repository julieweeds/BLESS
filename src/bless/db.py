__author__ = 'juliewe'
#read in BLESS.txt, store in db and write to different file formats for different evaluations

import sys,json,random,math,conf

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


    def getRel(self,relation):
        if relation == "hyper":
            return self.hypers
        elif relation == "coord":
            return self.coords
        elif relation == "mero":
            return self.meros
        elif relation == "random-n":
            return self.randoms
        else:
            print "Warning: ignoring unknown relation "+relation
            return []


    def writecache(self,outstream,rels):

        for rel in rels:
            neighs=self.getRel(rel)
            for neigh in neighs:
                outstream.write(self.word+"-n\t"+self.group+"\t"+rel+"\t"+neigh+"\n")


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
    thesdir=datadir
    blessfile="BLESS"
    countfile="entries_t10.strings"

    def __init__(self,parameters):
        self.filter=parameters.get("filter",False)
        self.usecache=parameters.get("blesscache",False)
        self.correlate=parameters.get("correlate",False)
        self.entrydict={}
        self.entList=[]
        self.countdict={}
        self.discards=[]
        self.blessfile=blessDB.datadir+blessDB.blessfile
        self.countfile=blessDB.thesdir+blessDB.countfile
        if self.usecache:
            self.infile=self.blessfile+".cache"
            self.filter=False
        else:
            self.infile=self.blessfile+".txt"

        if self.filter or self.correlate:
            self.readtotals()

        self.readfile()

    def readtotals(self):
        #read freq info
        instream=open(self.countfile,'r')
        print "Reading "+self.countfile
        linesread=0
        for line in instream:
            fields=line.rstrip().split('\t')
            if len(fields) < 2:
                print "Discarding line "+line+" : "+str(len(fields))
            else:
                fields[0]=untag(fields[0],'/')
                if len(fields)==2:
                    self.countdict[fields[0]]=fields[1]
                else:
                    self.countdict[fields[0]]=(fields[1],fields[2])
            linesread+=1
        print "Read "+str(linesread)+" lines"
        print "Size of countdict is "+str(len(self.countdict))
        instream.close()

    def filtercheck(self,word):
        if self.filter:
            if word in self.countdict.keys():
                return True
            else:
                return False
        else:
            return True

    def readfile(self):
        #read pair info
        print "Reading "+self.infile
        with open(self.infile,'r') as instream:
            linesread=0
            for line in instream:
                line=line.rstrip()
                fields=line.split('\t')
                if len(fields) != 4:
                    print "Warning: invalid line format "+line
                else:
                    fields[0]=untag(fields[0],'-')
                    fields[0]=fields[0].lower()
                    if self.filtercheck(fields[0]):
                        fields[3]=untag(fields[3],'-')
                        fields[3]=fields[3].lower()
                        if fields[0] not in self.entrydict.keys():
                            self.entrydict[fields[0]] = Entry(fields[0],fields[1])
                        if fields[2] in blessDB.knownRels and self.filtercheck(fields[3]):
                            self.entrydict[fields[0]].addRel(fields[2],fields[3])
                    else:
                        if fields[0] not in self.discards:
                            self.discards.append(fields[0])
                linesread+=1
                if linesread %1000 == 0:
                    print "Read "+str(linesread)+" lines, number of discarded concepts = "+str(len(self.discards))
        if self.filter:
            self.writecache()

    def printstats(self):
        print "Size of entrydict is "+str(len(self.entrydict))



    def writecache(self):
        outfile=self.blessfile+".cache"
        print "Caching BLESS file from filter: "+outfile
        with open(outfile,'w') as outstream:
            for entry in self.entrydict.values():
                entry.writecache(outstream,blessDB.knownRels)

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
        outfile=self.blessfile+"_ent-pairs.json"
        print "Writing "+outfile
        with open(outfile,'w') as outstream:
            json.dump(self.entList,outstream)

    def genSim(self):
        outfile=self.blessfile+"_simlists.txt"
        print "Writing "+outfile
        with open(outfile,'w') as outstream:
            entrycount=0
            paircount=0
            for entry in self.entrydict.values():
                outstream.write(entry.word+'/N')
                for hyper in entry.hypers:
                    outstream.write('\t'+hyper+'/N')
                    paircount+=1
                for coord in entry.coords:
                    outstream.write('\t'+coord+'/N')
                    paircount+=1
                for mero in entry.meros:
                    outstream.write('\t'+mero+'/N')
                    paircount+=1
                outstream.write('\n')
                entrycount+=1
        print "Number of entry lines written is "+str(entrycount)
        print "Total number of similarity pairs is "+str(paircount)
        print "BLESS concepts discarded are "
        print self.discards

if __name__ == "__main__":
    ###configuration
    parameters=conf.configure(sys.argv)
    ####initialization
    blessDB.datadir=parameters["datadir"]
    if parameters["thes_override"]:
        blessDB.thesdir=parameters["thesdir"]
        blessDB.countfile=parameters["countfile"]
    myBless=blessDB(parameters["filter"])
    myBless.printstats()

    ###run appropriate methods
    if parameters["entail"]:
        myBless.genEntail()
    if parameters["sim"]:
        myBless.genSim()
