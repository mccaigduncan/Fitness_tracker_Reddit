# Code prepared by Duncan McCaig (d.mccaig@warwick.ac.uk) Dec 2017-Jan 2018 - please do not hesitate to contact if any problems with the code are encountered
# Written using Python 3.6.3. (64-bit) - due to size of data, 64-bit version of Python might be necessary
# Supporting information to IJED article submission ("Fitness tracking technology and online communities")
#==========================================================================================================================================================================================================================================

# FOLLOWING CODE REFERS TO SECTION 2.4. OF ARTICLE, STEP 2

# After reading the instructions below, press ctrl+shift+F10 to run the code

# This code concatenates all comments related to the same thread and subreddit
# In order for the threads to concatenate, all .csvs for a subreddit should be placed in the same folder as this code
# When the code finishes, it will produce one .csv in the same folder that contains all of the threads for that subreddit (inc. all months for which there were separate files)
# Each row of the output file ("cnct_thrds.csv") corresponds to a thread

#==========================================================================================================================================================================================================================================

import csv, glob
r_files = glob.glob("*.csv") # reads all files from step 1 that are in the same folder as this code
thread_dict = {}

#==========================================================================================================================================================================================================================================

with open("cnct_thrds.csv", 'a', encoding='utf8', newline='') as output:
    writer = csv.writer(output)
    for file in r_files:
        with open(file, 'rt', encoding='utf8') as input:
            input.readline() # skips first line in files (i.e., headers)
            for row in input:
                row = row.split(",")
                if row[5] in thread_dict:
                    thread_dict[row[5]].append(row[4])
                else:
                    thread_dict[row[5]] = [row[4]]
    for key, value in thread_dict.items():
        thread_string = ' '.join(value)
        thread_string = thread_string.replace("  ", " ")
        writer.writerow([thread_string])

#==========================================================================================================================================================================================================================================
