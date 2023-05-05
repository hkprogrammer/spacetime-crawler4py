from collections import defaultdict

def readFile(filepath):
    
    d = dict()
    with open(filepath) as f:
        
        
        
        
        currentURL = None
        for line in f:
            line = line.rstrip("\n")
            if ".apk" in line or "zip-attachment" in line or "mpg" in line or "war" in line or "files" in line or ".Z" in line or "wp-content/uploads" in line:
                currentURL = None
                continue
           
            
            
            if line.startswith("PAGE::"):
                # URL
                URL = line.split("PAGE::")[1]
                if URL in d:
                    # skipping an url in the cases if there is a duplicate.
                    currentURL = None
                    continue
                # assert URL not in d
                d[URL] = []
                currentURL = URL
                continue
            if currentURL != None:
                d[currentURL].append(line)
    
    new_d = {}
    for i in d:
        counts = 0
        for k in d[i]:
            numOfDigits = [char for char in k if char.isdigit()]
            if len(numOfDigits)/len(k) <=.10 or len(numOfDigits) == len(k):
                pass
            else:
                counts+=1
            if counts >= 50:
                break
                
        else:
            if counts < 50:
                new_d[i] = d[i]
            continue
    # return d
    return new_d,d


def findLongestPage(mapping):
    currentLongest = []
    currentLongestURL = ""
    for i in mapping:
        if len(mapping[i]) > len(currentLongest):
            currentLongest = mapping[i]
            currentLongestURL = i
    return currentLongestURL,currentLongest


def mostCommonWords(mapping,num):
    words = defaultdict(int)
    for i in mapping:
        for k in mapping[i]:
            if len(k) <=2:
                continue
            words[k] += 1
    
    listOfWords = list()
    for i in words:
        listOfWords.append((i,words[i]))
    return sorted(listOfWords,key=lambda x:x[1],reverse=True)[:num]


def readPages(filepath):
    f = open(filepath)
    
    listOfURLS = []
    for i in f:
        i = i.rstrip("\n")
        if i in listOfURLS:
            continue
        listOfURLS.append(i)
    f.close()
    return listOfURLS[1:]
    
def uniquePages(listOfURLS):
    return len(list(set(listOfURLS)))    

def countSubdomains(listOfURLS):
    
    subdomains = defaultdict(int)
    for i in listOfURLS:
        i = i.rstrip("\n").split("uci.edu")
        path = i[1]
        subdomain = i[0] + "uci.edu"
        subdomains[subdomain] += 1
    # print(subdomains)
    return subdomains
        
    
    


if __name__ == "__main__":
    

    #Method 1: how many pages had the word (for the case when one document has huge amount of the same word when other document doesn't have at all
    wordMapping,originalMapping = readFile("wordsCollection.txt")
    
    longestURL,words = findLongestPage(wordMapping)
    
    print(f"longest URL {longestURL} with {len(words)}")
    print("==========================================")
    # print(longestURL,len(words))
    fiftyMostCommon = mostCommonWords(wordMapping,50)
    print("Fifty most common words in all pages (didn't ignore noises)")
    
    print("Words -> frequency")
    for i in fiftyMostCommon:
        print(i[0], "->",i[1])
    
    
    urls = readPages("pageOfURLS.txt")
    print("===========================================================")
    print("# of unique pages")
    print(uniquePages(urls))
    

    print("==================================================")
    print("Subdomains count:")
    subs_dict = countSubdomains(urls)
    subs_sorted = list(sorted(subs_dict,key=(lambda x:subs_dict[x]),reverse=True))
    for i in subs_sorted:
        print(i,"->",subs_dict[i])
     
    
        
    
    
    
    

        