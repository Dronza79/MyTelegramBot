import pickle
import os.path

from example_history import Alpha, Beta

if os.path.isfile('../data_base/history.pickle'):
    with open('../data_base/history.pickle', 'rb') as f:
        try:
            history = pickle.load(f)
        except Exception:
            history = dict()
else:
    history = dict()

print(history)

# {
# 123: [
#   Alpha1/время:10/13/22 14:22:09/param:qwerty/args:(['1', '5', '9'],),
#   Beta1/время:10/13/22 14:24:00/param:дом/args:(['1', '11', '1'],)],
# 987: [
#   Alpha2/время:10/13/22 14:22:51/param:poiu/args:(['5', '5', '5'],),
#   Beta2/время:10/13/22 14:24:20/param:edrf/args:(['2', '2', '2'],)]}

