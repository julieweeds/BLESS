__author__ = 'Julie'

def configure(arguments):
    parameters={}
    parameters["filter"]=True
    parameters["entail"]=False
    parameters["sim"]=False
    parameters["coord"]=False
    parameters["hyper"]=False
    parameters["allsim"]=False
    parameters["mero_random"]=False
    parameters["at_home"]=False
    parameters["local"]=True
    parameters["datadir"]="/home/j/ju/juliewe/Documents/workspace/BLESS/data/" #directory for BLESS data
   # parameters["thesdir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/giga_t100f100/"
    #parameters["thesdir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/wiki_t100f100_nouns_wins/" #directory for neighbour file
    #parameters["thesdir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/Relevance/data/"
    parameters["thesdir"]="/home/j/ju/juliewe/Documents/workspace/SentenceCompletionChallenge/data/apt/"
    parameters["vectordir"]=parameters["thesdir"]
    parameters["k"]=1000
    parameters["compress"]=True
    parameters["metric"]="cosine"
    parameters["simcache"]=True
    parameters["thesfile"]="neighbours.strings" #byblo neighbour file
    parameters["vectordir"]=""
    #parameters["vectorfile"]="events_rel100.strings"  #byblo events file (event frequency)
    parameters["vectorfile"]="events.strings"
    parameters["thes_override"]=True
    #parameters["countfile"]="entries.widths"  #byblo events file or alternative events file(event frequency width)
    parameters["countfile"]="entries.strings"
    parameters["rellist"]=["hyper","coord","mero","random-n"]
    parameters["pos"]='N'
    parameters["blesscache"]=False
    parameters["correlate"]=False
    parameters["predict_params"]=False
    parameters["topsim_corr"]=False
    parameters["adjust"]=False
    parameters["normalise"]=False
    parameters["pos"]="X"
    parameters["nprop"]=0

    for arg in arguments:
        if arg == "filter":
            parameters["filter"]=True
        elif arg == "nofilter":
            parameters["filter"]=False
        elif arg=="at_home":
            parameters["at_home"]=True
        elif arg=="entail":
            parameters["entail"]=True
        elif arg=="sim":
            parameters["sim"]=True
        elif arg=="override":
            parameters["thes_override"]=True
            parameters["filter"]=True
        elif arg=="NO_override":
            parameters["thes_override"]=False
        elif arg=="blesscache":
            parameters["blesscache"]=True
        elif arg=="correlate":
            parameters["correlate"]=True
        elif arg=="predict_params":
            parameters["predict_params"]=True #predict normal dist parameters from width
            parameters["correlate"]=True
            parameters["normalise"]=True
        elif arg=="topsim_corr":
            parameters["topsim_corr"]=True #do correlation with top sim rather than average sim
        elif arg=="adjust":
            parameters["adjust"]=True  #adjust all similarities based on widths
        elif arg=="normalise":
            parameters["normalise"]=True #whether to normalise similarity scores per entry
        elif arg=="coord":
            parameters["coord"]=True
        elif arg=="hyper":
            parameters["hyper"]=True
        elif arg=="allsim":
            parameters["allsim"]=True
        elif arg=="mero_random":
            parameters["mero_random"]=True
        elif arg=="wiki-lc" or arg =="wiki-mc":
            parameters["thesdir"]+=arg+"/"
            parameters["vectordir"]=parameters["thesdir"]
            parameters["pos"]="NN"
        elif arg=="nyt":
            parameters["thesdir"]+=arg+"/"
            parameters["vectordir"]=parameters["thesdir"]
            parameters["pos"]="N"
        elif arg.startswith("nouns"):
            parameters["thesdir"]+=arg+"/"
            parameters["vectordir"]=parameters["thesdir"]
        elif arg.startswith("norm"):
            parameters["thesdir"]+=arg+"/"
            parameters["vectordir"]=parameters["thesdir"]
        elif arg=="pnppmi" or arg.startswith("ppmi_"):
            parameters["thesdir"]+=arg+"/"
            parameters["vectordir"]=parameters["thesdir"]

    if parameters["at_home"]:

        parameters["datadir"]="C:/Users/Julie/Documents/GitHub/BLESS/data/"
        parameters["thesdir"]="C:/Users/Julie/Documents/GitHub/WordNet/data/giga_t100f100_nouns_deps/"
        parameters["vectordir"]=parameters["thesdir"]
        #print "Changing datadir to "+blessDB.datadir

    parameters["simfile"]=parameters["thesdir"]+parameters["thesfile"]
    return parameters
