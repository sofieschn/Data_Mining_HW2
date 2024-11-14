# apriori.py
from collections import defaultdict
from itertools import combinations


## we generate candidate itemsets of size k by combining frequent itemsets of the size k-1
## what we check is the size of the itemsets filtering them by length to ensure only valid candidates are considered for the next level.
def generate_cand(frequent_itemsets, k) :
    candidates = set() # set to store candidates
    frequent_itemsets = list(frequent_itemsets) # convert set to list for indexing 

    # generate combinations of itemsets to find new candidates
    for i in range(len(frequent_itemsets)): # for each item..
        for j in range(i+1, len(frequent_itemsets)): # compare with rest of items..
            candidate = frequent_itemsets[i] | frequent_itemsets[j] # combine itemsets i and j
            if len(candidate) == k: # if the candidate size matches the desired size k
                candidates.add(candidate) # add to set 
    return candidates # return set of candidates


## iterate each transaction an check is each candidate item is a subset of that transaction
## when we find a candidate itemset present in a transaction, we increase the support counter
## the output is : the number of transactions in which the itemset appears
def count_support(transactions, candidates) :
    support_counts = defaultdict(int)

    # loop through each transaction and each candidate 
    for transaction in transactions: # for each transaction...
        for candidate in candidates:  # check each candidate..
            if candidate.issubset(transaction): # in case we find the candidate in the transaction
                support_counts[candidate] +=1 # we add 1 to the support counter 
    return support_counts # and then reuturn


## we create a filter so only the itemsets surpassing the support threshold are included and the rest filtered out
def filter_itemsets_by_support(support_counts, min_support) : 
    # keep only itemsets meeting the minimum support
    surpassing_threshold = {itemset: count for itemset, count in support_counts.items() if count >= min_support}
    return surpassing_threshold


##### Apriori function, using all above functions

##     Run the A-Priori algorithm to find all frequent itemsets with support >= min_support.

def apriori(transactions, min_support):
    # Step 1: Generate 1-itemsets and count their support
    support_counts = defaultdict(int) 
    for transaction in transactions: 
        for item in transaction:
            support_counts[frozenset([item])] += 1

    # Filter 1-itemsets by minimum support
    frequent_itemsets = filter_itemsets_by_support(support_counts, min_support)
    all_frequent_itemsets = frequent_itemsets.copy()  # Store all levels of frequent itemsets

    # Step 2: Iteratively generate larger frequent itemsets
    k = 2  # Starting from 2-itemsets
    while frequent_itemsets:
        # Generate candidate itemsets of size k
        candidates = generate_cand(frequent_itemsets.keys(), k)
        
        # Count support for each candidate
        support_counts = count_support(transactions, candidates)
        
        # Filter candidates by minimum support to get new frequent itemsets
        frequent_itemsets = filter_itemsets_by_support(support_counts, min_support)
        
        # Add new frequent itemsets to the all_frequent_itemsets dictionary
        all_frequent_itemsets.update(frequent_itemsets)
        
        # Increment k for the next iteration (move to k+1 itemsets)
        k += 1

    return all_frequent_itemsets
