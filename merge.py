import os
import json
import ast
import math

numDocuments = 55393

term_counter = 0
term_position = dict() # position in merged_index.txt
champion_list_position = dict() # position in champion_lists.txt

def merge():
    with open('merged_index.txt', 'w') as merged_index, \
        open('champion_lists.txt', 'w') as champion_lists:
        index_position = dict()
        
        indexes = list()
         
        # open all partial index files
        for file in os.listdir('indexes'):
            index = open(os.path.join('indexes', file), 'r')
            index_position[index]  = index.tell()
            indexes.append(index)

        # iterate through all files to get next term to put in merged_index, repeat:
            # get all possible next term from all files (readline)
            # pick the lowest term alphabetically
            # update position of the index(ess) of that term only
            # remove the index of any term that has line == ""
            # if there are duplicates for that lowest term, merge postings 

        while len(indexes) != 0:
            possible_terms = list()
            possible_postings = list()
            count  = 0
            for index in indexes: # index = open(file_name, 'r')
                count += 1
                position = index_position[index] # position = index.tell()
                index.seek(position)

                line = index.readline()

                if line != "":
                    line_list = line.rstrip().split(', ', 1)
                    current_term = line_list[0]
                    current_postings = ast.literal_eval('[' + line_list[1][1:-1] + ']')

                    possible_terms.append(current_term)
                    possible_postings.append(current_postings)

                    
                else:
                    possible_terms.append(line)
                    possible_postings.append(line)


            term = min(possible_terms)
            print(term)
            postings = None


            for i, t in enumerate(possible_terms):
                if t == term:
                    if postings == None:
                        postings = possible_postings[i]
                    else:
                        postings = union_postings(postings, possible_postings[i])
                    
                    index_position[indexes[i]] = indexes[i].tell()

            new_indexes = list()
            for i, t in enumerate(possible_terms):
                if t == "":
                    index_position[indexes[i]] = indexes[i].tell()
                else:
                    new_indexes.append(indexes[i])                

            indexes = new_indexes

            if term != None and postings != None: 
                global term_position
                term_position[term] = merged_index.tell()

                merged_index.write(term + ", " + str(postings) + "\n")
                global term_counter
                term_counter += 1

                # CHAMPION LIST
                # calculate tf-idf for all documents in postings list
                # sort the postings list by tf-idf
                # store the first r documents in champion_lists.txt
                # line in champion_lists.txt = "term, len_original_postings_list, [(docID, tf-idf), (), ...]"
                document_scores = dict()
                for posting in postings:
                    score = tf_idf_score(posting[1], len(postings))
                    document_scores[posting[0]] = score
            
        
                updated_postings = list()

                r = 0
                max_r = 2000
                for docID, tf_idf in sorted(document_scores.items(), key= lambda x: -x[1]):
                    updated_postings.append((docID, tf_idf))
                    r += 1
                    if r == max_r:
                        break
                
                champion_list_position[term] = champion_lists.tell()
                champion_lists.write(term + ", " + str(len(postings)) + ", " + str(updated_postings) + "\n")


        # close all partial index files
        for index in index_position:
            index.close()

    with open('term_position.json', 'w') as file:
        json.dump(term_position, file)

    with open('champion_list_position.json', 'w') as file:
        json.dump(champion_list_position, file)



def union_postings(p1, p2):
    answer = list()
    # print(p1, p2)
    while len(p1) != 0 and len(p2) != 0:
        if p1[0][0] == p2[0][0]:
            answer.append(p1[0])
            p1 = p1[1:]
            p2 = p2[1:]
        else:

            if p1[0][0] < p2[0][0]:
                answer.append(p1[0])
                p1 = p1[1:]
            else:
                answer.append(p2[0])
                p2 = p2[1:]

    if len(p1) != 0:
        for p in p1:
            answer.append(p)
    if len(p2) != 0:
        for p in p2:
            answer.append(p)

    return answer


def tf_idf_score(term_frequency, document_frequency):
    return (1 + math.log(term_frequency, 10)) * math.log(numDocuments / document_frequency, 10)



        


if __name__ == '__main__':
    merge()

    print(f'Number of terms: {term_counter}\n\n')


    # Old Number of terms: 1013219
    # New Number of terms: 184827
