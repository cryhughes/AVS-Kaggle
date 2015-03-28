AVS-Kaggle
Acquire Valued Shopper Challenge Kaggle Competition: 
https://www.kaggle.com/c/acquire-valued-shoppers-challenge

PREDICTION PROBLEM:
1. Predict the probability a customer will become a repeat purchaser, given they made an initial purchase AFTER being provided a marketing offer 

DATA
The total transaction dataset is 22gb. This is my first effort working with a dataset this large. (SPOILER: the learning curve is pretty steep!)

DATA REDUCTION
To make data exploration and algorithm developement more manageable, I reduced the dataset to only the transactions that match one of the products/companies where we an offer was presented to customers. This reduces the dataset from 22gb to ~1.5gb (240mb gzipped). Credit to "breakfast pirate" for the first post on the concept (and a tasty alias name): 
http://www.kaggle.com/c/acquire-valued-shoppers-challenge/forums/t/7666/getting-started-data-reduction/

I was able to reduce the dataset 
-Data reduction scripts did not work with iPython notebook on local (file to large) 
-Data reduction scripts did not work with iPython notebook on AWS EC2 (keep disconnecting) 
-Data reduction script with python on local succeeded. Script based on: Auduno's repository: https://github.com/auduno/Kaggle-Acquire-Valued-Shoppers-Challenge

TO expedite testing for feature development and prediction modeling, I have used a smaller datasets with all of the transactions for 4 ONLY 4 customers (2 in trainset, 2 in testset). Hat tip to Vadim Kyssa for the dataset: http://www.kaggle.com/c/acquire-valued-shoppers-challenge/forums/t/7659/sample-of-transaction-data

DATA EXPLORATION / FEATURE ENGINEERING 
Data exploration does not yeild very much on its own, adding features to increase how interesting it is

FEATURES TO BE DEVELOPED:
-Company_Purchase_True, Company_Purchase_Quantity, Company_Purchase_Amount, Company_Share_Wallet, 
-Category_Purchase_True, Category_Purchase_Quantity, Category_Purchase_Amount, Category_Share_Wallet
-Brand_Purchase_True, Brand_Purchase_Quantity, Brand_Purchase_Amount, Brand_Share_Wallet
-Total_Puchase_Quantity, Total_Purchase_Amount, Average_Cost_Purchase
-Time variables: Company / Category / Brand purchases within past 30, 60, 90, 180 days

concerns about feature: 
-Multicolinnearity (especially between time variables) could lead to over-fitting.
-Share of wallet metric biased, because ONLY analyzing transactions for products where the company/category made an offer 

PREDUCTION MODEL
HOLDING FOR FEATURE ENGINEERING

prediction models to be explored
-Logistic Regression
-KNN
-Decision Tree Classification
-... suggestions?

concerns models
-Computationally expensive... suggestions?

For reference, there is a great discussion on feature engineering my mlwave here: 
http://mlwave.com/predicting-repeat-buyers-vowpal-wabbit/

ALGORITHM DEVELOPMENT
HOLIDNG FOR DATA EXPLORATION - Iterative developemnt w/ FEATURE-ENGINEERING

SUBMSSION
This is a big-data learning exercise for my personal development. 
I plan to produce a final set of results, and compare my results to the leaderboard 

submission leaderboard (scores range between 0.44-0.63):
https://www.kaggle.com/c/acquire-valued-shoppers-challenge/leaderboard

