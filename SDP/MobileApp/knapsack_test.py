data = {
        'A': 5,
        'B': 10,
        'C': 11,
        'D': 7,
        'E': 2,
        'Z': 4,
        'F': 3
}

def greedy_algo(mystuff, limit=30):

    # Copy the dictionary to work on duplicate
    copy_stuff = dict(mystuff)
    # Initialize an output list
    outlist = []

    def keywithmaxval(d):
     #a) create a list of the dict's keys and values; 
     #b) return the key with the max value  
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]


    def greedy_grab(mydict):
        result = []
        total = 0
        while total <= limit and len(mydict) > 0:
            maxkey=keywithmaxval(mydict)
            result.append(maxkey)
            total += mydict[maxkey]
            del mydict[maxkey]
        return result

    def update_dict(mydict, mylist):
        for i in mylist:
            del mydict[i]
        return mydict     

    while len(copy_stuff) > 0:
        outlist.append(greedy_grab(copy_stuff))


    return outlist


print (greedy_algo(data, limit=30))