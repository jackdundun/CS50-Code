pos_choices = []
cell = (0,0)
# creating the tuples
for i in range(3):
    for j in range(3):
        tuple_add = (cell[0] + i - 1, cell[1] + j - 1)
        pos_choices.append(tuple_add)
# removing the original tuple that we know is safe
# using list comprehension to remove any tuples outside the range and then converting the list into a set
pos_choices = set([item for item in pos_choices if (item[0] > -1 and item[1] > -1) and (item[0] < 8 and item[1] < 8)])
pos_choices.remove(cell)
pos_choices.add(None)

if None in pos_choices:
    print(None)