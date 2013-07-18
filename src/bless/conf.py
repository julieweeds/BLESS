__author__ = 'Julie'

def configure(arguments):
    parameters={}
    parameters["filter"]=False
    parameters["entail"]=False
    parameters["sim"]=False
    parameters["at_home"]=False
    parameters["local"]=True
    parameters["datadir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/BLESS/data/"
   # parameters["thesdir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/giga_t100f100/"
    parameters["thesdir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/wiki_t100f100_nouns_dobj/"
    parameters["vectordir"]=parameters["thesdir"]
    parameters["k"]=1000
    parameters["compress"]=True
    parameters["metric"]="cosine"
    parameters["simcache"]=True
    parameters["thesfile"]="neighbours.strings"
    parameters["vectordir"]=""
    parameters["vectorfile"]="events.strings"
    parameters["thes_override"]=False
    parameters["countfile"]="entries.totals"
    parameters["rellist"]=["hyper","coord","mero","random-n"]
    parameters["pos"]='N'
    parameters["blesscache"]=False
    parameters["correlate"]=False
    parameters["predict_params"]=False
    parameters["topsim_corr"]=False
    parameters["adjust"]=False

    for arg in arguments:
        if arg == "filter":
            parameters["filter"]=True
        elif arg=="at_home":
            parameters["at_home"]=True
        elif arg=="entail":
            parameters["entail"]=True
        elif arg=="sim":
            parameters["sim"]=True
        elif arg=="override":
            parameters["thes_override"]=True
            parameters["filter"]=True
        elif arg=="blesscache":
            parameters["blesscache"]=True
        elif arg=="correlate":
            parameters["correlate"]=True
        elif arg=="predict_params":
            parameters["predict_params"]=True #predict normal dist parameters from width
        elif arg=="topsim_corr":
            parameters["topsim_corr"]=True #do correlation with top sim rather than average sim
        elif arg=="adjust":
            parameters["adjust"]=True  #adjust all similarities based on widths

    if parameters["at_home"]:

        parameters["datadir"]="C:/Users/Julie/Documents/GitHub/BLESS/data/"
        parameters["thesdir"]="C:/Users/Julie/Documents/GitHub/WordNet/data/giga_t100f100_nouns_deps/"
        parameters["vectordir"]="C:/Users/Julie/Documents/GitHub/WordNet/data/giga_t100f100_nouns_deps/"
        #print "Changing datadir to "+blessDB.datadir

    parameters["simfile"]=parameters["thesdir"]+parameters["thesfile"]
    return parameters
