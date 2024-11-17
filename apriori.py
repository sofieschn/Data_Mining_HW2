import os
from itertools import combinations
from collections import defaultdict

def read_dataset(file_path):
    """
    Reads the dataset and returns it as a list of transactions.
    Each line in the file represents a transaction with items separated by spaces.

    Args:
        file_path (str): Path to the dataset file.
    
    Returns:
        transactions (list of list of str): List of transactions, each transaction is a list of items.
    """
    print("Reading dataset...")
    with open(file_path, 'r') as file:
        transactions = [line.strip().split() for line in file]
    print(f"Dataset loaded with {len(transactions)} transactions.")
    return transactions

def get_itemset_support(transactions, itemsets):
    """
    Calculates the support count for each itemset in the given list of transactions.

    Args:
        transactions (list of list of str): List of transactions.
        itemsets (list of tuple): List of itemsets to calculate support for.
    
    Returns:
        itemset_support (dict): Dictionary mapping itemsets to their support counts.
    """
    itemset_support = defaultdict(int)
    for transaction in transactions:
        transaction_set = set(transaction)  # Convert transaction to a set for faster subset checking
        for itemset in itemsets:
            if transaction_set.issuperset(itemset):  # Check if transaction contains the itemset
                itemset_support[itemset] += 1
    return itemset_support

def generate_candidates(frequent_itemsets, k):
    """
    Generates candidate itemsets of size k+1 from frequent itemsets of size k.

    Args:
        frequent_itemsets (dict): Dictionary of frequent itemsets and their support.
        k (int): Current size of frequent itemsets.
    
    Returns:
        candidates (list of tuple): List of candidate itemsets of size k+1.
    """
    candidates = set()
    frequent_items = list(frequent_itemsets.keys())
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            itemset1, itemset2 = frequent_items[i], frequent_items[j]
            # Combine itemsets if the first k-1 items are the same
            if itemset1[:k - 1] == itemset2[:k - 1]:
                candidate = tuple(sorted(set(itemset1).union(set(itemset2))))
                candidates.add(candidate)
    return list(candidates)

def filter_itemsets_by_support(itemset_support, min_support):
    """
    Filters itemsets that meet or exceed the minimum support threshold.

    Args:
        itemset_support (dict): Dictionary of itemsets and their support counts.
        min_support (int): Minimum support threshold.
    
    Returns:
        filtered_itemsets (dict): Dictionary of itemsets meeting the minimum support.
    """
    return {itemset: support for itemset, support in itemset_support.items() if support >= min_support}

def apriori(transactions, min_support):
    """
    Implements the A-Priori algorithm to find all frequent itemsets with support >= min_support.

    Args:
        transactions (list of list of str): List of transactions.
        min_support (int): Minimum support threshold.
    
    Returns:
        all_frequent_itemsets (dict): Dictionary of all frequent itemsets and their support counts.
    """
    print(f"Starting A-Priori algorithm with minimum support = {min_support}")
    
    # Start with single-item candidates
    items = {item for transaction in transactions for item in transaction}
    current_itemsets = [tuple([item]) for item in sorted(items)]
    
    all_frequent_itemsets = {}
    k = 1
    
    while current_itemsets:
        print(f"Generating frequent itemsets of size {k}...")
        
        # Calculate support for current itemsets
        itemset_support = get_itemset_support(transactions, current_itemsets)
        
        # Filter itemsets by support
        frequent_itemsets = filter_itemsets_by_support(itemset_support, min_support)
        print(f"Found {len(frequent_itemsets)} frequent itemsets of size {k}.")
        
        all_frequent_itemsets.update(frequent_itemsets)
        
        # Generate candidates for the next size
        current_itemsets = generate_candidates(frequent_itemsets, k)
        k += 1
        
        # Optional optimization: Filter irrelevant transactions for larger itemsets
        if k > 2:
            transactions = [t for t in transactions if any(set(itemset).issubset(t) for itemset in current_itemsets)]
    
    print("A-Priori algorithm completed.")
    return all_frequent_itemsets

def generate_association_rules(frequent_itemsets, min_confidence, transactions_count):
    """
    Generates association rules from frequent itemsets with confidence >= min_confidence.

    Args:
        frequent_itemsets (dict): Dictionary of frequent itemsets and their support counts.
        min_confidence (float): Minimum confidence threshold.
        transactions_count (int): Total number of transactions.
    
    Returns:
        rules (list of tuple): List of association rules in the form (antecedent, consequent, support, confidence).
    """
    print(f"\nGenerating association rules with minimum confidence = {min_confidence}")
    rules = []
    
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue  # Rules require at least two items
        
        itemset_support = frequent_itemsets[itemset]  # Support for the entire itemset
        subsets = [tuple(sorted(comb)) for i in range(1, len(itemset)) for comb in combinations(itemset, i)]
        
        for antecedent in subsets:
            consequent = tuple(sorted(set(itemset) - set(antecedent)))
            if not consequent:
                continue
            
            antecedent_support = frequent_itemsets.get(antecedent, 0)
            confidence = itemset_support / antecedent_support  # Confidence of the rule
            
            if confidence >= min_confidence:
                rules.append((antecedent, consequent, itemset_support, confidence))
    
    print(f"Generated {len(rules)} rules.")
    return rules

def main():
    """
    Main function to run the A-Priori algorithm and generate association rules.
    """
    # Find the dataset file path dynamically
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'T10I4D100K.dat')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at {file_path}")
    
    min_support = 1000  # Minimum support threshold
    min_confidence = 0.6  # Minimum confidence threshold
    
    # Load the dataset
    transactions = read_dataset(file_path)
    
    # Run A-Priori algorithm to find frequent itemsets
    frequent_itemsets = apriori(transactions, min_support)
    
    print("\nFrequent Itemsets with their supports:")
    for itemset, support in frequent_itemsets.items():
        print(f"{itemset}: {support}")
    
    # Generate association rules
    transactions_count = len(transactions)
    association_rules = generate_association_rules(frequent_itemsets, min_confidence, transactions_count)
    
    print("\nAssociation Rules:")
    for antecedent, consequent, support, confidence in association_rules:
        print(f"{antecedent} -> {consequent} (Support: {support}, Confidence: {confidence:.2f})")

if __name__ == "__main__":
    main()
