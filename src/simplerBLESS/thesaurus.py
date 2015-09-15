__author__ = 'juliewe'
#Refactored 15/9/15
#Basic thesaurus representation



import re
import sys
from blessDB import untag
from scipy.stats import norm as normal

class ThesEntry:
    debug=False

    def __init__(self, wordpos):

        self.word=wordpos[0]
        self.pos=wordpos[1]
        self.allsims={}
        self.tuplelist=[]
        self.analysed=False

    def update(self,featurelist):
        while(len(featurelist)>0):
            f=featurelist.pop()
            sc=featurelist.pop()
            self.allsims[f]=float(sc)

    def displaysims(self):
        res=self.word+"/"+self.pos
        for (sim,word) in self.tuplelist:
            res+="\t"+word+"\t"+str(sim)
        res+="\n"
        print res

    def topk(self,k):
        #only retain top k neighbours
        if len(self.tuplelist)==0:
            self.tuplelist=[]
            for item in self.allsims.keys():
                self.tuplelist.append((float(self.allsims[item]),item))
            self.tuplelist.sort()
        else:
            self.tuplelist.reverse()
        self.allsims={}
        tuplelist=self.tuplelist
        self.tuplelist=[]
        done=0
        while done < k:
            if len(tuplelist)>0:
                (sim,word)=tuplelist.pop()
                self.allsims[word]=float(sim)
                self.tuplelist.append((sim,word))
            else:
                done = k
            done+=1

    def keeptopsim(self,sim):
        #only retain neighbours above sim threshold
        tuplelist=[]
        for item in self.allsims.keys():
            tuplelist.append((float(self.allsims[item]),item))
        tuplelist.sort()
        self.allsims={}
        if len(tuplelist)>0:
          (thissim,word)=tuplelist.pop()
        else:
            thissim=-1
        while thissim > sim:

            self.allsims[word]=float(thissim)
            if len(tuplelist)==0:
                thissim=-1
            else:
                (thissim,word)=tuplelist.pop()

    def analyse(self):
        if not self.analysed:
            total =0.0
            count=0
            max=0.0
            squares=0.0
            for neigh in self.allsims.keys():
                sim =self.allsims[neigh]
                if sim > max:
                    max = sim
                    nn=neigh

                total+=float(sim)
                count+=1
                squares+=sim*sim

            self.topsim=max
            self.nearestneighbour=nn
            self.avgsim=total/count
            self.totalsim=total
            self.squaretotal=squares
            self.nosims=count
            self.sd = pow(squares*1.0/count - self.avgsim*self.avgsim,0.5)
            #increase sd slightly as estimate and do not want 0
            self.sd=self.sd+0.001
            self.analysed=True

    def znorm(self):
        #estimate normal dist params and transform into normal probs
        self.analyse()
        if ThesEntry.debug:
            print self.word, self.avgsim,self.sd

        for (sim,neigh) in self.tuplelist:
            p = normal(self.avgsim,self.sd).cdf(sim)
            self.allsims[neigh]=p

        self.analysed=False
        self.analyse()
        if ThesEntry.debug:
            print self.word,self.avgsim,self.sd

        self.tuplelist=[]



class Thesaurus:

    wordposPATT = re.compile('(.*)/(.*)') #whole POS

    def __init__(self,parameters):

        self.parameters=parameters
        self.vectordict={} #dictionary of vectors
        self.updated=0
        self.simcachefile=parameters.get("parentdir","./")+parameters.get("thesdir","./")+parameters.get("thesfile","neighbours.strings")
        self.k=parameters.get("k",1000)
        self.pos=parameters.get("pos","X")
        self.filterwords=parameters.get("filterwords",[])

        if "all" in self.parameters.get("debug",[]):
            ThesEntry.debug=True
            print self.filterwords
            print self.pos
        if "znorm" in self.parameters.get("debug"):
            ThesEntry.debug=True

        self.readsims()

    def readsims(self):

        print"Reading sim file "+self.simcachefile
        linesread=0
        instream=open(self.simcachefile,'r')
        for line in instream:
            self.processsimline(line.rstrip())
            linesread+=1
            if (linesread%1000 == 0):
                print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" similarity vectors"
                sys.stdout.flush()
                #return
        self.topk(self.k)
        print "Read "+str(linesread)+" lines and updated "+str(self.updated)+" vectors"
        instream.close()


    def filteradd(self,word,pos):
        return (len(self.filterwords)==0 or word in self.filterwords) and (pos==self.pos or self.pos=="X")

    def processsimline(self,line):
        featurelist=line.split('\t')
        matchobj = Thesaurus.wordposPATT.match(featurelist[0])
        if matchobj:
            wordpos=(matchobj.group(1),matchobj.group(2))
        else:
            print "Error with vector file matching "+featurelist[0]
            return

        (word,pos)=wordpos
        #print word,pos

        if self.filteradd(word,pos):
            self.vectordict[wordpos]=ThesEntry(wordpos)

            featurelist.reverse() #reverse list so can pop features and scores off
            featurelist.pop() #take off last item which is word itself
            self.vectordict[wordpos].update(featurelist)
            self.vectordict[wordpos].topk(self.k)
            self.updated+=1


    def topk(self,k):
        #retain top k neighbours for each word
        for thisvector in self.vectordict.values():
            thisvector.topk(k)

    def topsim(self,sim):
        #retain similarities over sim threshold
        for thisvector in self.vectordict.values():
            #print thisvector,sim
            thisvector.keeptopsim(sim)

    def displayneighs(self,word,k):
        if word in self.vectordict.keys():

            vector=self.vectordict[word]
            vector.topk(k)
            vector.displaysims()
        else:
            (word,pos)=word
            print word+"/"+pos + " not in dictionary"

    def displayall(self):
        for word in self.vectordict.keys():
            self.displayneighs(word,self.k)

    def znorm(self):
        print "Estimating means and standard deviations and normalising similarity scores"
        for vector in self.vectordict.values():
            vector.znorm()
            vector.topk(self.k)
