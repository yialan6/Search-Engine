import os
from bs4 import BeautifulSoup
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


ps = PorterStemmer()

numDocuments = 0
docID = dict()


def indexer():
    global numDocuments
    if not os.path.exists('Indexes'): os.mkdir('Indexes')
    for folder in os.listdir('DEV'):
        indexes = dict()
        if folder == '.DS_Store': continue          # .DS_Store gets created automatically; no need to delete it all the time
        for file in os.listdir(os.path.join('DEV', folder)):
            if file == '.DS_Store': continue        # .DS_Store gets created automatically; no need to delete it all the time
            numDocuments += 1
            with open(os.path.join('DEV', folder, file), 'r') as f:
                data = json.load(f)
                content = data['content']

                # Need this block of code to use BeautifulSoup without warnings (still need to add more)
                # May not be able to use BeautifulSoup as not all JSON files are well-formatted
                '''
                # Index 20 was chosen to check the document type; doesn't necessarily have to be 20
                if '!DOCTYPE HTML' in content[:20] or '!DOCTYPE html' in content[:20]:      # Use 'lxml' parser
                    soup = BeautifulSoup(content, 'lxml')
                elif content[1:5] == '?xml':                                                # Use 'xml' parser
                    soup = BeautifulSoup(content, 'xml')
                else:                                                                       # Manual string processing
                    #soup = BeautifulSoup(content, 'lxml')
                    #print(soup.title, soup.text[:10])
                '''

                newID = False
                if data['url'] not in docID.values():
                    newID = True
                    docID[len(docID)] = data['url']
                
                if newID:
                    urlID = len(docID) - 1
                else:
                    urlID = docID.keys()[docID.values().index(data['url'])]

                #stemmed_tokens = [ps.stem(token) for token in word_tokenize(content) if token.isalnum()]
                # May need to modify PorterStemmer to take word importance into account

                tokensFrequency = dict()

                soup = BeautifulSoup(content, 'html.parser')

                # Weight of 2 
                for tag in soup.find_all(['i', 'em', 'h5', 'h6']):
                    stemmed_tokens = [ps.stem(word) for word in word_tokenize(tag.text) if word.isalnum()]
                    for token in stemmed_tokens:
                        if token not in tokensFrequency:
                            tokensFrequency[token] = 0
                        tokensFrequency[token] += 2
                
                # Weight of 3 tags
                for tag in soup.find_all(['b', 'h3', 'h4']):
                    stemmed_tokens = [ps.stem(word) for word in word_tokenize(tag.text) if word.isalnum()]
                    for token in stemmed_tokens:
                        if token not in tokensFrequency:
                            tokensFrequency[token] = 0
                        tokensFrequency[token] += 3

                # Weight of 4 tags
                for tag in soup.find_all(['h2']):
                    stemmed_tokens = [ps.stem(word) for word in word_tokenize(tag.text) if word.isalnum()]
                    for token in stemmed_tokens:
                        if token not in tokensFrequency:
                            tokensFrequency[token] = 0
                        tokensFrequency[token] += 4

                # Weight of 5 tags
                for tag in soup.find_all(['h1']):
                    stemmed_tokens = [ps.stem(word) for word in word_tokenize(tag.text) if word.isalnum()]
                    for token in stemmed_tokens:
                        if token not in tokensFrequency:
                            tokensFrequency[token] = 0
                        tokensFrequency[token] += 5

                # Weight of 1 tags
                for tag in ['i', 'em', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    [s.extract() for s in soup(tag)]
                for tag in soup.find_all():
                    stemmed_tokens = [ps.stem(word) for word in word_tokenize(tag.text) if word.isalnum()]
                    for token in stemmed_tokens:
                        if token not in tokensFrequency:
                            tokensFrequency[token] = 0
                        tokensFrequency[token] += 1


                for token, frequency in tokensFrequency.items():
                    if token not in indexes:
                        indexes[token] = set()
                    indexes[token].add((urlID, frequency))
        
        # Store the indexes to a file with the same name as the folder (one index file for each folder)
        with open(f'Indexes/{folder}.txt', 'w') as file:
            # indexes: {term: postings}
            # postings: docID, frequency/ tf-idf
            # sort term alphabetically
            # sort postings by docID
            for term, postings in sorted(indexes.items()):
                file.write(term + ", " + str(sorted(postings)).replace("), ","),  ") + "\n")

        
    # # Store URL/integer HashMap
    # with open(f'docID.txt', 'w') as file:
    #     for _, url in docID.items():
    #         # Updated to only write url
    #         file.write(url + "\n")


    with open('docID.txt', 'w') as file, \
        open('docID_position.json', 'w') as docID_position:
        id_position_dict = dict()
        for id, url in docID.items():
            id_position_dict[id] = file.tell()
            file.write(url + "\n")


        json.dump(id_position_dict, docID_position)

if __name__ == '__main__':
    indexer()

    # Report - MS 1
    print(f'Number of Documents: {numDocuments}\n\n')

    # print(f'Number of (Unique) Words: {len(inverted_index)}\n\n')

    print(f"Total Size of Index: {sum([os.path.getsize(os.path.join('Indexes', file)) for file in os.listdir(os.path.join(os.getcwd(), 'Indexes')) if file.endswith('.txt')] + [os.path.getsize('docID.txt')])} bytes")

# Number of Documents: 55393
# Total Size of Index: 211951484 bytes
