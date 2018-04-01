# Written using Python 3.6.3. (64-bit) - due to size of data, 64-bit version of Python might be necessary
# Supporting information to IJED article submission ("Fitness tracking technology and online communities")
#==========================================================================================================================================================================================================================================

# FOLLOWING CODE REFERS TO SECTION 2.4. OR ARTICLE, STEP 1

# After reading the instructions below, press ctrl+shift+F10 to run the code

# This code extracts data from Reddit files, as detailed in the IJED article submission
# To specify the subreddits from which to extract comments:
    # - identify the name of each subreddit for which you want to extract your data (e.g. EatingDisorders)
    # - create a .txt file named ("subreddits.txt") and save in the same directory as this code (example provided with code)
    # - populate the .txt file with the subreddits from which you want to extract data (each subreddit on a separate line, same capitalisation as on Reddit (e.g. "EatingDisorders") - N.B. if there is more than one subreddit of interest, use code 1b after 1a to separate these into different .csvs
# In order for data to be extracted, one or more .bz2 files (each corresponds to a separate month/year) from http://files.pushshift.io/reddit/comments/ (with name unchanged) should be in the same folder directory as this code
# When run, this code will then output a .csv file to the same directory containing the following data for each comment in the subreddits and months of interest:
    # - month posted
    # - author identifier (number used in place of Reddit username; '[deleted]'=1, 'AutoModerator'=2)
    # - subreddit name
    # - link identifier
    # - comment (i.e. text) body
    # - thread identifier

#==========================================================================================================================================================================================================================================

# This section of code imports necessary packages and sets stopwords, etc.
import re, bz2, glob, json, string, pandas as pd # imports necessary packages for this code; some packages might need installation, for which youtube.com provides useful tutorials
from nltk import word_tokenize # imports natural language processing toolkit package
from nltk.corpus import stopwords # imports natural language processing toolkit package
subreddits = [line.strip() for line in open("subreddits.txt", 'r')] # reads subreddits of interest from .txt file
R_files = glob.glob("*.bz2") # identifies all .bz2 files in same directory as this code
stop_words = set(stopwords.words('english')) # sets the stop words to use
stop_words.update(['TRUE','FALSE','oh','hi','hello','no','yes','1','2','3','4','5','6','7','8','9','0','a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at', 'b', 'be','because','been','but','by','c','can','cannot','could','d','dear','did','do','does','e','either','else','ever','every','f','for','from','g','get','got','h','had','has','have','he','her','hers','him','his','how','however','g','i','if','in','into','is','it','its','j','just','k','l','least','let','like','likely','m','may','me','might','most','must','my','n','neither','no','nr','not','o','of','off','often','on','only','or','other','our','own','p','q','r','rather','s','said','say','says','she','should','since','so','some','t','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','u','us','v','w','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','x','y','yet','you','your','z']) # appends other stopwords to set (includes duplicates)
translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
author_dict = {'[deleted]':1, 'AutoModerator':2} # dictionary of authors
author_count=2

#==========================================================================================================================================================================================================================================

# If the frequency of any two-word terms is being assessed, these should be merged (i.e. remove whitespace)
# Each two-word term should be entered on the same row of a .csv ("double_words.csv"), with the first word in the first column, and the second word in the second column
# If not double words to merge, place a hash symbol (#) in front of every line in this section (i.e. lines 40-47)
twowordlist_space = []
twowordlist_no_space = []
with open("double_words.csv", 'rt', encoding='utf8') as tech_input: # specify the prefix of the corpus
    for line in tech_input:
        line = line.split(",")
        twowordlist_space.append(line[0]+' '+(line[1])[:-1])
        twowordlist_no_space.append(line[0]+(line[1])[:-1])
twoword_dict = dict(zip(twowordlist_space, twowordlist_no_space))

#==========================================================================================================================================================================================================================================

# The following code reads a .bz2 file row-by-row, extracts comments from subreddits of interest and processes them. This repeats for each .bz2 file in the same folder as this code.
for file in R_files:
    print(file) # indicates the .bz2 file the code is currently working on in the console below (*DON'T OPEN THE .csv IT IS CURRENTLY WORKING ON OR IT WILL FORCE AN ERROR*)
    with bz2.open(file, 'rt') as f:
        data = [] # creates a list with all the data of interest
        for line in f:
            comment = json.loads(line)
            if (comment['subreddit']) in subreddits: # following enumerates authors
                if (comment['author']) in author_dict:
                    author = author_dict[(comment['author'])]
                else:
                    author_count += 1
                    author_dict[(comment['author'])] = (author_count)  # update dictionary
                    author = author_dict[(comment['author'])]
                body = comment['body']
                body = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ', body) # replaces URL links with a space
                body = body.replace("\n", " ") # replaces escape character 'newline' with a space
                body = body.replace("\r", " ") # replaces escape character 'carriage return' with a space
                body = body.replace("\t", " ") # replaces escape character 'tab' with a space
                body = body.replace("[deleted]", " ") # replaces any indication of a deleted body (i.e., '[deleted]') with a space
                body = body.lower() # makes all text lowercase
                body = body.translate(translator) # replaces any punctuation with a space
                body = re.sub(r'[^a-zA-Z\s]', "", str(body)) # removes any non 'a-z' 'A-Z' characters from body
                body = word_tokenize(body)  # turns body into a list of words
                body = [w for w in body if not w in stop_words]  # removes stop words
                body = ' '.join(body)  # turns body into a string
                for key, value in twoword_dict.items():
                    body = body.replace(key, value) # removes the space between any two-word terms
                relevant_comment = [file[3:-4], ("b_"+str(author)), comment['subreddit'], comment['link_id'], body, (comment['subreddit']+"_"+comment['link_id'])]  # this is the data from a comment that is extracted, this can be amended to extract more/less data, the first item in the list is the .bz2 file name; preceding letters for author and body (i.e., 'b_' and 'e_txtbdy ', respectively) help prevent formatting errors when printed in csv
                data.append(relevant_comment) # adds comment and relevant information to data list

# ==========================================================================================================================================================================================================================================

# SAVES EXTRACTED DATA TO A .csv FILE (name of .csv = the month to which the .bz2 relates)
    df = pd.DataFrame(data, columns=["a_month", "b_author", "c_subreddit", "d_link_id", "e_body", "f_thread_id"]) # prints .csv file headers
    df.to_csv(file[3:-4]+".csv",index=False,columns=("a_month", "b_author", "c_subreddit", "d_link_id", "e_body", "f_thread_id")) # adds a new row to the .csv containing the extracted data


# ==========================================================================================================================================================================================================================================
