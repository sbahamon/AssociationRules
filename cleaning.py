import pandas as pd
import numpy as np
from orangecontrib.associate.fpgrowth import *  


#reads in data
trans = pd.read_csv('trnsact.csv',
                	header = None,
                	index_col = False,
                	usecols = [0 ,1, 2, 5, 6],
                	names = ['SKU', 'STORE', 'REGISTER', 'SALEDATE', 6],
                	parse_dates = ['SALEDATE'],
                	dtype={'SKU': np.int32, 'STORE': np.int32,
                	'REGISTER': np.int32},
                	nrows = 12000000)
               	 
trans = trans[trans[6] == 'P']
del trans[6]              	 
 
#cleaning data to 2 column key and sku
trans = trans[trans['SALEDATE'] > "2005-07-26"]
trans['KEY1'] = trans['STORE'] + trans['REGISTER']
trans['KEY'] = trans['KEY1'] + trans['SALEDATE']
del trans['STORE'], trans['REGISTER'], trans['KEY1'], trans['SALEDATE']


trans = trans.reset_index() #reset index
del trans['index']
baskets = list(trans['SKU'].groupby(trans['KEY'])) #groups skus by key
baskets = [el[1:] for el in baskets] #converts tuples to list


#splits up individual baskets
for i in range(len(baskets)):
   baskets[i] = list( baskets[i] )
   grouping = baskets[i]
   baskets[i] = [c for c in grouping[0]]
del i, grouping


#saves to csv
#bdf = pd.DataFrame(baskets)
#bdf.to_csv('baskets.csv', index = False, header = False)


#apriori
itemsets = frequent_itemsets(baskets, 500)
rules = association_rules(itemsets, .6)
