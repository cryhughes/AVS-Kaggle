# feat_eng_avs_kaggle_20150323_v03.py
# 2015-03-23
# designed for local

## IMPORT
import os
import gzip
from datetime import datetime, date #for timing code

#basics
import pandas as pd
import numpy as np

#define data urls
gz_train = "/Users/rychughes/GA/data/trainHistory.csv.gz" 
gz_test =  "/Users/rychughes/GA/data/testHistory.csv.gz"
gz_offers = "/Users/rychughes/GA/data/offers.csv.gz"
gz_trans = "/Users/rychughes/GA/data/reduced.csv.gz" #note, sample only

#create new dataset for train || test set 
testset_true = False
if testset_true:
	gz_history = gz_test 
	folder = "/Users/rychughes/GA/data/test/"
else: 
	gz_history = gz_train
	folder = "/Users/rychughes/GA/data/train/"
out_file = os.path.join(folder, "base_features.csv") #define outfile

#define feature_list
feature_list = [""] #TBC

def generate_features( trans_file , out_file ):
	print "running generate_features()..."
	#keep a diction with the offer data
	offers = {}
	offers_categories = {}
	offers_companies = {}
	for e, line in enumerate( gzip.open( gz_offers) ):
		print e 
		row = line.strip().split(",")
		offers[ row[0]] = row			#assign 
		offers_categories[ row[1]] = 1
		offers_companies[ row[3]] = 1
	print "completed loop for offers data..."
	
	#keep dictionary from history data
	for e, line in enumerate( open(gz_offers)):
		if e > 0:	
			#skip header
			row = line.strip().split(",")
			id[row[0]] = row
	print "completed loop for history data..."

	seen_ids = set([])

	outfile = open(out_file, "wb")
	outfile.write("label repeattrips id" + string.join(feature_list)+"market chain\n") 

	#iterate through reduced dataset
	last_id = 0
	features = defaultdict(float)
	for e, line in enumerate( open(gz_trans)):
		#skip header
		if e > 0:
			row = line.strip().split(",")
			if last_id != row[0] and e != 1: #write away the features when we get to a new shopper id
				#generate features here
				#...
				x=0
			#check if we have a valid sample
			if row[0] in ids: 
				#generate label and history
				#do more here... 
				x=0
			last_id = row[0]

			#write progress for tracking
			if e % 100000 == 0:
				print e 
	# do stuff for ids without transactions
	allids = set(ids.keys())
	unseen_ids = allids.difference(seen_ids)
	for ui in unseen_ids:
		#do more stuff
		x=0

#actions
if __name__ == '__main__':
	generate_features( gz_trans , out_file)			

