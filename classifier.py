# -*- coding: utf-8 -*-
"""
Created on Sun May 22 15:19:31 2016

@author: shengquan
"""

import numpy as np

def return_best_board(input_list, weight_arr, rows=17, cols=8):
    results_arr = []
    for i in input_list:
        results_arr.append(calc_results(i, weight_arr, rows, cols))

    return np.argmax(results_arr)
    
def calc_results(input_list, weight_arr, rows, cols):
    #input_list = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]

    input_arr = np.array(input_list)
    
    # rows = 17
    # cols = 8
    
    #weight_arr = np.array([0.5,-0.5,-0.5,-0.5])
    #clear, height, hole, blockage
    
    #clear score calc
    clear_score_arr = np.sum(input_list, axis=1)
    clear_results = sum([1 if i==cols else 0 for i in clear_score_arr])
    
    #height score calc
    height_val_arr = np.array(np.ones(cols)*17)
    for i in range(rows - 1):
        height_val_arr = np.append(height_val_arr, np.ones(cols)*(rows-i-1), axis=0)
    
    height_val_arr = height_val_arr.reshape(rows, cols)
    height_results_arr = height_val_arr * input_arr
    height_results = np.sum(height_results_arr)
    
    #hole score calc
    hole_arr = np.max(height_results_arr, axis=0) - np.sum(input_list, axis=0)
    hole_results = sum(np.max(height_results_arr, axis=0) - np.sum(input_list, axis=0))
    
    #blockage score calc
    blockage_results = 0
    cols_w_holes_arr = np.nonzero(hole_arr)
    for i in cols_w_holes_arr[0]:
        hole_tmp = np.nonzero(input_arr[:,i])
        blockage_results += (hole_tmp[0][-1] - hole_tmp[0][0])
        
    total_results = sum(weight_arr * np.array([clear_results, height_results, hole_results, blockage_results]))
    
    return total_results
    