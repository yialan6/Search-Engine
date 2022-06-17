# Search Engine

A search engine application that handles queries and displays results in under 300ms by searching through UCI's Informatics of Computer Science Department's corpus.

# Specifications

main.py - Generates an index for each stemmed word found in the corpus. The index stores a weight for each term, calculated using its tf-idf value and the HTML tag which it is under.

merge.py - Takes all the partial indexes generated from main.py and merges them into one document. A champions list is created containing the top k weighted results for faster queries.

query.py - Takes a query as an input and searches through the champions list for all the documents that contain each term in the query. The highest k weighted documents are returned.

serach_ui.py - A web GUI used to take a query as an input and display its results as an output.

# Installations

## Requires Python3.7 for time_ns
\
**BeautifulSoup - HTML parser**

*Install BeautifulSoup*

```
pip3 install beautifulsoup4
```
\
**nltk - token stemmer**

*Install nltk*
```
pip3 install --user -U nltk
```
*then in Python terminal or Python folder run*
```
import nltk
```
\
**Flask - web UI**

*Install virtualenv*
```
sudo python3 -m pip install virtualenv

```
*Create environment in project directory*
```
python3 -m venv <name of environment>
```
*Move into environment*
```
. <name of environment>/bin/activate
```
*Install Flask*
```
pip3 install Flask
```

# Application

1. Run main.py to get all the partial indexes.
2. Run merge.py to merge all the partial indexes and to create champions list.
3. Run search_ui.py to run the webUI.
4. Go to localhost:5000/ on your web browser.
5. Enter a query into the search bar.
6. Get results!
