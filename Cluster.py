from jarowinkler import *

domain = 1
Subdomain = 2
path = 3

class Cluster:

    ####constructor --- assigning an empty dictionary
    def __init__(self, ):
        self.clusters = {}

    ####add a new cluster
    def makenewcluster(self, urlobjs, key):
        self.clusters[key] = urlobjs
        #print(self.clusters[key][0])
    
    ###needs improvement
    def compareURLObjects(self, urlobj1, urlObj2):
        ###DOMAIN 
        if jaro_similarity(urlobj1.domain, urlObj2.domain) > 0.85:
            return domain
        ###SUBDOMAIN
        elif (len(urlObj2.subdomain) > 6) and (urlobj1.subdomain != '') and (urlObj2.subdomain != '') and jaro_similarity(urlobj1.subdomain, urlObj2.subdomain) > 0.85:
            return Subdomain
        ###PATH
        elif (len(urlObj2.path) > 10) and (len(urlobj1.path) > 10) and (urlobj1.path != '') and (urlObj2.path != '') and jaro_similarity(urlobj1.path, urlObj2.path) > 0.90:
            return path
        else: return 0

    ###needs improvement
    def compareUrlToKey(self, key, urlobj):
        type = key.split('_', 1)[0]
        value = key.split('_', 1)[1]
        if type == "dom" and jaro_similarity(urlobj.domain, value) > 0.85:
            return True
        elif type == "subdom" and jaro_similarity(urlobj.subdomain, value) > 0.85:
            return True
        elif type == "path" and jaro_similarity(urlobj.path, value) > 0.90 and len(urlobj.path) > 10:
            return True
        else: return False

    ####find id the url fits and existing cluster - if yes add and return true - else return false
    def findMatch(self, key, urlobj):
        #get the list at key
        listOfUrlObjects = self.clusters[key]
        lengthOfUrlList = len(listOfUrlObjects)
        if lengthOfUrlList == 1:
            match = self.compareURLObjects(listOfUrlObjects[0],urlobj)
            if(match == domain):
                #make a new cluster and remove the previous
                del self.clusters[key]
                self.makenewcluster([listOfUrlObjects[0],urlobj], ("dom_" + urlobj.domain))
                return True
            elif(match == Subdomain):
                 #make a new cluster and remove the previous
                del self.clusters[key]
                self.makenewcluster([listOfUrlObjects[0],urlobj], ("subdom_" + urlobj.subdomain))
                return True
            elif(match == path):
                 #make a new cluster and remove the previous
                del self.clusters[key]
                self.makenewcluster([listOfUrlObjects[0],urlobj], ("path_" + urlobj.path))
                return True
            else: return False
        elif lengthOfUrlList > 1:
            #compare from the name of the key  
            '''there is a drawback to this approach
            a url can be in only one cluster no overlapping possible'''
            match = self.compareUrlToKey(key,urlobj)
            if match:
                self.clusters[key].append(urlobj)
                return True
            else: return False

    ####performs clustering
    def addToCluster(self, urlobj, index):
        keys = self.clusters.keys()
        matched = False
        # the first value - make a cluster an add object to it.
        if not any(keys):
            self.makenewcluster([urlobj], str(index))
        else:
            for key in keys:
                matched = self.findMatch(key, urlobj) #if matched already added to the cluster
                if matched:
                    return
            if not matched:
                self.makenewcluster([urlobj], str(index)) 
                return

    #####################################END CLASS##########################################