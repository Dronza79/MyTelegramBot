import pickle

class Alfa:
    def __init__(self, param1, param2, *args):
        self.param1 = param1
        self.param2 = param2
        self.args = args
    def __repr__(self):
        return f'имя:{self.__qualname__} param1:{self.param1} param2:{self.param2} args:{self.args}'


class Beta:
    def __init__(self, param1, param2, *args):
        self.param1 = param1
        self.param2 = param2
        self.args = args
    def __repr__(self):
        return f'param1:{self.param1} param2:{self.param2} args:{self.args}'


a = Alfa(10124, 'city', True, 'yes', [1, 2, 3])
b = Beta(25897, 'town', False, 'not', [0, 9, 8])
c = Alfa(10224, 'city', True, 'not', [0, 0, 3])

history = {
    123456: [a, c, b],
    9876: [b, a, c]
}
print(history)
seralize = pickle.dumps(history)

print(seralize)

# for k, v in history.items():
#     print(k, v)
