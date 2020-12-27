# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:05:20 2020

@author: Hogan
"""

import pulp as p
import pandas as pd
import numpy as np
  
class DEA():
    def __init__(self, inputs, outputs):
        
        if len(inputs.index)!=len(outputs.index):
            return print("Error: Number of units inconsistent")
        
        self.inputs=inputs
        self.outputs=outputs
        
        self.units_number=len(inputs.index)
        self.inputs_number=len(inputs.columns)
        self.outputs_number=len(outputs.columns)
        
        self._i=range(self.units_number)
        self._j=range(self.inputs_number)
        self._k=range(self.outputs_number)
        
        self.DMU=self.create_problems()
        
    def create_problems(self):
        DMU={}
        for i in self._i:
            DMU[i] = self.create_dmu(i)
        return DMU
    
    def create_dmu(self, j0):
        
        problem = p.LpProblem('DMU_'+str(j0), p.LpMaximize)
        self.input_weights = p.LpVariable.dicts("input_weights", ((i, j) for i in self._i for j in self._j), lowBound=0, cat='Continuous')
        self.output_weights = p.LpVariable.dicts("output_weights", ((i, k) for i in self._i for k in self._k), lowBound=0, cat='Continuous')
        
        #Objective funtion
        problem += p.LpAffineExpression([(self.output_weights[(j0,k)], self.outputs.values[(j0,k)]) for k in self._k])
        
        #Constraints
        problem += p.LpAffineExpression([(self.input_weights[(j0,i)],self.inputs.values[(j0,i)]) for i in self._j]) == 1, "Norm Constraint"
        
        for j1 in self._i:
            problem += self.dmu_constraint(j0, j1)  <= 0, "DMU_constraint_"+str(j1)
        
        
        return problem
    
    def dmu_constraint(self, j0, j1):
        Out = p.LpAffineExpression([(self.output_weights[(j0,k)], self.outputs.values[(j1,k)]) for k in self._k])
        In = p.LpAffineExpression([(self.input_weights[(j0,i)], self.inputs.values[(j1,i)]) for i in self._j])
        
        return Out - In
        
    def solve(self):
        
        status={}
        weights={}
        efficiency=pd.DataFrame(data=np.nan, index=self.inputs.index, columns=['Efficiency'])
        
        for i, problem in list(self.DMU.items()):
            problem.solve()
            status[i] = p.LpStatus[problem.status]
            weights[i] = {}
            
            for j in problem.variables():
                weights[i][j.name] = j.varValue
            efficiency.iloc[i,0] = p.value(problem.objective)
            
        
        
        return status, weights, efficiency
        
        


