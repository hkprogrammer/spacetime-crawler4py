import re
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scraper(worker,frontier,url, resp,config,writingFile,stopwords,discoveredURLS,urlDoc):


    links = extract_next_links(worker,frontier,url, resp,config,writingFile,stopwords,discoveredURLS,urlDoc)
    
    return [link for link in links if is_valid(link)]

def extract_next_links(worker,frontier,url, resp,config, writingFile,stopwords,discoveredURLs,urlDoc):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    
    
    ### Start Added by Hitoki 4/26/2023 10:52pm
    
    
    # print(resp)
    
    if not is_ascii(url):
        return list()
    
    if resp.status == 200: #added by Hitoki 4/27/2023 12:17pm
        print(url)
        soup = BeautifulSoup(resp.raw_response.text, 'html.parser') # beautifulsoup for html.
    
        #finding all links
        links = list()
        texts = soup.get_text()
        
        errorLists = ["Sorry, the requested page or file does not exist.","404","file not found", "page not found"]
        
        frontier.visited.append(discoveredURLs)
        for i in errorLists:
            if i in texts:
                return list()
        
        
        tokens = list(set(tokenize(texts,stopwords)))
        if simHash(tokens) not in frontier.visitedSimHashes:
            frontier.visitedSimHashes.append(simHash(tokens))
            #TODO complete simhash
            
            # errorLists = ["Sorry", "the", "requested", "page", "or", "file", "does", "not", "exist"]
            
            
            
            if len(tokens) >= config.min_words:
                
                writingFile.write("\nPAGE::"+url)
                writingFile.write("\n"+"\n".join(sorted(tokens)))
                
            for link in soup.find_all('a'):
                link = link.get('href')
                
                if not link or "pdf" in link:
                    continue
                
                link = toAbsolute(url,link)
                if re.match("^.+ics.uci.edu/",str(link)) or re.match("^.+cs.uci.edu/",str(link)) or re.match("^.+informatics.uci.edu/",str(link)) or re.match("^.+stat.uci.edu/",str(link)):
                    
                    
                    
                    if link not in discoveredURLs:
                        if "?" in link:
                            link = link[:link.index("?")] # this takes out the fragment
                        if "#" in link:
                            link = link[:link.index("#")]
                        links.append(link)
                        discoveredURLs.append(url)
            
            print(f"\n\nDiscovered: {len(frontier.save)} URLS so far & Visited: {worker.downloadedURLs} URLS")
            urlDoc.write("\n"+resp.url)
            return links
    ### END by hitoki 4/26/2023 10:52pm
    
    return list()

#added by Hitoki 4/27/2023 1:19am
def toAbsolute(url, newlink):
    #TODO make relative to absolute
    if newlink.startswith("https://") or newlink.startswith("http://"):
        return newlink
    combined = urljoin(url, newlink)

    return combined  

#added by Hitoki 4/27/2023 1:24am
def simHash(words):
    # Lecture Slide 9.5 & 12
    # Initialize hash array with zeros
    # words are already tokenized and pased into

    hash_size = 64
    v = [0] * (hash_size + 1)
    # extra bit is used as a sign bit

    # Calculate hash values
    for token in words:
        # Compute hash for the token using MD5
        #token_hash = hashlib.md5(token.encode('utf-8')).hexdigest()

        # Convert hash to binary representation
        #token_bin = bin(int(token_hash, 16))[2:].zfill(hash_size)
        token_bin = bin(int(hash(token)))[2:].zfill(hash_size)
        # to remove first two characters from binary expression of hash value (Ob)

        # Add token's binary hash to the vector
        # Vector V formed by summing weights
        for i, bit in enumerate(token_bin):
            if bit == '1':
                v[i] += 1
            else:
                v[i] -= 1

    # Now bit is (fingerprint formed from V)
    simhash = 0
    for i, bit in enumerate(v):
        if bit > 0:
            simhash |= 1 << i

    return simhash
    #return -1

#from stackoverflow page: https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)


#added by Hitoki 4/27/2023 1:12am
def tokenize(text,stopwords)->list:
    """The tokenize function is a modified function from Assignment 1 Part A of Hitoki Kdahashi's submission (37022201)
    This function takes in a string text, splits it by white spaces, and attempt to check the validity of each word.
    A word is valid if it is not in the stopwords list, or that it is more than 1 character long, and obeys the regular expression ^[a-zA-Z0-9]$, or that it has to be alphanumerical.
    
    THIS FUNCTION DOES NOT REMOVE DUPLICATES
    
    Args:
        text (str): text scraped from the crawler
        stopwords (list[str]): list of string of stopwords in english dictionary.

    Returns:
        List[str]: A list of token strings
        
    Complexity:
        O(n) where n is the number of characters in the text because this function loops through every line and for every line it iterates through every character in that line. Thus the function grow in linear time based on the input N.
    """
    text = text.split(" ") 
    words = []
    numOfStopWordsDetected = 0
    # iterate avery line
    for word in text:
        #reset currentword
        currentWord = ""
        for i in word: 
            
            #if word is upfront in the stopwords list or that if it is less than or equal to 1 characters long then discard it.
            if word.lower() in stopwords or len(word) <= 1:
                numOfStopWordsDetected+=1
                continue
            try:
                # if current char is alphanumerical, then it is in the sequence of the token
                if re.match('^[a-zA-Z0-9]$',i): 
                    # if i.isalnum():
                    currentWord+=i
                    # print(currentWord)
                else:
                    
                    # if current word is "" then no sequence of alphanumerical strings are being appeneded
                    if currentWord == "": continue
                    
                    # if word in stopword list then discard the word
                    if currentWord.lower() in stopwords or len(currentWord) <= 1:
                        currentWord = ""
                        numOfStopWordsDetected+=1
                        continue
                    
                    #add to wordlist
                    words.append(currentWord.lower())
                    currentWord = ""
                
            except:
                continue
    print("Number of stopwords detected:",numOfStopWordsDetected)

    return words
       

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        if not is_ascii(url):
            return False
        if "zip-attachment" in url or "files" in url:
            return False
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|pdf|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|ppsx"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|bib|pptx|ppsx|ppt|odc|txt|war|py|apk|file|ipynb|z|a|ps)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


if __name__ == "__main__":
    print(is_valid(""))
    
    print(simHash(["Hello", "World"]))
    print(simHash(["Hello", "World","a"]))
    
