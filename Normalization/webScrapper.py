import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
import nltk
import string
import re

"""
WebScrapper used for the creation of the common english trie.
 - Warning: The script will probably return an error with most big sites.

Author: Eli Efrain Dominguez

Email: 

"""





nltk.download('stopwords')
nltk.download('wordnet')

def get_site_info(url):
    try:
        # HTTP request
        headersList = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headersList)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error al obtener la página {url}: {e}")
        return None



def extract_from_html(html):
    try:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Extract text from the HTML and get stripped strings
        words = [string for string in soup.stripped_strings]

        # Split words using regular expressions
        word_split = []
        for word in words:
            # Split on non-alphanumeric characters
            word_split.extend(re.split(r'[^a-zA-Z0-9]', word))

        # Remove empty strings
        word_split = [p for p in word_split if p]

        return word_split
    except Exception as e:
        print(f"Error: {e}")
        return None



def word_processing(words):
    try:
        # Delete punctuation
        words = [palabra.lower().translate(str.maketrans('', '', string.punctuation)) for palabra in words]
        
        # stop words
        stop_words = set(stopwords.words('english'))
        filteredWords = [word for word in words if word not in stop_words]
        
        # Lemattize words
        lematizer = WordNetLemmatizer()
        lematized_words = [lematizer.lemmatize(word) for word in filteredWords]
        
        # Transliteration
        word_no_tilde = [unidecode(word) for word in lematized_words]
        
        return word_no_tilde
    except Exception as e:
        print(f"Error while processing: {e}")
        return None

def save_in_file(words, file_name='resultado.txt'):
    try:
        # Saves each word in a line for each one 
        with open(file_name, 'w', encoding='utf-8', errors='replace') as file:
            for palabra in words:
                file.write(f"{palabra}\n")
        print(f"Content save in {file_name}")
    except Exception as e:
        print(f"Error while saving {file_name}: {e}")

import os

def clean_filename(url):
    # Replace invalid characters with underscores
    cleaned_filename = f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt"
    cleaned_filename = re.sub(r'[^\w\-_.]', '_', url)
    return cleaned_filename

# ...

def url_from_file(urlFile):
    try:
        with open(urlFile, 'r', encoding='utf-8', errors='replace') as archivo_urls:
            #Reads the URLs
            urls = archivo_urls.readlines()
            
            for url in urls:
                # Cleans whitespaces
                url = url.strip()
                
                if url:
                    # Gets the site info
                    site_content = get_site_info(url)
                    
                    if site_content:
                        # Extracts the html data
                        extracted = extract_from_html(site_content)
                        
                        if extracted:
                            # Word processing
                            processed = word_processing(extracted)
                            
                            if processed:
                                # File name
                                nombre_archivo = f"{clean_filename(url)}.txt"
                                
                                # Saves the processed words
                                save_in_file(processed, nombre_archivo)
    except Exception as e:
        print(f"Error while processing {urlFile}: {e}")



# File directory
urls = 'urls.txt'
    
# File processing
url_from_file(urls)

