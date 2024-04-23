from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1200, n_features=4, weights=[0.95, 0.05])

X_test = X[-200:]
X = X[:-200]
y = y[:-200]
test = X[-200:]

print(y[-200:].sum())
