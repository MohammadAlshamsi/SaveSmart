import csv
my_dict = {'1': 'aaa', '2': 'bbb', '3': 'ccc'}
with open('test.csv', 'w') as f:
    for key in my_dict.keys():
        f.write("%s,%s\n"%(key,my_dict[key]))