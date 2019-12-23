#!/usr/bin/env python
from pgmpy.utils.mathext import powerset
from pgmpy.base import UndirectedGraph
from pgmpy.models import BayesianModel
from pgmpy.estimators import StructureEstimator, HillClimbSearch, BDeuScore
from pgmpy.independencies import Independencies, IndependenceAssertion
from pgmpy.estimators.CITests import chi_square


class MmhcEstimator(StructureEstimator):
    def __init__(self, data, **kwargs):
        """
        """
        super(MmhcEstimator, self).__init__(data, **kwargs)

    def estimate(self, scoring_method=None, tabu_length=10, significance_level=0.01):
        if scoring_method is None:
            scoring_method = BDeuScore(self.data, equivalent_sample_size=10)

        skel = self.mmpc(significance_level)

        hc = HillClimbSearch(self.data, scoring_method=scoring_method)

        model = hc.estimate(
            white_list=skel.to_directed().edges(), tabu_length=tabu_length
        )

        return model

    def mmpc(self, significance_level=0.01):
        nodes = self.state_names.keys()

        def assoc(X, Y, Zs):
            """Measure for (conditional) association between variables. Use negative
            p-value of independence test.
            """
            return 1 - chi_square(X, Y, Zs, self.data)[1]

        def min_assoc(X, Y, Zs):
            "Minimal association of X, Y given any subset of Zs."
            return min(assoc(X, Y, Zs_subset) for Zs_subset in powerset(Zs))

        def max_min_heuristic(X, Zs):
            "Finds variable that maximizes min_assoc with `node` relative to `neighbors`."
            max_min_assoc = 0
            best_Y = None

            for Y in set(nodes) - set(Zs + [X]):
                min_assoc_val = min_assoc(X, Y, Zs)
                if min_assoc_val >= max_min_assoc:
                    best_Y = Y
                    max_min_assoc = min_assoc_val

            return (best_Y, max_min_assoc)

        # Find parents and children for each node
        neighbors = dict()
        for node in nodes:
            neighbors[node] = []

            # Forward Phase
            while True:
                new_neighbor, new_neighbor_min_assoc = max_min_heuristic(
                    node, neighbors[node]
                )
                if new_neighbor_min_assoc > 0:
                    neighbors[node].append(new_neighbor)
                else:
                    break

            # Backward Phase
            for neigh in neighbors[node]:
                other_neighbors = [n for n in neighbors[node] if n != neigh]
                for sep_set in powerset(other_neighbors):
                    if self.test_conditional_independence(node, neigh, sep_set):
                        neighbors[node].remove(neigh)
                        break

        # correct for false positives
        for node in nodes:
            print(node,":",neighbors[node])
            print(neighbors[node])
            for neigh in neighbors[node]:
                if node not in neighbors[neigh]:
                    print("node-%s is removed"%neigh)
                    neighbors[node].remove(neigh)

        skel = UndirectedGraph()
        skel.add_nodes_from(nodes)
        for node in nodes:
            print(node,"->",neighbors[node])
            skel.add_edges_from([(node, neigh) for neigh in neighbors[node]])

        return skel


import pandas as pd
import numpy as np
data = pd.DataFrame(np.random.randint(0, 3, size=(500, 8)), columns=list('ABCDEFGH'))
data['A'] += data['B'] + data['C']
data['H'] = data['G'] - data['A']
data['E'] *= data['F']

mmhc = MmhcEstimator(data)
skeleton = mmhc.mmpc()
print("Part 1) Skeleton: ", skeleton.edges())