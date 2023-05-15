import random
import numpy as np


# list = [20, 16, 10, 5]
# random.shuffle(list)
# print("ya: ",  list)


# ha = [0, 1, 2, 3, 4, 5, 6, 7]

# random.seed(100)
# print(random.sample(ha, k=8))   # [2, 5, 3, 4]
# print(random.sample((1, 2, 3, 4, 5), k=4))   # [2, 1, 5, 4]
# print(random.sample('12345', k=4))       # ['2', '5', '3', '1']


# binary = format(11, "b").zfill(4)
# for i in range(4):
#     print(binary[i])
#     # print(len(binary))


# hehe = np.zeros(8)
# print(hehe[1])

# l = len(binary)

# hoho = 0

# for i in range(0, l, 1):
#     # print(i)
#     print(binary[i])
#     hehe[i] = binary[i]
#     print(hehe[i])

#     hoho += hehe[i] * (2**(l-i-1))

# print(hoho)
# hoho = int(hoho)
# print(type(hoho))

num = 50
b = format(num, "b")
print("10 -> 2")
print(b)

l = len(b)
# print("length")
# print(l)
j = 0
list2 = np.zeros(8)

for i in range(8-l, 8, 1):
    list2[i] = b[j]
    # list2[i] = int(list2[i])
    j += 1

print("8 bit")
print(list2)

list1 = [0, 1, 2, 3, 4, 5, 6, 7]

random.seed(100)
for i in range(8):
    list1[i] = list1[i] % 100

print("before shuffe")
print(list1)

list3 = random.sample(list1, k=8)
print("after shuffe")
print(list3)

list4 = np.empty(8)

for i in range(8):
    list4[i] = list2[list3[i]]

print("final")
print(list4)

p = 0

for i in range(8):
    p += list4[i] * (2**(list1[7-i]))
#     hoho += hehe[i] * (2**(l-i-1))
p = int(p)
print(p)
