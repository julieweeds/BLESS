__author__ = 'juliewe'
#15/9/2015
#Rewriting of core functionality of blesseval.py

from blessDB import BlessDB, untag, getPOS
from thesaurus import Thesaurus
import yaml,sys, math, matplotlib.pyplot as plt, numpy as np



class BlessThes(Thesaurus):

    def get_sim(self,concept,wordlist,n):
        #for given concept find nth closest neighbour in wordlist and return rank and sim
        rank=1
        topsim=0
        maxrank=self.parameters.get("k",1000)
        toprank=maxrank
        vector=self.vectordict.get(concept,None)
        nfound=0
        if vector!=None:
            for (sim, word) in vector.tuplelist: #sorted list of concepts neighbours
                if untag(word,'/') in wordlist: #hey presto found the nearest one
                    nfound+=1
                    if nfound==n:
                        topsim=sim
                        toprank=rank
                        break
                    else:
                        rank+=1
                else:
                    rank+=1
        else:
            print "Warning: No vector for: ",concept
        #convertrank=float(maxrank-toprank)/float(maxrank)
        return (toprank,topsim)

class Evaluator:

    def __init__(self,config):
        with open(config) as fp:
            self.parameters=yaml.safe_load(fp)
        print "Using parameters from "+config
        self.check_config()
        print self.parameters

    def check_config(self):
        #defaults and other init checks
        self.parameters["rellist"]=self.parameters.get("rellist",[])
        self.parameters["debug"]=self.parameters.get("debug",[])
        self.parameters["show"]=self.parameters.get("show",["ranks"])

    def load_bless(self):
        print "Loading Bless database"
        self.blessDB=BlessDB(self.parameters)
        self.parameters["filterwords"]=self.blessDB.getEntries()
        self.blessDB.printstats()

    def load_thes(self):
        print "Loading thesaurus"
        self.thes = BlessThes(self.parameters)
        self.thes.znorm()
        if "thes" in self.parameters.get("debug"):
            self.thes.displayall()

    def run_blesseval(self):
        print "Running Bless Evaluation"

        print "Creating boxplots for relations in:"
        print self.parameters["rellist"]
        relranks=[]
        relsims=[]
        for rel in self.parameters["rellist"]:
            ranks=[]
            sims=[]

            for concept in self.blessDB.entrydict.keys():
                blessed=self.blessDB.entrydict[concept].getRel(rel)#get the semantically related words from BLESS

                if self.parameters.get("nprop",0)<=0:
                    n=self.parameters.get("bestn",1)
                else:
                    n=math.floor(len(blessed)*float(self.parameters["nprop"]))

                (rank,sim)=self.thes.get_sim((concept,self.parameters['pos']),blessed,n) #score according to thesaurus
      #          print concept, rel, blessed,rank,sim
                ranks.append(rank)
                sims.append(sim)
     #           break
            relranks.append(ranks)
            relsims.append(sims)

        plt.figure(1)
        if self.parameters.get("nprop",0)<=0:
            key="best "+str(self.parameters.get("bestn",1))
        else:
            key="best "+str(float(self.parameters["nprop"])*100)+"%"

        if "sims" in self.parameters["show"]:
            self.show_sims(relsims,self.get_position("sims"))

        if "ranks" in self.parameters["show"]:
            self.show_ranks(relranks,self.get_position("ranks"))


        #plt.figure(1)
        plt.title(self.parameters["thesdir"]+": "+key)
        plt.show()



    def get_position(self,item):
        if len(self.parameters["show"])==1:
            return 1
        elif len(self.parameters["show"])<4:
            position=101+len(self.parameters["show"])*10
            for thing in self.parameters["show"]:
                if item==thing:
                    break
                else:
                    position+=1
        else:
            print "Do not know how to position more than 3 subplots"
        return position

    def show_ranks(self, relranks,position):
        if position>1:
            plt.subplot(position)
        plt.boxplot(relranks)
        plt.ylim(1000,0)
        plt.yticks(np.arange(1000,0,-50))
        plt.grid(True)
        plt.ylabel('Rank')
        plt.setp(plt.gca(),'xticklabels',self.parameters["rellist"])


    def show_sims(self,relsims,position):
        if position>1:
            plt.subplot(position)
        plt.boxplot(relsims)

        plt.ylim(0,1)
        plt.yticks(np.arange(0,1,0.05))
        plt.ylabel('Similarity')
        plt.grid(True)
        plt.setp(plt.gca(),'xticklabels',self.parameters["rellist"])

    def run(self):
        self.load_bless()
        self.load_thes()
        if self.parameters.get("blesseval",False):
            self.run_blesseval()

if __name__=="__main__":
    myEvaluation=Evaluator(sys.argv[1])
    myEvaluation.run()


