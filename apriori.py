import os
from itertools import combinations
from collections import defaultdict

def read_dataset(file_path):
    """Reads the dataset and returns it as a list of transactions."""
    print("Reading dataset...")
    with open(file_path, 'r') as file:
        transactions = [line.strip().split() for line in file]
    print(f"Dataset loaded with {len(transactions)} transactions.")
    return transactions

def get_itemset_support(transactions, itemsets):
    """Calculates the support for each itemset in the transactions."""
    itemset_support = defaultdict(int)
    for transaction in transactions:
        transaction_set = set(transaction)
        for itemset in itemsets:
            if transaction_set.issuperset(itemset):
                itemset_support[itemset] += 1
    return itemset_support

def generate_candidates(frequent_itemsets, k):
    """Generates candidate itemsets of size k+1 using only frequent itemsets of size k."""
    candidates = set()
    frequent_items = list(frequent_itemsets.keys())
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            itemset1, itemset2 = frequent_items[i], frequent_items[j]
            # Join only if first k-1 items are the same
            if itemset1[:k - 1] == itemset2[:k - 1]:
                candidate = tuple(sorted(set(itemset1).union(itemset2)))
                candidates.add(candidate)
    return list(candidates)

def filter_itemsets_by_support(itemset_support, min_support):
    """Filters itemsets based on minimum support threshold."""
    return {itemset: support for itemset, support in itemset_support.items() if support >= min_support}

def apriori(transactions, min_support):
    """Runs the optimized A-Priori algorithm to find all frequent itemsets."""
    print(f"Starting A-Priori algorithm with minimum support = {min_support}")
    
    # Generate initial candidates (single items)
    items = {item for transaction in transactions for item in transaction}
    current_itemsets = [tuple([item]) for item in sorted(items)]
    
    all_frequent_itemsets = {}
    k = 1
    
    while current_itemsets:
        print(f"Generating frequent itemsets of size {k}...")
        
        # Get support for current itemsets
        itemset_support = get_itemset_support(transactions, current_itemsets)
        
        # Filter by min support
        frequent_itemsets = filter_itemsets_by_support(itemset_support, min_support)
        print(f"Found {len(frequent_itemsets)} frequent itemsets of size {k}.")
        
        all_frequent_itemsets.update(frequent_itemsets)
        
        # Generate next level of candidates using only frequent itemsets
        current_itemsets = generate_candidates(frequent_itemsets, k)
        k += 1
        
        # Reduce transactions by filtering out irrelevant ones
        if k > 2:
            transactions = [t for t in transactions if any(set(itemset).issubset(t) for itemset in current_itemsets)]
    
    print("A-Priori algorithm completed.")
    return all_frequent_itemsets

def main():
    # Dynamically find the dataset file path in the current directory or subdirectories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'T10I4D100K.dat')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at {file_path}")
    
    min_support = 1000  # Example minimum support threshold
    
    transactions = read_dataset(file_path)
    frequent_itemsets = apriori(transactions, min_support)
    
    print("\nFrequent Itemsets with their supports:")
    for itemset, support in frequent_itemsets.items():
        print(f"{itemset}: {support}")

if __name__ == "__main__":
    main()
