from operator import itemgetter

def read_input():
    min_support = input()
    transaction_DB = {} # use a dictionary to store the inputs, key is the transaction number, value is the item list
    counter = 1
    line = input()
    while line != '':
        line = line.split(' ')
        transaction_DB[counter] = line
        counter += 1
        line = input()
    return min_support, transaction_DB

# This function is usde to extract L1 from transaction DB
def extract_L1(min_support, transaction_DB):
    item_occurance = {}
    for key in transaction_DB.keys():
        for item in transaction_DB[key]:
            if item in item_occurance.keys():
                item_occurance[item] += 1
            else:
                item_occurance[item] = 1
    L1 = []
    for item in item_occurance.keys():
        if int(item_occurance[item]) >= int(min_support):
            L1.append([item])
    return L1        

# Check if list1 is a subset of list2
def isSubset(list1, list2):
    set_list1 = set(list1)
    set_list2 = set(list2)
    if len(set_list1 - set_list2) == 0:
        return True
    else:
        return False

# This function serves cartisian_product(), it returns the union of two lists
def combine_lists(list1, list2):
    set_list1 = set(list1)
    set_list2 = set(list2)
    union = list1 + list(set_list2 - set_list1)
    union.sort()
    return union

# to remove duplicate elements 
def Remove_duplicate(list_with_duplicate): 
    final_list = [] 
    for num in list_with_duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

# Use L(k-1) to get C(k), note that L(k-1) and C(k) are both list of list
def cartisian_product(Lk_minus_1, k):
    C_k = []
    for i in range(len(Lk_minus_1) - 1):
        for j in range(i+1, len(Lk_minus_1)):
            new_list = combine_lists(Lk_minus_1[i], Lk_minus_1[j])
            if len(new_list) == k:
                new_list.sort()
                C_k.append(new_list)
    C_k = Remove_duplicate(C_k)
    return C_k

# This function is used to count the number of occurance of a certain pattern
def count_pattern_occurance(pattern, transaction_DB):
    set_pattern = set(pattern)
    counter = 0
    for key in transaction_DB.keys():
        set_transaction = set(transaction_DB[key])
        if len(set_pattern - set_transaction) == 0:
            counter += 1
    return counter

# This function checks if a pattern is frequent or not
def isFrequent(pattern, transaction_DB, min_support):
    counter = count_pattern_occurance(pattern, transaction_DB)
    if counter >= int(min_support):
        return True
    else:
        return False

def get_L_k(C_k, transaction_DB, min_support):
    L_k = []
    for candidate in C_k:
        if isFrequent(candidate, transaction_DB, min_support):
            L_k.append(candidate)
    return L_k


def fill_frequency_pattern_book(frequent_pattern_book, L_k, transaction_DB):
    for pattern in L_k:
        occurance = count_pattern_occurance(pattern,transaction_DB)
        pair = [str(occurance), pattern]
        frequent_pattern_book.append(pair)
    return frequent_pattern_book

def fill_closed_and_max_frequent_pattern_book(closed_frequent_pattern_book, max_frequent_pattern_book, Lk_minus_1, frequent_pattern_book, transaction_DB):
    for pattern in Lk_minus_1:
        occurance = count_pattern_occurance(pattern, transaction_DB)
        checker1 = 0
        checker2 = 0
        for pair in frequent_pattern_book:
            if pair[0] == str(occurance) and isSubset(pattern, pair[1]) == True and isSubset(pair[1],pattern)==False:
                checker1 += 1
            if isSubset(pattern, pair[1]) == True and isSubset(pair[1],pattern)==False:
                checker2 += 1
        if checker1 == 0:
            pair1 = [str(occurance), pattern]
            closed_frequent_pattern_book.append(pair1)
        if checker2 == 0:
            pair2 = [str(occurance), pattern]
            max_frequent_pattern_book.append(pair2)
    return closed_frequent_pattern_book, max_frequent_pattern_book



# This function is used to mine the frequent pattern from the transaction database
# It returns a dictionary, key is frequent pattern and value is fequency
def mining_frequent_pattern():
    min_support, transaction_DB = read_input()
    min_support = int(min_support)
    k = 2
    frequent_pattern_book = []
    closed_frequent_pattern_book = []
    max_frequent_pattern_book = []
    L1 = extract_L1(min_support, transaction_DB)
    L = []
    L.append(L1)
    frequent_pattern_book = fill_frequency_pattern_book(frequent_pattern_book,L1,transaction_DB)
    while True:
        Lk_minus_1 = L[-1]
        L_k = get_L_k(cartisian_product(Lk_minus_1, k), transaction_DB, min_support)
        if len(L_k) != 0:
            L.append(L_k)
            frequent_pattern_book = fill_frequency_pattern_book(frequent_pattern_book,L_k,transaction_DB)
            closed_frequent_pattern_book,max_frequent_pattern_book = fill_closed_and_max_frequent_pattern_book(closed_frequent_pattern_book, max_frequent_pattern_book,Lk_minus_1, frequent_pattern_book, transaction_DB)
            k += 1
        else:
            closed_frequent_pattern_book, max_frequent_pattern_book = fill_closed_and_max_frequent_pattern_book(closed_frequent_pattern_book, max_frequent_pattern_book, Lk_minus_1, frequent_pattern_book, transaction_DB)
            break
    frequent_pattern_book.sort(key = itemgetter(1))
    frequent_pattern_book.sort(key = itemgetter(0), reverse = True)
    closed_frequent_pattern_book.sort(key = itemgetter(1))
    closed_frequent_pattern_book.sort(key = itemgetter(0), reverse = True)
    max_frequent_pattern_book.sort(key = itemgetter(1))
    max_frequent_pattern_book.sort(key = itemgetter(0), reverse = True)
    for pair in frequent_pattern_book:
        print(pair[0], end = " ")
        print(pair[1])
    print(" ")
    for pair in closed_frequent_pattern_book:
        print(pair[0], end = " ")
        print(pair[1])
    print(" ")
    for pair in max_frequent_pattern_book:
        print(pair[0], end = " ")
        print(pair[1])

mining_frequent_pattern()
