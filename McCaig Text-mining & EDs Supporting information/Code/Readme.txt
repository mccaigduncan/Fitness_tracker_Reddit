Code prepared by Duncan McCaig (d.mccaig@warwick.ac.uk) Dec 2017-Jan 2018 - please do not hesitate to contact if any problems with the code are encountered
# Written using Python 3.6.3. (64-bit) - due to size of data, 64-bit version of Python might be necessary
# Supporting information to IJED article submission ("Fitness tracking technology and online communities")
#==========================================================================================================================================================================================================================================

Overview of code in folders:

1) "1_data_extraction"
- 1a extracts all comments for specified subreddits from .bz2 files
- If extracting from multiple subreddits, 1b can used afterwards to separate the subreddits into separate files

2) "2_concatenation_threads"
- Concatenates all comments in a subreddit into threads (i.e. all comments that responded to the same inital post)