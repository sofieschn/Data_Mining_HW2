
def read_transactions(filename):
    bucket = []

    with open(filename, 'r') as file:
        for line in file:
            transaction = set(map(int, line.strip().split()))
            bucket.append(transaction)

    return bucket

## data
filename = 'T10I4D100K.dat'
transactions = read_transactions(filename)

## testing testing
#for i, transaction in enumerate(transactions, start=1):
    #print(f"Transaction {i}: {transaction}")