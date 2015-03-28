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
#
'''#get headers 
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
#define global variables
ids = {}
#features = defaultdict(float) #function is better if variable kept local
#define feature_list for printing
feature_list = [\
				"offer_id","offer_value", \
				"purchases_total_quantity","purchases_total_amount", "purchases_avg_price_per_item", \
				"purchase"
				"company_buy_true","company_total_quantity","company_total_amount", "company_share_wallet", \
				
				"category_buy_true","category_total_quantity","category_total_amount", "category_share_wallet", \
				
				"brand_buy_true","brand_total_quantity","brand_total_amount", "brand_share_wallet", \
				
				] 
#transform feature list into csv format for export
csv_feature_list_str = ""
for f in feature_list:
	csv_feature_list_str += ", " + f 
#define path and write first line 
out_file = os.path.join(folder, "base_features.csv") #define outfile
outfile = open(out_file, "wb")
outfile.write("repeattrue, repeattrips, id " + csv_feature_list_str + "\n") #write first line of outfile
#helper function for feature creation: time_features
def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days
#helper function to prevent divide-by-zero errors
def zidz( numerator, denominator):
	if denominator <= 0:
		return 0
	return numerator / denominator
#helper function for writing features to file
def write_features_to_outline( id_nbr , features ):
	outline = "" #define empty line
	if testset_true:
		outline += "-999, -999, " + str(id_nbr)  #set default testset values to -999
	else: 
		outline += str(features['repeattrue'])+ ", " + str(features['repeattrips']) + ", " + str(id_nbr)
	#write features
	for f in feature_list:
		if f in features:
			outline += ", "+str(features[f]) #write feature
		else:
			outline += ", 0" #set default to zero if feature NOT created
	if id_nbr in ids:
		outline += " "+ids[id_nbr][3] #chain
		outline += " "+ids[id_nbr][1] #market		
	outline += "\n"
	outfile.write( outline ) #end line and output 
	#test
	#print "cust_id: " + str(id_nbr) + " features: " + str(features)
	#print "cust_id: " + str(id_nbr) + " outline: " + outline
	#
#function to generate features for file
def generate_features( trans_file , out_file ):
	print "running generate_features()..."
	#load offers data
	print "starting loop of offers data..."
	#keep diction with offer data
	offers = {}
	offers_categories = {}
	offers_companies = {}
	for e, line in enumerate( gzip.open( gz_offers) ):
		row = line.strip().split(",")
		offers[ row[0]] = row			#assign 
		offers_categories[ row[1]] = 1
		offers_companies[ row[3]] = 1
		#print offers_categories
	print "completed loop for offers data. Offers len: " + str(len(offers))
	#load history data
	print "starting loop of history (train/test) file..." 
	ids = {} 	#keep dictionary with history data
	for e, line in enumerate( gzip.open(gz_history)):
		if e > 0:	
			#skip header
			row = line.strip().split(",")
			ids[row[0]] = row
	print "completed loop for history data. Cust Ids len: " + str(len(ids))
	#load transactions data... AND create features
	print "starting loop of transactions file..."
	#reset local variables
	last_id = 0
	features = defaultdict(float) #cannot be local variable OR other functions will not have access to its values
	seen_ids = set([])
	#iterate through (reduced) transactions dataset #KEY NOTE: transactions dataset appears to be grouped by cust_id, cust_id 86246 for 900+ consecutive rows
	for e, line in enumerate( gzip.open(gz_trans)):
		#skip header
		if e > 0:
			row = line.strip().split(",") #row is attributes from transaction
			## ==================
			## write features to out-file for complete cust_id
			if last_id != row[0] and e != 1: #write features when we get to a new shopper id
				#generate aggregated features here
				#purchase
				features['purchases_avg_price_per_item'] = zidz(features['purchases_total_amount'], features['purchases_total_quantity'])  
				#company
				features['company_buy_true'] = 1 if features['company_total_quantity'] > 0 else 0
				features['company_share_wallet'] = zidz( features['company_total_amount'], features['purchases_total_amount']) 
				#category
				features['category_buy_true'] = 1 if features['category_total_quantity'] > 0 else 0
				features['category_share_wallet'] = zidz( features['category_total_amount'], features['purchases_total_amount']) 
				#brand
				features['brand_buy_true'] = 1 if features['brand_total_quantity'] > 0 else 0
				features['brand_share_wallet'] = zidz( features['brand_total_amount'], features['purchases_total_amount']) 
				#write out to file
				#print "writing features for complete cust_id. e: " + str(e) + " last_id: " + str(last_id)  + " row: " + str(row[0])  
				write_features_to_outline( last_id, features ) 	#write features to outline
				seen_ids.add( last_id ) 			#record successfully written 
				features = defaultdict(float) 		#reset features for new row (cust_id)
			## ==================
			# check if cust_id in test/train, then += feature vars for each transaction
			if row[0] in ids: 
				#generate cust_hist
				cust_hist = ids[row[0]]
				if not testset_true:
					if cust_hist[5] =="t":
						features['repeattrue'] = 1
						features['repeattrips'] = ids[row[0]][4]
					else:
						features['repeattrue'] = int(0)
						features['repeattrips'] = int(0)
				#offer details
				features['offer_id'] = cust_hist[2]
				features['offer_value'] = offers[ cust_hist[2] ][4]
				#totals
				features['purchases_total_quantity'] += float( row[9] )
				features['purchases_total_amount'] += float( row[10] )
				#company		
				if offers[ cust_hist[2]] [3] == row[4]:
					features['company_total_quantity'] += float( row[9] )
					features['company_total_amount'] += float( row[10] )
				#category 
				if offers[ cust_hist[2] ][1] == row[3]:
					features['category_total_quantity'] += float( row[9] )
					features['category_total_amount'] += float( row[10] )
				#brand
				if offers[ cust_hist[2] ][5] == row[5]:
					features['brand_total_quantity'] += float( row[9] )
					features['brand_total_amount'] += float( row[10] )
			#set last_id to control for-loop work-flow
			last_id = row[0]
			# ==================
			#write progress for tracking, 29M transactions in "reduced.csv.gz"
			if e % 1000000 == 0:
				print "rows in transactions files processed: " + str(e) 
	print "completed loop for transaction data. Total rows: " + str(e)
	# do stuff for ids without transactions
	allids = set(ids.keys())
	unseen_ids = allids.difference(seen_ids)
	#loop through unseen_ids
	print "starting loop for unseen_ids..."
	for ui in unseen_ids:
		cust_hist = ids[ui]
		#offer details
		features['offer_value'] = offers[ cust_hist[2] ][4]
		features['offer_id'] = cust_hist[2]		
		#write 
		write_features_to_outline( ui, features)
		features = defaultdict(float) 		#reset features for new row (cust_id)
	print "completed loop for unseen_ids. seen_ids: " + str(len(seen_ids)) + " unseen_ids: " +str(len(unseen_ids)) 
	#complete for loop thorugh transactions data
	print "complete loop through transactions data. Total rows: " + str(e)

#actions
if __name__ == '__main__':
	generate_features( gz_trans , out_file)			
	#run both datasets
	testset_true = True
	generate_features( gz_trans , out_file)			

