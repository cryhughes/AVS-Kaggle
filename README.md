AVS-Kaggle
Acquired Valued Shopper Challenge Kaggle Competition: 
https://www.kaggle.com/c/acquire-valued-shoppers-challenge

PREDICTION PROBLEM:\n
1. Predict the probability a customer will make a purchase, if provided a marketing offer (not part of Kaggle competition)
2. Predict the probability a customer will become a repeat purchaser, give they made an initial purchase AFTER being provided a marketing offer  

DATA
The total transaction dataset is 22gb. Very big. (Especially for me...)

DATA REDUCTION
To make the initial data exploration and algorithm developement more manageable, I will reduce the dataset to only the relevant products/companies where we have data on the offers presented to customers. This reduces the dataset from 22gb to ~1gb (240mb compressed). Credit to "breakfast pirate" for the first post on the concept (and a tasty alias name): 
http://www.kaggle.com/c/acquire-valued-shoppers-challenge/forums/t/7666/getting-started-data-reduction/

I encountered some problems reducing the dataset, but evenutally succeeded by switching from ipython NB to python script 
-Data reduction scripts did not work with iPython notebook on local (file to large) 
-Data reduction scripts did not work with iPython notebook on AWS EC2 (keep disconnecting) 
-Data reduction script with python on local succeeded. Script based on: Auduno's repository: https://github.com/auduno/Kaggle-Acquire-Valued-Shoppers-Challenge

DATA EXPLORATION
WORK IN PROGRESS - Will post a summary of any noteworhy findings here...

FEATURE ENGINEERING
HOLDING FOR DATA EXPLORATION 

For reference, there is a great discussion on feature engineering my mlwave here: 
http://mlwave.com/predicting-repeat-buyers-vowpal-wabbit/

ALGORITHM DEVELOPMENT
HOLIDNG FOR DATA EXPLORATION - Iterative developemnt w/ FEATURE-ENGINEERING

SUBMSSION
This is a big-data learning exercise for my personal development. 
I plan to produce a final set of results, and compare my results to the leaderboard 

Submission leaderboard (scores range between 0.44-0.63):
https://www.kaggle.com/c/acquire-valued-shoppers-challenge/leaderboard

