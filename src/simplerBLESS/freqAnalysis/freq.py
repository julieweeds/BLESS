
__author__ = 'juliewe'
#perfrom frequency analysis on thesaurus entries

from src.simplerBLESS.eval import Evaluator
import sys,numpy as np,math
from scipy.stats import norm as normal


class FreqEvaluator(Evaluator):

    def check_config(self):
        #defaults and other init checks
        self.parameters["debug"]=self.parameters.get("debug",[])
        try:
            self.freqfile=self.parameters.get("parentdir","./")+self.parameters["freqpath"]
        except:
            print "No frequency file given in config file"
            exit(1)

    def set_words(self):
        if self.parameters.get("words_bless"):
            self.load_bless()
            #this will set self.parameters["filterwords"]

    def filtercheck(self,word,pos,freq):
        if self.parameters.get("pos","X")=="X" or self.parameters["pos"]==pos:
            if self.parameters.get("minfreq",-1)<0 or freq>self.parameters["minfreq"]:
                return True
        return False

    def load_freqs(self):
        self.freqs={}
        print "Loading frequency estimates from "+self.freqfile
        done=0
        with open(self.freqfile) as fp:
            for line in fp:
                line=line.rstrip()
                fields=line.split('\t')
                token=fields[0].split('/')
                word=token[0]
                pos=token[1]
                freq=float(fields[1])
                if self.filtercheck(word,pos,freq):
                    self.freqs[word]=freq
                done+=1
                if done%100000==0:print "Read "+str(done)+" lines"

        if "load_freqs" in self.parameters["debug"]:
            print self.freqs
            print len(self.parameters["filterwords"]),self.parameters["filterwords"]


    def analyse(self):
        #compute mean etc of mean frequency of neighbours
        emf=np.mean(self.freqs.values()) #mean frequency of all neighbour words
        meanfreq={}
        bias={}
        ebias={}
        entryfreq={}
        plus=0
        minus=0
        eplus=0
        eminus=0
        for entry in self.thes.vectordict.keys():
            meanfreq[entry]=self.computeneighfreq(self.thes.vectordict[entry])
            entryfreq[entry]=float(self.freqs[entry[0]])
            bias[entry]=meanfreq[entry]-entryfreq[entry]
            if bias[entry]>0:plus+=1
            if bias[entry]<0:minus+=1
            ebias[entry]=emf-entryfreq[entry]
            if ebias[entry]>0:eplus+=1
            if ebias[entry]<0:eminus+=1

        #print meanfreq
        print "Neighbour mean frequency: mean = "+str(np.mean(meanfreq.values()))+", std = "+str(np.std(meanfreq.values()))+", median = "+str(np.median(meanfreq.values()))
        meanbias=np.mean(bias.values())
        medianbias=np.median(bias.values())
        stdbias=np.std(bias.values())
        error=stdbias/math.pow(len(bias.keys()),0.5)


        mean_entry_freq=np.mean(entryfreq.values())
        expectedbias=emf-mean_entry_freq
        neighbour_median=np.median(self.freqs.values())
        entry_median=np.median(entryfreq.values())
        expectedmedianbias=neighbour_median-entry_median

        print "Sign value: plus = "+str(plus)+", minus = "+str(minus)+"; out of "+str(len(bias.keys()))+" (expected: plus = "+str(eplus)+", minus = "+str(eminus)+")"
        print "high frequency bias: mean = "+str(meanbias)+", median = "+str(medianbias)+", std = "+str(stdbias)+", error = "+str(error)
        print "expected bias based on means: "+str(expectedbias)+" ("+str(emf)+"-"+str(mean_entry_freq)+")"
        prob=normal.cdf((meanbias-expectedbias)/error)
        print "Probability of less than bias: "+str(prob)
        print "expected bias based on medians: "+str(expectedmedianbias)+" ("+str(neighbour_median)+"-"+str(entry_median)+")"
        prob = normal.cdf((medianbias-expectedmedianbias)/error)
        print "Probability of less than bias: "+str(prob)


    def computeneighfreq(self,entry):
        total=0
        count=0
        for neigh in entry.allsims.keys():
            count+=1
            total+=float(self.freqs[neigh.split('/')[0]])

        return total/count


    def run(self):
        self.set_words()
        self.load_freqs()
        self.load_thes()
        self.analyse()

if __name__=="__main__":
    myEvaluation=FreqEvaluator(sys.argv[1])
    myEvaluation.run()
