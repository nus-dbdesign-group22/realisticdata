prio = [('a', 4),('b',0),('c',1),('d',3),('e',2),('f',3),('g',2),('h',4)]
order = []

for p in prio:
    while len(order) <= p[1]:
        order.append([])
    order[p[1]].append(p[0])

print(order)
