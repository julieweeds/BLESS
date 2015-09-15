__author__ = 'juliewe'
#Refactored 15/9/2015
#python representation of BLESS datafile

def untag(word,d):
    parts=word.split(d)
    res=parts[0]
    if(len(parts)>2):
        for part in parts[1:len(parts)-1]:
            res=res+d+part
        #print res
    return res

def getPOS(word,d):
    parts=word.split(d)
    return parts[-1]

class Entry:

    def __init__(self,word,group=""):
        self.word=word
        self.group=group
        self.hypers=[]
        self.coords=[]
        self.randoms=[]
        self.meros=[]

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

class BlessDB:

    knownRels=["coord","hyper","mero","random-n"]
    blessfile="BLESS.txt"

    def __init__(self,parameters):

        self.entrydict={}
        self.infile=parameters.get("parentdir","./")+parameters.get("blessdir","./")+BlessDB.blessfile
        self.pos=parameters.get("pos","X")
        self.readfile()


    def poscheck(self,word):
        return self.pos=="X" or self.pos==getPOS(word,'/')

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

                    fields[3]=untag(fields[3],'-')
                    fields[3]=fields[3].lower()
                    if fields[0] not in self.entrydict.keys():
                        self.entrydict[fields[0]] = Entry(fields[0],fields[1])
                    if fields[2] in BlessDB.knownRels:
                        self.entrydict[fields[0]].addRel(fields[2],fields[3])

                linesread+=1
                if linesread %1000 == 0:
                    print "Read "+str(linesread)+" lines"


    def getEntries(self):
        return self.entrydict.keys()

    def printstats(self):
        print "Size of entrydict is "+str(len(self.entrydict))
        print self.entrydict.keys()



