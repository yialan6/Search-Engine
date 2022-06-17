import json

import time
import ast
import math

from urllib.parse import urlparse
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
ps = PorterStemmer()

numDocuments = 55393


def intersect_postings(p1, p2, n=-1):
    answer = list()

    while len(p1) != 0 and len(p2) != 0:
        if n != -1 and len(answer) == n:
            break
        if p1[0][0] == p2[0][0]: # comparing docIDs
            answer.append((p1[0][0], p1[0][1]+p2[0][1]))
            p1 = p1[1:]
            p2 = p2[1:]
        else:
            if p1[0][0] < p2[0][0]:
                p1 = p1[1:]
            else:
                p2 = p2[1:]
  
    return answer
  

def tf_idf_score(term_frequency, document_frequency):
    return (1 + math.log(term_frequency, 10)) * math.log(numDocuments / document_frequency, 10)


def run(query):
    with open('champion_list_position.json', 'r') as f1, \
        open('champion_lists.txt', 'r') as champion_lists, \
        open('docID_position.json', 'r') as f2, \
        open('docID.txt', 'r') as urls:
       
        champion_list_position = json.load(f1)
        docID_position = json.load(f2)
            
        start_time =  time.time_ns()
        stemmed_query_list = [ps.stem(token) for token in word_tokenize(query) if token.isalnum()]
        
        possible_postings = list()

        for term in stemmed_query_list:
            try:
                position = champion_list_position[term]
            except:
                continue
            champion_lists.seek(position)
            
            # line = "00000000h, 2, [(24449, 5.5), (27466, 3)]"
            # line =  "term, document_frequency, [(doc_ID, tf_idf), (doc_ID, tf_idf), etc.]"
            line = champion_lists.readline()
            line_list = line.rstrip().split(', ', 2)
            
            postings = ast.literal_eval('[' + line_list[2][1:-1] + ']')
            
            possible_postings.append(sorted(postings, key=lambda x : (x[0], -x[1])))
        
        # sort because want to process terms in order of increasing document frequency
        possible_postings.sort(key = lambda x: len(x))
        
        # Find union of all terms' postings lists
        try:
            result_postings = possible_postings[0]
        except:
            result_postings = []
          
        for p in possible_postings[1:]:
            result_postings = intersect_postings(result_postings, p)
  
        # Added all the tf_idf of each term for each document in intersect_postings()

        results = []
        counter = 0
        tracker = set()
        for docID, _ in sorted(result_postings, key=lambda x: -x[1]):
            position = docID_position[str(docID)]
            urls.seek(position)
            url = urls.readline()
            
            parsed_url = urlparse(url)
            path = parsed_url.path.split('/')
            scheme_path = parsed_url.hostname + '/' + path[1]
            
            if scheme_path not in tracker:
                tracker.add(scheme_path)
                results.append(url)
                counter += 1
            if counter == 25:
                break
        print("Total number of results:", len(result_postings))
          
        end_time = time.time_ns()
          
        print("Time:", (end_time - start_time) // 1_000_000, "ms")
        return [results, (end_time - start_time) // 1_000_000]


if __name__ == '__main__':
    while True:
        query = input()
        run(query)
