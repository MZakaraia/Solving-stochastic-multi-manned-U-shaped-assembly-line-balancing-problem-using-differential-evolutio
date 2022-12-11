import numpy as np
import random as rn
from Multi_Manned_with_U_Shaped_functions import prob_data, SolutionClass, bubblesort2, normdf
import time as ti
# import matplotlib.pyplot as plt

def differential_ev(problem_name = None, ct= None, alpha = 0.95, operatators = 1, nPop= 50, MaxIt= 100, beta_min= 0.2, beta_max= 0.8, pCR= 0.2):
    # Preparing problem data
    prob = prob_data(problem_name)
    problem_data = prob[0]
    tasks = [x for x in problem_data]
    total_time = 0
    for i in prob[0]:
        prob[0][i]['Variance'] = (ct - prob[0][i]['Processing time'])/1000    
    total_area = prob[1]
    # Initialization
    pop = {}
    BestSol_fn = float('inf')
    beta_dist = np.sqrt(beta_min ** 2 + beta_max ** 2)
    plot_array = []
    start = ti.time()
    for i in range(nPop):
        position = np.array([rn.random() for i in range(len(tasks))])
        pos = np.copy(position)   
        tasks_list = list(tasks)
        bubblesort2(position, tasks_list)
        pop[i] = SolutionClass(ct, total_area, alpha, problem_data, tasks_list,operatators, pos)
        if pop[i].solution[1] < BestSol_fn:
            BestSol_fn = pop[i].solution[1]
            # plot_array.append(BestSol_fn)
            best_solution = pop[i]
            end = ti.time()
            # print(i)
            total_time = end - start
    # DE main loop
    for i in range(MaxIt):
        for j in range(nPop):
            current_position = pop[j].position
            # Get three random positions from population that aren't equal to the position of i solution
            Others = [x for x in range(nPop) if x != j]
            sol1 = Others[0]
            sol2 = Others[1]
            # sol3 = Others[2]
            beta = np.array([beta_min + rn.random() * beta_dist for ii in range(len(tasks))])
            # Mutation
            new_position = best_solution.position + beta * (pop[sol1].position - pop[sol2].position)
            # mu_pos = np.copy(new_position)
            # tasks_list = list(tasks)
            # tasks_list = bubblesort2(mu_pos, tasks_list)
            # mu_solution = SolutionClass(ct, total_area, alpha, problem_data, tasks_list,operatators, mu_pos)
            # Crossover
            crossover_pos = np.zeros((1, len(tasks)))[0]
            for k in range(len(new_position)):
                if rn.random() <= pCR:
                    crossover_pos[k] = current_position[k]
                else:
                    crossover_pos[k] = new_position[k]
            # Selection
            cr_pos = np.copy(crossover_pos)
            tasks_list = list(tasks)
            tasks_list = bubblesort2(crossover_pos, tasks_list)
            cr_solution = SolutionClass(ct, total_area, alpha, problem_data, tasks_list,operatators, cr_pos)
            # if mu_solution.solution[1] < cr_solution.solution[1]:
            #     new_solution = mu_solution
            # else:
            new_solution = cr_solution
            # print(crossover_pos)
            if new_solution.solution[1] < pop[j].solution[1]:
                pop[j] = new_solution
            else:
                position = np.array([rn.random() for i in range(len(tasks))])
                pos = np.copy(position)   
                tasks_list = list(tasks)
                bubblesort2(position, tasks_list)
                pop[j] = SolutionClass(ct, total_area, alpha, problem_data, tasks_list,operatators, pos)
                # print('ok1')
                if pop[j].solution[1]  < new_solution.solution[1]:
                    new_solution = pop[j]
            if new_solution.solution[1] < BestSol_fn:
                print('New optimized solution')
                BestSol_fn = new_solution.solution[1]                    
                best_solution = new_solution
                end = ti.time()
                print(i)
                total_time = end - start
        # plot_array.append(BestSol_fn)
    # Return the best solution found
    # print(plot_array)
    # plt.plot(plot_array)
    return best_solution, total_time





