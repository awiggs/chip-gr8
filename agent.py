import numpy as np
from sklearn.neural_network import MLPClassifier as classifier
import stats
#X = np.array([ [bool(), int(0)], [bool(), int(1)] ])
#y = np.array([ bool(), bool(), int() ])
#print(X.shape)
#print(y.shape)
agent = classifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
agent.fit(stats.X, stats.Y)

