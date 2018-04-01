# Written using Python 3.6.3. (64-bit) - due to size of data, 64-bit version of Python might be necessary
# Supporting information to IJED article submission ("Fitness tracking technology and online communities")
#==========================================================================================================================================================================================================================================

# FOLLOWING CODE REFERS TO SECTION 2.4. OF ARTICLE, STEP 1

# If multiple subreddits were extracted in step 1a, use this code to separate them into separate files for each subreddit

# First, put all .csv files from step 1a in the same folder as this code

# Second, specify the name of the subreddit (exactly as it appears) in the quotation marks below
# e.g. subreddit = "EatingDisorders"
subreddit = "EatingDisorders"

# Third, enter a three letter term below to represent the subreddit
# e.g. subreddit_prefix = "ed"
subreddit_prefix = "ed"

# Fourth, run the code by pressing ctrl+shift+F10

#==========================================================================================================================================================================================================================================

# When the code has finished, for each .csv file from step 1a, another file containing only the comments from the specified subreddit will be produced
# Repeat this code for each subreddit of interest

#==========================================================================================================================================================================================================================================

import csv, glob, pandas as pd
r_files = glob.glob("*.csv")

for file in r_files:
    print(file)
    data = []
    with open(file, 'rt', encoding='utf8') as input:
        reader = csv.reader(input)
        for line in reader:
            if line[2] == subreddit:
                if not line[1] == '2':  # Removes comments from the AutoModerator bot
                    data.append(line)
        output_df = pd.DataFrame(data, columns=["a_month", "b_author", "c_subreddit", "d_link_id", "e_body", "f_thread_id"])  # prints .csv file headers
        output_df.to_csv(subreddit_prefix+"_"+file, index=False, columns=("a_month", "b_author", "c_subreddit", "d_link_id", "e_body", "f_thread_id"))  # adds a new row to the .csv containing the extracted data

#==========================================================================================================================================================================================================================================