numbers = [1,2,3,4,5,6,7,8,9]
group = {1,4,6,7}

def sorting(numbers, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found, numbers

#sort = sorting(numbers, group)

class Sort:
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return self.found, (1, x)

sort2 = Sort(group)
numbers.sort(key=sort2)
print(numbers)
    
  