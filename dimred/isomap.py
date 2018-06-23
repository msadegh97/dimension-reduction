from sklearn.neighbors import kneighbors_graph
from sklearn.neighbors import NearestNeighbors
from sklearn.utils.graph import graph_shortest_path
import numpy as np
import scipy as sp
import networkx


class IsoMap():



    def __init__(self, n_component):


        self.n_component = n_component
        self.k = None
        self.lambdas = None
        self.alphas = None
        self.kneargraph = None

    def _fit(self, X):

        neighbour = NearestNeighbors(n_neighbors=50)
        neighbour.fit(X)
        self.kneargraph = kneighbors_graph(neighbour, n_neighbors=50, mode = 'distance')
        D = graph_shortest_path(self.kneargraph, directed=False)
        H = np.eye(1000, 1000) - 1 / 1000 * np.ones((1000, 1000))
        self.k = -1 / 2 * H.dot(D ** 2).dot(H)
        self.lambdas, self.alphas = sp.linalg.eigh(self.k)

        indices = self.lambdas.argsort()[::-1]
        self.lambdas = self.lambdas[indices]
        self.alphas = self.alphas[:, indices]

        self.lambdas = self.lambdas[0:self.n_component]
        self.alphas = self.alphas[:, 0:self.n_component]

    def fit(self, X):


        self._fit(X)
        return self

    def transform(self, X):

        y = self.alphas * np.sqrt(self.lambdas)
        return y

