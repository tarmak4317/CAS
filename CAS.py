class Symbol: #Symbolic object class
    def __init__(self, var, pre, post):
        self.var = var
        self.pre = pre
        self.post = post

    def __truediv__(self, other): #division override
        return Symbol(self.var, self.pre / other.pre, self.post - other.post)

    def __mul__(self, other): #multiplication override
        return Symbol(self.var, self.pre * other.pre, self.post + other.post)

    def __add__(self, other): #addition override
        return Symbol(self.var, self.pre + other.pre, self.post)

    def __sub__(self, other): #subtraction override
        return Symbol(self.var, self.pre - other.pre, self.post)

    def __str__(self): #conversion for printing
        return str(self.pre) + self.var + str(self.post)

class Frac: #Fraction class
    def __init__(self, num, den):
        self.num = num
        self.den = den

    @staticmethod
    def converter(obj): #converts Symbol objects to Frac objects
        if isinstance(obj, Symbol):
            return Frac(obj, Symbol('x', 1, 0))
        else:
            return obj

    def __truediv__(self, other): #division override
        self = Frac.converter(self)
        other = Frac.converter(other)
        return Frac(self.num * other.den, self.den * other.num)

    def __mul__(self, other): #multiplication override
        self = Frac.converter(self)
        other = Frac.converter(other)
        return Frac(self.num * other.num, self.den * other.den)

    def __add__(self, other): #addition override
        self = Frac.converter(self)
        other = Frac.converter(other)
        if self.den == other.den:
            num = [self.num, '+', other.num]
            solver(num)
            den = self.den
        else:
            num = [self.num * other.den, '+', other.num * self.den]
            solver(num)
            den = self.den * other.den
        return Frac(num, den)

    def __sub__(self, other): #subtraction override
        self = Frac.converter(self)
        other = Frac.converter(other)
        if self.den == other.den:
            num = [self.num, '-', other.num]
            solver(num)
            den = self.den
        else:
            num = [self.num * other.den, '-', other.num * self.den]
            solver(num)
            den = self.den * other.den
        return Frac(num, den)

    def __str__(self): #conversion for printing
        if isinstance(self.num, list):
            st = '[' + ' '.join(map(str, self.num)) + ']|' + str(self.den)
            return st
        else:
            return str(self.num) + '|' + str(self.den)
        
def sort_expression(arr):
    terms = []  # Store (sign, symbol) pairs
    sign = '+'  # Default sign
    
    for elem in arr:
        if elem in ['+', '-']:
            sign = elem  # Update sign for next term
        else:
            terms.append((sign, elem))  # Store term with its sign

    # Sort based on exponent (`post` value) in descending order
    terms.sort(key=lambda x: x[1].post, reverse=True)

    # Rebuild sorted expression
    sorted_arr = []
    for sign, term in terms:
        sorted_arr.append(sign)
        sorted_arr.append(term)

    return sorted_arr

def remover(arr): #removes labelled objects by trying to match wits with a rutabaga
    while "brownMunde" in arr:
        arr.remove("brownMunde")

def solver(arr):
    x = 0
    while x < len(arr): #implements division
        if arr[x] == '/':
            arr[x + 1] = arr[x - 1] / arr[x + 1]
            arr[x - 1] = "brownMunde"
            arr[x] = "brownMunde"
            remover(arr)
        x += 1

    x = 0
    while x < len(arr): #implements multiplication
        if arr[x] == '*':
            arr[x + 1] = arr[x - 1] * arr[x + 1]
            arr[x - 1] = "brownMunde"
            arr[x] = "brownMunde"
            remover(arr)
        x += 1

    x = 0
    while x < len(arr): #implements subtraction conversion
        if arr[x] == '-':
            arr[x+1].pre *= -1
            arr[x] = '+'
        x += 1

    x = 0
    while x < len(arr): #implements addition
        arr = sort_expression(arr)
        if arr[x] == '+':
            if isinstance(arr[x + 1], Symbol) and isinstance(arr[x - 1], Symbol):
                if arr[x + 1].post == arr[x - 1].post:
                    arr[x + 1] = arr[x - 1] + arr[x + 1]
                    arr[x - 1] = "brownMunde"
                    arr[x] = "brownMunde"
                    remover(arr)
        x += 1

def list_add(arr1, arr2): #implements polynomial addition
    solver(arr1)
    solver(arr2)
    res=arr1 + ['+'] + arr2
    solver(res)
    return res

def list_sub(arr1, arr2): #implements polynomial subtraction
    solver(arr1)
    solver(arr2)
    k = 0
    while k < len(arr2):
        if arr2[k] == '-':
            arr2[k] = '+'
        k += 1
    res=arr1 + ['-'] + arr2
    solver(res)
    return res

def list_mult(arr1, arr2): #implements polynomial multiplication
    res = []
    sign = ['+']
    for x in arr1:
        if x == '+' or x == '-':
            sign = x
            continue
        else:
            for y in arr2:
                if (y == '+' and sign == '+') or (y == '-' and sign == '-'):
                    res += ['+']
                elif y == '-' or y == '+':
                    res += ['-']
                else:
                    res.append(x * y)
    solver(res)
    return res

def list_div(arr1, arr2): #implements polynomial division
    sign = ['+']
    res = []
    while arr1[0].post >= arr2[0].post:
        a = arr1[0]
        b = arr2[0]
        d = [a / b]
        res.append(sign)
        res.append(d)
        arr1 = list_sub(arr1, list_mult(arr2, d))
    return res

def printer(arr): #for printing final result
    j = 0
    while j < len(arr):
        print(arr[j], end=' ')
        j += 1
    print('\n')  # Add a newline at the end for clarity

# Example usage
arr = [Frac(Symbol('x', 3, 2), Symbol('x', 2, 1)), '-', Symbol('x', 3, 2)]
solver(arr)
printer(arr)
printer(list_div([Symbol('x',1,2),'-',Symbol('x',1,0)],[Symbol('x',1,1),'-',Symbol('x',1,0)]))
# Example usage ends
