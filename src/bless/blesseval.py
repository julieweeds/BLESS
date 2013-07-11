__author__ = 'Julie'

import thesaurus,conf,sys,math
from db import blessDB, untag
import matplotlib.pyplot as plt
import numpy as np
#from scipy.stats import norm as normal
import scipy.stats as stats


def showpoly(x,y,xlab='X',ylab='Y',title="Regression Analysis"):
    pr=stats.spearmanr(x,y)
    #print x
    xl=np.amax(x)
    #print xl
    #print y
    yl=np.amax(y)
    #print yl
    poly1=np.poly1d(np.polyfit(x,y,1))
    print poly1

#    poly2=np.poly1d(np.polyfit(x,y,2))
    print pr
#    print poly2

    xp=np.linspace(0,xl,100)
    plt.plot(x,y,'.',xp,poly1(xp),'-')
    plt.ylim(0,yl)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    mytext1="srcc = "+str(pr[0])
    mytext2="p = "+str(pr[1])
    mytext3="y = "+str(poly1)
    plt.text(0.07,yl*0.9,mytext1)
    plt.text(0.07,yl*0.8,mytext2)
    plt.text(0.07,yl*0.7,mytext3)
    plt.show()
    return poly1



class BlessThes(thesaurus.Thesaurus):

    metric="lin"
    thesaurus.Thesaurus.byblo=True

    def __init__(self,parameters):
        #create basic Thesaurus
        thesaurus.Thesaurus.__init__(self,"",parameters["simfile"],True,False,parameters["k"],1,1,False)
        self.blesscache=parameters.get("blesscache",False)
        self.pos=parameters.get("pos",'N')
        self.predict=parameters["predict_params"]

    def allsims(self,entrylist):
        if self.blesscache:
            self.simcachefile=self.simcachefile+".blesscache"
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
        if not self.blesscache:
            #write cache
            self.writecache()

    def writecache(self):
        outfile=self.simcachefile+".blesscache"
        print "Creating cache of similarities"
        with open(outfile,'w') as outstream:
            for vector in self.vectordict.values():
                outstream.write(vector.word+"/"+vector.pos)
                for(sim,word) in vector.tuplelist:
                    outstream.write("\t"+word+"\t"+str(sim))
                outstream.write("\n")

    def znorm(self,myBless,meanpoly,sigmapoly):
        for vector in self.vectordict.values():
            concept=vector.word
            if self.predict:

                (_,width)=myBless.countdict.get(concept,0)
                mean=meanpoly(math.log(float(width)))
                sd=sigmapoly(math.log(float(width)))
                #print concept,width,math.log(float(width)),mean,sd
                vector.znorm_fixed(mean,sd)
            else:
                vector.znorm()

    def get_topsim(self,concept,wordlist):
        #for given concept find closest neighbour in wordlist and return rank and sim
        rank=1
        topsim=0
        maxrank=1000
        toprank=maxrank
        for (sim, word) in self.vectordict[concept].tuplelist: #sorted list of concepts neighbours
            if untag(word,'/') in wordlist: #hey presto found the nearest one
                topsim=sim
                toprank=rank
                break
            else:
                rank+=1
        #convertrank=float(maxrank-toprank)/float(maxrank)
        return (toprank,topsim)

    def sims_to_ranks(self,simlist):
        ranklist=[]
        for sim in simlist:
            totalrank=0
            count=0
            for concept in self.vectordict.keys():
                rank=0
                for(simA,word) in self.vectordict[concept].tuplelist:
                    if float(simA) < float(sim):
                        break
                    else:
                        rank+=1
                totalrank+=rank
                count+=1
            ranklist.append(float(totalrank)/float(count))

        return ranklist

    def correlate(self,myBless,displaylist=[0,2,3]):
        labels=['Log Width','Frequency','Average Similarity','Sd similarity']
        mymatrix=[[],[],[],[]]
        polys=[]
        for concept in myBless.entrydict.keys():
            concept2=(concept,'N')
            self.vectordict[concept2].analyse()
            (freq,width)=myBless.countdict.get(concept,0)
            avsim=self.vectordict[concept2].avgsim
            sd=self.vectordict[concept2].sd
            #print concept, width, freq, avsim,sd
            mymatrix[1].append(float(freq))
            mymatrix[2].append(float(avsim))
            mymatrix[3].append(float(sd))
            mymatrix[0].append(math.log(float(width)))
        for i in range(len(displaylist)-1):
            for j in range(i+1,len(displaylist)):
                print labels[displaylist[i]],labels[displaylist[j]]
                xs=np.array(mymatrix[displaylist[i]])
                ys=np.array(mymatrix[displaylist[j]])
                polys.append(showpoly(xs,ys,labels[displaylist[i]],labels[displaylist[j]]))
        return polys



