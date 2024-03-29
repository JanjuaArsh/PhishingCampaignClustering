import pandas as pd   #to create data frames
import tldextract     #to extract domains, subdomains and tlds
from urllib.parse import  urlparse  #to get the path

from Cluster import Cluster
from UrlComponents import UrlComponents   
    
####The main function
def main():
    df = pd.read_csv('PhishingCampaignClustering/bda_urls_hashtags.csv',sep = ',', quotechar='"', skipinitialspace=True)
    urls = df.get("url")
    domains = []; tlds = []; subDomains = []; paths = []

    for url in urls:
        extractResult = tldextract.extract(url)
        domains.append(extractResult.domain)
        tlds.append(extractResult.suffix)
        subDomains.append(extractResult.subdomain)
        paths.append(urlparse(url).path.strip())
        #end for

    df.insert(1, "tld" , tlds, True)
    df.insert(2, "domain" , domains, True)
    df.insert(3, "subdomain" , subDomains, True)
    df.insert(4, "path" , paths, True)

    df = df[df.isPhishing != 0]
    theclusters = Cluster()
    processData(df, theclusters)
    printClustersToAFile(theclusters)
    '''df = pd.DataFrame([(k, o.sid, o.rd, o.url, o.tld)
              for k, l in theclusters.clusters.items() for o in l],
             columns=['key', 'sid', 'rd', 'url', 'tld']
            )'''
    #analyseDiffTlds(df)
    ##todo - after tld part is done - get started with getting the whois _ add the registrant to df 
####End Function

##todo - add the value of unique tld to original df and find a way to print df in file properly
def  analyseDiffTlds(df):
    with open('roughtemp10&.txt', 'w') as f:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
            print(df, file=f)
            print(df.astype(str).groupby('key')['tld'].agg(lambda x: ','.join(x.unique())), file=f)
            

def printClustersToAFile(theclusters):
    with open('PhishingCampaignClustering/clustersFormed104.txt', 'w') as f:
        for key in theclusters.clusters:
            print(key, file=f)
            for value in theclusters.clusters[key]:
                print("    " + value.url,  file=f)
####End Function
            
    
def processData(df, theclusters):
    for index, row in df.iterrows():
            urlobj = UrlComponents(row['subdomain'], row['domain'], row['tld'], row['path'], row['sid'], row['url'], row['rd'])
            theclusters.addToCluster(urlobj, index)
####End Function
        
####BEGIN - start point of the program
if __name__ == '__main__':
    main()