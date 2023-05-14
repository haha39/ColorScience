import random
import numpy as np


list = [20, 16, 10, 5]
random.shuffle(list)
print("ya: ",  list)


ha = [0, 1, 2, 3, 4, 5, 6, 7]

random.seed(100)
print(random.sample(ha, k=8))   # [2, 5, 3, 4]
print(random.sample((1, 2, 3, 4, 5), k=4))   # [2, 1, 5, 4]
print(random.sample('12345', k=4))       # ['2', '5', '3', '1']


binary = format(11, "b").zfill(4)
for i in range(4):
    print(binary[i])
    # print(len(binary))


hehe = np.zeros(8)
print(hehe[1])

l = len(binary)

hoho = 0

for i in range(0, l, 1):
    # print(i)
    print(binary[i])
    hehe[i] = binary[i]
    print(hehe[i])

    hoho += hehe[i] * (2**(l-i-1))

print(hoho)
hoho = int(hoho)
print(type(hoho))
