dictionary = ['all', 'an', 'and', 'as', 'closely', 'correct', 'equivocal',
              'examine', 'indication', 'is', 'means', 'minutely', 'or', 'scrutinize',
              'sign', 'the', 'to', 'uncertain']
words = input()
if all([word in dictionary for word in words.split()]):
    print('OK')
else:
    [print(word) if (word not in dictionary) else "" for word in words.split()]
