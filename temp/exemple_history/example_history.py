import pickle
import time


class Alpha:
    count = 0

    def __init__(self, param1, listing=None):
        self.param1 = param1
        self.time = time.time()
        self.listing = listing
        self.num = Alpha.count + 1
        Alpha.count += 1

    def __repr__(self):
        return (f'Alpha{self.num}/{time.strftime("%x %X", time.localtime(self.time))}'
                f'/param:{self.param1}/args:{self.listing}')


class Beta:
    count = 0

    def __init__(self, param1, listing=None):
        self.param1 = param1
        self.time = time.time()
        self.listing = listing
        self.num = Beta.count + 1
        Beta.count += 1

    def __repr__(self):
        return (f'Beta{self.num}/{time.strftime("%x %X", time.localtime(self.time))}'
                f'/param:{self.param1}/args:{self.listing}')

    def __str__(self):
        return 'command Beta'


def make_exemple_alfa():
    user = int(input('user(int)>> '))
    type_h = input('type(Any)>> ')
    list_n = [input('num(Any)>> ') for _ in range(3)]
    alfa = Alpha(type_h, list_n)

    if user in history:
        history[user].append(alfa)
    else:
        history[user] = [alfa]
    with open('../data_base/history.pickle', 'wb') as f:
        pickle.dump(history, f)


def make_exemple_beta():
    user = int(input('user(int)>> '))
    type_h = input('type(Any)>> ')
    list_n = [input('num(Any)>> ') for _ in range(3)]
    beta = Beta(type_h, list_n)

    if user in history:
        history[user].append(beta)
    else:
        history[user] = [beta]
    with open('../data_base/history.pickle', 'wb') as f:
        pickle.dump(history, f)

if __name__ == '__main__':

    # from handler_pickle import history
    #
    # while True:
    #     temp = input('choice(int)>> ')
    #     if temp == '1':
    #         make_exemple_alfa()
    #         print(history)
    #     elif temp == '2':
    #         make_exemple_beta()
    #         print(history)
    #     elif temp == '3':
    #         if input('change(int) >> ') == '1':
    #             userid = int(input('user(int)>> '))
    #             target = history[userid][len(history[userid]) - 1]
    #             print(target)
    #             target.param1 = input('param1(Any)>> ')
    #             print(history)
    #             with open('../data_base/history.pickle', 'wb') as file:
    #                 pickle.dump(history, file)
    a = Beta(1, [1,2])

    print(a)
