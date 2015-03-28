# feature_eng_avs_kaggle_20150322_v01
# Kaggle Feature Creation Script
# NOTE: must change credentials route run on local || aws connection

##IMPORTS
#import
import os
from datetime import datetime, date #for timing code

#basics
import pandas as pd
import numpy as np

#plot libraries
#%matplotlib inline
#import seaborn as sns
#from seaborn import plt

#plot default configuration for plots
#plt.rcParams['figure.figsize'] = 10, 7.5
#plt.rcParams['axes.grid'] = True

#for AWS connection
from boto.s3.connection import S3Connection
from IPython.parallel import Client

## =========================
## CONNECT TO AWS 
#get creds 
credentials = pd.read_csv('/Users/rychughes/.ssh/credentials.csv') #local
#credentials = pd.read_csv('/home/centos/certificates/credentials.csv') #AWS
aws_id = credentials['Access Key Id'][0]
aws_key = credentials['Secret Access Key'][0]

#connect to S3 for data
s3conn = S3Connection( aws_id , aws_key )
bucket = s3conn.get_bucket('avs-kaggle-data')

## =========================
## LOAD DATA 
#Transactions Data
keys = bucket.get_all_keys(prefix='reduced.csv.gz')
keys[0].get_contents_to_filename('reduced.csv.gz') #compressed file = 240mb, command hangs local machine... ~5 seconds on AWS
reduced_df = pd.read_csv('reduced.csv.gz',compression='gzip')
#print reduced_df.shape
#reduced_df.head(3)

#Offers Data
keys = bucket.get_all_keys(prefix='offers')
keys[0].get_contents_to_filename('offers.csv')
offers_df = pd.read_csv('offers.csv')
#print offers_df.shape
#offers_df.head(3)

#Train Data
keys = bucket.get_all_keys(prefix='trainHistory')
keys[0].get_contents_to_filename('trainHistory.csv')
X_train = pd.read_csv('trainHistory.csv')
#print X_train.shape
#X_train.head(3)

#Test Data
keys = bucket.get_all_keys(prefix='testHistory')
keys[0].get_contents_to_filename('testHistory.csv')
X_test = pd.read_csv('testHistory.csv')
#print X_test.shape
#X_test.head(3)

## MERGE DATA
#combine X_train and X_test for feature creation
X_combine = pd.concat([X_train, X_test])
#print X_combine.shape
#X_combine.head(1) #view train sample

#merge history with offer
X_combine = pd.merge( X_combine, offers_df, how='left', on=['offer'])
print X_combine.shape
X_combine.head(3) 

## =========================
## FUNCTIONS

# COUNT DAYS (HELPER FUNCTION)
def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

## FEATURE EXTRACTION
#Chitcode features - https://chitcode.wordpress.com/
#http://mlwave.com/predicting-repeat-buyers-vowpal-wabbit/
def extract_features( cust_id):
    cust_details = X_combine.ix[X_combine.id == cust_id,:] #gets 12-attributes for customer (1x12 list)
    #print cust_details
    
    #assign important variables for feature creation
    offer_category = cust_details.category.values[0]
    offer_company = cust_details.company.values[0]
    offer_brand = cust_details.brand.values[0]
    #print offer_category, offer_company , offer_brand 
    
    #get all transactions for customer
    trans_cust = reduced_df.ix[reduced_df.id == cust_id,:]
    #print trans_cust
    
    #define empty transaction to catch exceptions in feature creation
    empty_trans = pd.DataFrame({'id':0,'chain':0,'dept':0,'category':0,'company':0,'brand':0,'date':'2000-01-01',
                                'productsize':0,'productmeasure':'OO','purchasequantity':0,'purchaseamount':0.0},index=[1])  
    if trans_cust.shape[0] == 0:        
        trans_cust=empty_trans
    
    #dummy repeater for y_test... do this later
    #cust_details['repeater_true'] = 1 if cust_details.repeater.values[0]=='t' else 0 
    
    #summary values
    cust_details['offer_discount_per_item'] = cust_details.offervalue / cust_details.quantity
    cust_details['purchase_total_amount'] = trans_cust.purchaseamount.sum()
    cust_details['purchase_total_quantity'] = trans_cust.purchasequantity.sum() #these should be from COMPLETE (not reduced) dataset 

    
    #category
    cust_details['category_total_amount'] =   trans_cust.ix[trans_cust.category == offer_category,:].purchaseamount.sum()  
    cust_details['category_total_quantity'] = trans_cust.ix[trans_cust.category == offer_category,:].purchasequantity.sum()  
    cust_details['category_buy_true'] =  1 if trans_cust.ix[trans_cust.category == offer_category,:].purchasequantity.sum() > 0 else 0
    cust_details['category_share_spend'] = cust_details['category_total_amount'] / cust_details['purchase_total_amount']
    #company
    cust_details['company_total_amount'] =   trans_cust.ix[trans_cust.company == offer_company,:].purchaseamount.sum()  
    cust_details['company_total_quantity'] = trans_cust.ix[trans_cust.company == offer_company,:].purchasequantity.sum()  
    cust_details['company_buy_true'] =  1 if trans_cust.ix[trans_cust.company == offer_company,:].purchasequantity.sum() > 0 else 0
    cust_details['company_share_spend'] = cust_details['company_total_amount'] / cust_details['purchase_total_amount']
    #brand
    cust_details['brand_total_amount'] =   trans_cust.ix[trans_cust.brand == offer_brand,:].purchaseamount.sum()  
    cust_details['brand_total_quantity'] = trans_cust.ix[trans_cust.brand == offer_brand,:].purchasequantity.sum()  
    cust_details['brand_buy_true'] =  1 if trans_cust.ix[trans_cust.brand == offer_brand,:].purchasequantity.sum() > 0 else 0
    cust_details['brand_share_spend'] = cust_details['brand_total_amount'] / cust_details['purchase_total_amount']
    #print cust_details
    
    #Selected ML-Wave features go one layer deeper 
    #enter this code in later version
    #print cust_details

    #Ryan features
    cust_details['offer_discount_per_item'] = cust_details.offervalue / cust_details.quantity
    cust_details['purchase_total_amount'] = trans_cust.purchaseamount.sum()
    cust_details['purchase_total_quantity'] = trans_cust.purchasequantity.sum() #these should be from COMPLETE (not reduced) dataset     
    #print cust_details

    return cust_details


## GENERATE FEATURES FUNCTION
def generate_features( X_combine ): #requires formatted dataframe from above
	print "starting generate_features()"
	
	start_time = datetime.now() #for timing code
	X_features = pd.DataFrame() #new dataframe to write to
 
	#for e, cust_id in enumerate( X_combine.id.values): #complete dataset
	for e, cust_id in range(0,5): #complete dataset
        try: 
	        print e, cust_id
            X_features = pd.concat([X_features,extract_features(cust_id)]) #creating new df w/ features for each X_combine
	    except:
            print "error %" (%)
	        print '====='*10 #prints series of dashes to make errors "pop"
	        print 'Error at id', cust_id
	        break
		if e % 10 == 0:
			print e, datetime.now() - start
	print e, datetime.now() - start

	#print X_features.shape
	#X_features.head(3)

	#X_features = X_features.fillna(value=-1) #line in chitcode's script, ignoring for now

	#return
	X_features.to_csv('X_features.csv',index=False)
	#return X_features #wrote to csv, no need to return in python script

## =========================
## ACTION
generate_features( X_combine)


