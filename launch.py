from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from collections import Counter


def main(config_file, restart):

    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()
    
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)

    

    # top_50_words = word_count_common(50)

    # with open('top_50_words.txt', 'w') as f:
    #     f.write("Top 50 Words appeared from the crawler!\n")
    #     for word, count in top_50_words:
    #         f.write(f'{word}: {count}\n')

    #Method 2: How many times the word appeared in the documents (Counts)

    '''
    with open('wordscolleciton.txt', 'r') as f:
        texts = f.read().split()

    word_counts = Counter(texts)

    sorted_words = sorted(word_counts.items(), key = lambda x: x[1], reverse = True)

    with open('top_50_words.txt', "w") as f:
        f.write("Top 50 Words appeared from the crawler!\n")
        for word, count in sorted_words[:50]:
            f.write(f"{word}: {count}\n")
    '''




        
