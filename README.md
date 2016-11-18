# A simple tweets crawler
A streaming tweets crawler for collecting tweets related to 2016 US presidential election.

## Install dependencies
`pip install -r requirements.txt`

## How were the keywords generated?
1. Count the frequency of 1-gram and 2-gram in the recently collected data.
2. From the most frequent 1000 1-gram and the most frequent 1000 2-gram, manually select keywords that are related to the presidential election.
  * Remove the words that are obviously too general (e.g. vote, win, debate, etc.).
  * Search rest of the frequent keywords in Twitter, observe the search result to see if most of them are related to the election.
  * Search Twitter at https://twitter.com/search?f=tweets&vertical=news&q={query} (login required) - replace {query} with the keyword.
