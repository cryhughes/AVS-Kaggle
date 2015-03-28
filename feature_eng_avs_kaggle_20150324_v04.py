# feat_eng_avs_kaggle_20150323_v03.py
# 2015-03-23
# designed for local

## IMPORT
import os, string
import gzip
from datetime import datetime, date #for timing code
from collections import defaultdict

#basics
import pandas as pd
import numpy as np

#define data urls
gz_train = "/Users/rychughes/GA/data/trainHistory.csv.gz" 
gz_test =  "/Users/rychughes/GA/data/testHistory.csv.gz"
gz_offers = "/Users/rychughes/GA/data/offers.csv.gz"
gz_trans = "/Users/rychughes/GA/data/transactions-sample.csv.gz" #sample only (col headers are same)
#gz_trans = "/Users/rychughes/GA/data/reduced.csv.gz" #full

''' #no need for headers in actual script
#get headers 
headers_train = list( pd.read_csv( gz_train, compression='gzip', nrows=1).columns.values) 
headers_test = list( pd.read_csv( gz_test, compression='gzip', nrows=1).columns.values) 
headers_offers = list( pd.read_csv( gz_offers, compression='gzip', nrows=1).columns.values) 
headers_trans = list( pd.read_csv( gz_trans, compression='gzip', nrows=1).columns.values) 
'''

#create new dataset for train || test set 
testset_true = False
if testset_true:
	gz_history = gz_test 
	folder = "/Users/rychughes/GA/data/test/"
else: 
	gz_history = gz_train
	folder = "/Users/rychughes/GA/data/train/"
out_file = os.path.join(folder, "base_features.csv") #define outfile

#define feature_list for printing
feature_list = [\
				"offer_value","offer_id",\
				"purchases_total_quantity","purchases_total_amount",\
				"company_buy_true","company_total_quantity","company_total_amount",\
				"category_buy_true","category_total_quantity","category_total_amount",\
				"brand_buy_true","brand_total_quantity","brand_total_amount",\
				] 

#helper function for feature creation
def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

def generate_features( trans_file , out_file ):
	print "running generate_features()..."
	#keep diction with offer data
	offers = {}
	offers_categories = {}
	offers_companies = {}
	for e, line in enumerate( gzip.open( gz_offers) ):
		row = line.strip().split(",")
		offers[ row[0]] = row			#assign 
		offers_categories[ row[1]] = 1
		offers_companies[ row[3]] = 1
	print "completed loop for offers data. Offers len: " + str(len(offers))
	
	#keep dictionary with history data
	ids = {}
	for e, line in enumerate( gzip.open(gz_history)):
		if e > 0:	
			#skip header
			row = line.strip().split(",")
			ids[row[0]] = row
	print "completed loop for history data. Cust Ids len: " + str(len(ids))

	seen_ids = set([])

	outfile = open(out_file, "wb")
	outfile.write("repeattrue repeattrips id" + string.join(feature_list)+"\n") 

	#iterate through (reduced) transactions dataset
	#KEY NOTE: transactions dataset appears to be grouped by cust_id, cust_id 86246 for 900+ consecutive rows
	last_id = 0
	features = defaultdict(float)
	for e, line in enumerate( gzip.open(gz_trans)):
		#skip header
		if e > 0:
			row = line.strip().split(",")
			## ==================
			## write features to out-file for complete cust_id
			if last_id != row[0] and e != 1: #write features when we get to a new shopper id
				#generate aggregated features here
				#...
				
				#write outline for customer
				outline = "" #define empty line
				if testset_true:
					outline += "=999 -999 " + str(last_id) #set default testset values to -999
				else: 
					outline += str(features['repeattrue'])+ " " + str(features['repeattrips']) + " " + str(last_id)
				for f in features:
					#if f in features:
						outline += " "+str(features[f])
					#else:
					#	outline += " 0" #set default to zero if feature NOT created
				outline += "\n"
				outfile.write( outline ) #end line and output 
				seen_ids.add(last_id)

				#record successfully written cust_ids (test w/ transactions-sample):
				print "cust id: " +str(last_id) + " written! "
				#print " -nbr features: " + str(len(features))
				#print " -features: " +str(features)

				#reset features for new row (cust_id)
				features = defaultdict(float)
			
			## ==================
			## enter for-loop for almost ALL new lines here
			#check if we have a valid sample
			if row[0] in ids: 
				#generate cust_hist
				cust_hist = ids[row[0]]
				if not testset_true:
					if ids[row[0]][5] =="t":
						features['repeattrue'] = 1
						features['repeattrips'] = ids[row[0]][6]
					else:
						features['repeattrue'] = 0
						features['repeattrips'] = 0

				offervalue = offers[ cust_hist[2] ][4]
				features['offer_value'] = offers[ cust_hist[2] ][4]
				features['offer_id'] = cust_hist[2]
				
				features['purchases_total_quantity'] += float( row[10] )
				features['purchases_total_amount'] += float( row[10] )
				#company		
				if offers[ cust_hist[2] ][3] == row[4]:
					features['company_buy_true'] += 1.0
					features['company_total_quantity'] += float( row[9] )
					features['company_total_amount'] += float( row[10] )
				#category 
				if offers[ cust_hist[2] ][1] == row[3]:
					features['category_buy_true'] += 1.0
					features['category_total_quantity'] += float( row[9] )
					features['category_total_amount'] += float( row[10] )
				#brand
				if offers[ cust_hist[2] ][5] == row[5] and (row[3] in offers_categories or row[4] in offers_companies):
					features['brand_buy_true'] += 1.0
					features['brand_total_quantity'] += float( row[9] )
					features['brand_total_amount'] += float( row[10] )
			
			#break if NOT valid sample
			#else:
			#	print '====='*10 #prints series of dashes to make errors "pop"
		    #    print 'Error at e', e, row[0]
		        #break
			
			last_id = row[0] #set cust_id to row, for comparing to next line

			#write progress for tracking
			if e % 100000 == 0:
				print e 
	print "completed loop for transaction data. Total rows: " + str(e)


	# do stuff for ids without transactions
	allids = set(ids.keys())
	unseen_ids = allids.difference(seen_ids)
	for ui in unseen_ids:
		#do more stuff
		outline = ""
		outline += "\n"
		outfile.write( outline)
	print "completed loop for unseen_ids... Total unseen_ids: " +str(len(unseen_ids))

	'''
	#print features list
	for f in features:
		print features[f]
	#print "printed list of feature names to terminal"
	'''

#actions
if __name__ == '__main__':
	generate_features( gz_trans , out_file)			

