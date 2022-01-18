# -*- coding: utf-8 -*-

import gurobipy as gp
from gurobipy import GRB


def TripSelectionProblem(D, S, P, r):
    trip_indexs = list(range(len(S)))
    m = gp.Model("mip1")
    x = m.addVars(len(S), vtype=GRB.BINARY, name="x")

    m.setObjective(gp.quicksum(S[i]*x[i] for i in trip_indexs), GRB.MAXIMIZE)
    for d in D: #겹치지 않는 조건
        m.addConstr(gp.quicksum(x[i]  for i in d) <= 1)
    m.addConstr(gp.quicksum(x[i] for i in trip_indexs) <= r) #선택되는 trip의 수는 로봇의 수보다 작도록

    #풀이
    m.optimize()
    try:
        print('Obj val: %g' % m.objVal)
        res = []
        count = 0
        for val in m.getVars():
            if val.VarName[0] == 'x' and float(val.x) == 1.0:
                res.append(count)
            count += 1
        return res
    except:
        print('Infeasible')
        return []