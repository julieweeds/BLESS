__author__ = 'Julie'

def configure(arguments):
    parameters={}
    parameters["filter"]=False
    parameters["entail"]=False
    parameters["sim"]=False
    parameters["at_home"]=False
    parameters["datadir"]="/Volumes/LocalScratchHD/juliewe/Documents/workspace/BLESS/data/"
    parameters["k"]=1000
    parameters["compress"]=True
    parameters["metric"]="cosine"
    parameters["simcache"]=True
    parameters["thesdir"]=""
    parameters["thesfile"]="neighbours.strings"
    parameters["vectordir"]=""
    parameters["vectorfile"]="events.strings"
    parameters["thes_override"]=False
    parameters["countfile"]="entries.totals"

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

    if parameters["at_home"]:

        parameters["datadir"]="C:/Users/Julie/Documents/GitHub/BLESS/data/"
        parameters["thesdir"]="C:/Users/Julie/Documents/GitHub/WordNet/data/giga_t100f100_nouns_deps/"
        parameters["vectordir"]="C:/Users/Julie/Documents/GitHub/WordNet/data/giga_t100f100_nouns_deps/"
        #print "Changing datadir to "+blessDB.datadir

    parameters["simfile"]=parameters["thesdir"]+parameters["thesfile"]
    return parameters