if __name__== "__main__":
    parameters=conf.configure(sys.argv)

    if parameters["thes_override"]:
        blessDB.thesdir=parameters["thesdir"]
        blessDB.countfile=parameters["countfile"]
        #print blessDB.thesdir, blessDB.countfile

    blessDB.datadir=parameters["datadir"]
    print "Loading blessDB from "+blessDB.datadir
    print "Filter file is "+blessDB.thesdir+blessDB.countfile
    print "Filter applied: "+str(parameters["filter"])
    myBless=blessDB(parameters)
    print "Created blessDB"
    myBless.printstats()
    print "Loading thesaurus with parameters "+parameters["simfile"]+" k = "+str(parameters["k"])
    myThes=BlessThes(parameters)
    myThes.allsims(myBless.entrydict.keys())

    ##test##
    #for concept in myBless.entrydict.keys():
        #myThes.displayneighs((concept,parameters["pos"]),10)

    print "Computing correlation"
    mypolys=myThes.correlate(myBless)
    print "Normalising scores"
    myThes.znorm(myBless,mypolys[0],mypolys[1])

    print "Creating boxplots for relations in:"
    print parameters["rellist"]
    relranks=[]
    relsims=[]
    relconverts=[]
    for rel in parameters["rellist"]:
        ranks=[]
        sims=[]
        converts=[]
        for concept in myBless.entrydict.keys():
            blessed=myBless.entrydict[concept].getRel(rel) #get the semantically related words from BLESS
            (rank,sim)=myThes.get_topsim((concept,parameters['pos']),blessed) #score according to thesaurus
  #          print concept, rel, blessed,rank,sim
            ranks.append(rank)
            sims.append(sim)
 #           break
        relranks.append(ranks)
        relsims.append(sims)
        relconverts.append(myThes.sims_to_ranks(sims))


#    print relranks
#    print relsims
#    print relconverts

    plt.figure(1)

    plt.subplot(131)
    bp=plt.boxplot(relranks)
   # plt.savefig('ranks')
    plt.ylim(1000,0)
    plt.yticks(np.arange(1000,0,-50))
    plt.grid(True)
    plt.ylabel('Rank')
    plt.setp(plt.gca(),'xticklabels',parameters["rellist"])

   # plt.show()


#    plt.figure()
    plt.subplot(132)
    plt.boxplot(relsims)
   # plt.savefig('sims')
    plt.ylim(0,1)
    plt.yticks(np.arange(0,1,0.05))
    plt.ylabel('Similarity')
    plt.grid(True)
    plt.setp(plt.gca(),'xticklabels',parameters["rellist"])
    plt.title(parameters["simfile"])
   # plt.show()

#    plt.figure()
    plt.subplot(133)
    bp=plt.boxplot(relconverts)
    #plt.savefig('cranks')
    plt.ylim(1000,0)
    plt.yticks(np.arange(1000,0,-50))
    plt.grid(True)
    plt.ylabel('Sims As Ranks')
    plt.setp(plt.gca(),'xticklabels',parameters["rellist"])
    plt.show()


#    myThes.displayneighs(("bomb","N"),10)
