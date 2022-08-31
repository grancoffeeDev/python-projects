from pack.id import lastid as lastid

id = lastid()

results = id.getLastBQ()

print(results)

#for row in results:
#    print("{}".format(row.lastid))
