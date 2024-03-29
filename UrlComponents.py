class UrlComponents:
    
    ####constructor
    def __init__(self, subdomain, domain, tld, path, sid, url, rd):
        self.subdomain = subdomain
        self.domain = domain
        self.tld = tld
        self.path = path
        self.sid = sid
        self.url = url
        self.rd = rd
    ###end of constructor here
    
    def __str__(self):
        return f"subdomain: {self.subdomain} domain:{self.domain} tld:{self.tld} path:{self.path} sid:{self.sid}"
        ###end here

    #####################################END CLASS##########################################