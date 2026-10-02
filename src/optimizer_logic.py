import json
from random import sample, random, seed
import re
from math import exp
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from  numpy import inf
import os
import sys

class Algorithm:
    def __init__(self):
        
        with open(resource_path("data/filtered_champions.json"), "r", encoding="utf-8") as file1:
            champs_data = json.load(file1)

        with open(resource_path("data/filtered_items.json"), "r", encoding="utf-8") as file2:
            items_data = json.load(file2)

        with open(resource_path("data/champs_suggested_items.json"), "r", encoding="utf-8") as file2:
            suggested_items = json.load(file2)

        
        self.champs_data = champs_data
        self.items_data = items_data
        self.set_of_item_names = set(items_data.keys())
        self.suggested_items = suggested_items
        self.no_of_items = None
        self.neighbour_dict = {
            1 : self.make_neighbour_1,
            2 : self.make_neighbour_2,
            3 : self.make_neighbour_3,
            4 : self.make_neighbour_4
        }
        self.en_ad = None
        self.en_ap = None
        self.en_tank = None
        self.gold_cap = None
        self.enemy_rel_val = [None,None,None,None,0,0]    #pola klasy do obslugi funkcji celu
        self.item_itself_val = [None,None,None,None,0,0]  #pola klasy do obslugi funkcji celu
        self.total_items_val = [None,None,None,None,0,0]  #pola klasy do obslugi funkcji celu
        self.limit_of_iterations = 0


    # funkcje tworzące sąsiada rozwiązania
    # losowe wybranie jednego przedmiotu do zmiany, losowy wybór nowego przedmiotu
    def make_neighbour_1(self,current_solution):

        list_of_indexes = [x for x in range(self.no_of_items)]
        index =  sample(list_of_indexes,1)[0]

        # assign current_solution to neighbour
        neighbour = current_solution.copy()
        contains_hydra = any(re.search(r'hydra', item, re.IGNORECASE) for item in current_solution)
        # Check if current solution contains any of the specified items
        contains_spellblade = any(re.search(r'trinity force|lich bane|iceborn gauntlet', item, re.IGNORECASE) for item in current_solution)
        g = inf
        g_actual_wo_new_item = 0

        for i in range(self.no_of_items):
            g_actual_wo_new_item += self.items_data[current_solution[i]]["shop"]["prices"]["total"]
        g_actual_wo_new_item -= self.items_data[current_solution[index]]["shop"]["prices"]["total"]
        #limit of iterations
        limit = 0
        # Randomly choose new item from list_of_item_names, ensuring it does not contain 'hydra' or any of the specified items if current solution does
        while (g > self.gold_cap):
            item_name = sample(list(self.set_of_item_names - set(current_solution)), 1)[0]
            if (not contains_hydra or not re.search(r'hydra', item_name, re.IGNORECASE)) and \
            (not contains_spellblade or not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name, re.IGNORECASE)):
                neighbour[index] = item_name
                g = g_actual_wo_new_item + self.items_data[item_name]["shop"]["prices"]["total"]
                limit += 1
                if g <= self.gold_cap:
                    break
                elif limit == 4000:
                    g = g_actual_wo_new_item + self.items_data[current_solution[index]]["shop"]["prices"]["total"]
                    return current_solution, g, []
        # randomly choose new item from list_of_item_names
        #item_name = sample(list(self.set_of_item_names - set(current_solution)),1)[0]
        # replace item in current_solution with new item in index index
        neighbour[index] = item_name

        # calculate cost of all items in new solution
        


        return neighbour, g, [index]

    # loswe wybranie dwóch przedmiotów do zmiany, loswy wybór nowych przedmiotów
    def make_neighbour_2(self,current_solution):

        list_of_indexes = [x for x in range(self.no_of_items)]
        index1, index2 =  sample(list_of_indexes,2)

        # assign current_solution to neighbour
        neighbour = current_solution.copy()



        # Check if current solution contains an item with 'hydra' in its name
        contains_hydra = any(re.search(r'hydra', item, re.IGNORECASE) for item in current_solution)
        # Check if current solution contains any of the specified items
        contains_spellblade = any(re.search(r'trinity force|lich bane|iceborn gauntlet', item, re.IGNORECASE) for item in current_solution)

        g = inf
        g_actual_wo_new_item = 0

        for i in range(self.no_of_items):
            g_actual_wo_new_item += self.items_data[current_solution[i]]["shop"]["prices"]["total"]
        g_actual_wo_new_item -= self.items_data[current_solution[index1]]["shop"]["prices"]["total"] + self.items_data[current_solution[index2]]["shop"]["prices"]["total"]
        #limit of iterations
        limit = 0

        # Randomly choose new items from list_of_item_names, ensuring they do not contain 'hydra' or any of the specified items if current solution does
        while (g > self.gold_cap):
            item_name1, item_name2 = sample(list(self.set_of_item_names - set(current_solution)), 2)
            if (not contains_hydra or (not re.search(r'hydra', item_name1, re.IGNORECASE) and not re.search(r'hydra', item_name2, re.IGNORECASE))) and \
            (not contains_spellblade or (not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name1, re.IGNORECASE) and not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name2, re.IGNORECASE))):
                neighbour[index1] = item_name1
                neighbour[index2] = item_name2
                g = g_actual_wo_new_item + self.items_data[item_name1]["shop"]["prices"]["total"] + self.items_data[item_name2]["shop"]["prices"]["total"]
                limit += 1
                if g <= self.gold_cap:
                    break
                elif limit == 4000:
                    g = g_actual_wo_new_item + self.items_data[current_solution[index1]]["shop"]["prices"]["total"] + self.items_data[current_solution[index2]]["shop"]["prices"]["total"]
                    return current_solution, g, []
        # randomly choose new items from list_of_item_names
        #item_name1, item_name2 = sample(list(self.set_of_item_names - set(current_solution)),2)

        # replace items with new item in indexes index1 and index2
        neighbour[index1] = item_name1
        neighbour[index2] = item_name2

        # calculate cost of all items in new solution]

        return neighbour, g , [index1,index2]

    # loswe wybranie trzech przedmiotów do zmiany, loswy wybór nowych przedmiotów
    def make_neighbour_3(self,current_solution):

        list_of_indexes = [x for x in range(self.no_of_items)]
        index1, index2, index3 =  sample(list_of_indexes,3)

        # assign current_solution to neighbour
        neighbour = current_solution.copy()



        contains_hydra = any(re.search(r'hydra', item, re.IGNORECASE) for item in current_solution)
        # Check if current solution contains any of the specified items
        contains_spellblade = any(re.search(r'trinity force|lich bane|iceborn gauntlet', item, re.IGNORECASE) for item in current_solution)

        g = inf
        g_actual_wo_new_item = 0

        for i in range(self.no_of_items):
            g_actual_wo_new_item += self.items_data[current_solution[i]]["shop"]["prices"]["total"]
        g_actual_wo_new_item -= self.items_data[current_solution[index1]]["shop"]["prices"]["total"] + self.items_data[current_solution[index2]]["shop"]["prices"]["total"] + self.items_data[current_solution[index3]]["shop"]["prices"]["total"]
        #limit of iterations
        limit = 0

        # Randomly choose new items from list_of_item_names, ensuring they do not contain 'hydra' or any of the specified items if current solution does
        while True:
            item_name1, item_name2, item_name3 = sample(list(self.set_of_item_names - set(current_solution)), 3)
            if (not contains_hydra or (not re.search(r'hydra', item_name1, re.IGNORECASE) and not re.search(r'hydra', item_name2, re.IGNORECASE) and not re.search(r'hydra', item_name3, re.IGNORECASE))) and \
            (not contains_spellblade or (not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name1, re.IGNORECASE) and not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name2, re.IGNORECASE) and not re.search(r'trinity force|lich bane|iceborn gauntlet', item_name3, re.IGNORECASE))):
                g = g_actual_wo_new_item + self.items_data[item_name1]["shop"]["prices"]["total"] + self.items_data[item_name2]["shop"]["prices"]["total"] + self.items_data[item_name3]["shop"]["prices"]["total"]
                limit += 1
                if g <= self.gold_cap:
                    break
                elif limit == 4000:
                    g = g_actual_wo_new_item + self.items_data[current_solution[index1]]["shop"]["prices"]["total"] + self.items_data[current_solution[index2]]["shop"]["prices"]["total"] + self.items_data[current_solution[index3]]["shop"]["prices"]["total"]
                    return current_solution, g, []
        # randomly choose new items from list_of_item_names
        #item_name1, item_name2, item_name3 = sample(list(self.set_of_item_names - set(current_solution)),3)
        # replace items with new item in indexes index1 and index2
        neighbour[index1] = item_name1
        neighbour[index2] = item_name2
        neighbour[index3] = item_name3


        return neighbour, g , [index1,index2,index3]

    # wymiana najgorszego przedmiotu według list_of_item_importance lub value_list lub enemy_rel_list
    def make_neighbour_4(self,current_solution,lst: list):

        # assign current_solution to neighbour
        neighbour = current_solution.copy()

        # Check if current solution contains an item with 'hydra' in its name
        contains_hydra = any(re.search(r'hydra', item, re.IGNORECASE) for item in current_solution)
        # Check if current solution contains any of the specified items
        contains_spellblade = any(re.search(r'trinity force|lich bane|iceborn gauntlet', item, re.IGNORECASE) for item in current_solution)

        # find the least contributing item
        min_elem = min(lst[:self.no_of_items])
        index_min = lst.index(min_elem)
        new_item = current_solution[index_min]

        g = inf
        g_actual_wo_new_item = 0

        for i in range(self.no_of_items):
            g_actual_wo_new_item += self.items_data[current_solution[i]]["shop"]["prices"]["total"]
        g_actual_wo_new_item -= self.items_data[current_solution[index_min]]["shop"]["prices"]["total"]
        #limit of iterations
        limit = 0

        # Find new one different than current one, ensuring it does not contain 'hydra' or any of the specified items if current solution does
        while current_solution[index_min] == new_item or \
            (contains_hydra and re.search(r'hydra', new_item, re.IGNORECASE)) or \
            (contains_spellblade and re.search(r'trinity force|lich bane|iceborn gauntlet', new_item, re.IGNORECASE)):
            new_item = sample(list(self.set_of_item_names - set(current_solution)), 1)[0]

            g = g_actual_wo_new_item + self.items_data[new_item]["shop"]["prices"]["total"]
            limit += 1
            if g <= self.gold_cap:
                break
            elif limit == 4000:
                g = g_actual_wo_new_item + self.items_data[current_solution[index_min]]["shop"]["prices"]["total"]
                return current_solution, g, []
        # calculate cost of all items in new solution

        # replace item and return
        neighbour[index_min] = new_item

        return neighbour, g, [index_min]

    def starting_enemy_parameters(self,enemy_champs: list):
        
        self.en_tank = 0 #ile tankow w enemy
        self.en_ad = 0 #ile ad w enemy
        self.en_ap = 0 #ile ap w enemy
        #w zaleznosci od postaci przeciwnika
        for i in range(0,5):
            enemy_type = self.champs_data[enemy_champs[i]]["attributes"]["type"]
            match enemy_type:
                case "attackDamage": 
                    self.en_ad += 1
                case "abilityPower":
                    self.en_ap += 1
                case "tank":
                    self.en_tank += 1
    
    # funkcja celu 
    def objective_function(self, champ_name: str, solution: list, changed_items:list):
        # [enemy_champ1, enemy_champ2... 5]
        #enemy_champ1 : [item1,item2,item3...]
        dmg_type = self.champs_data[champ_name]["attributes"]["type"]
        ability_rel = self.champs_data[champ_name]["attributes"]["abilityReliance"]
        toughness = self.champs_data[champ_name]["attributes"]["toughness"]
        damage_importance =  self.champs_data[champ_name]["attributes"]["damage"]

        len_sol = len([item for item in solution if item is not None])
        
            
        enemy_reliant = 0
        value = 0
        #TESTOWE LISTY

        match dmg_type:

            case "attackDamage":
                for i in changed_items:
                    if damage_importance == 3:
                        enemy_reliant = self.en_tank * damage_importance * self.items_data[solution[i]]["param"]["armorPenetration"]["percent"]
                    elif (solution[i] == "Black Cleaver"):
                        enemy_reliant = (self.en_tank * 30 * damage_importance) / 1.75
                    
                    enemy_reliant += (self.en_ad * toughness * self.items_data[solution[i]]["param"]["armor"]["flat"] \
                                + self.en_ap * toughness * self.items_data[solution[i]]["param"]["magicResistance"]["flat"])
                        
                    
                    value = damage_importance * (self.items_data[solution[i]]["param"]["attackDamage"]["flat"] * 1  + self.items_data[solution[i]]["param"]["attackDamage"]["perLevel"] * 18)\
                        + ((self.items_data[solution[i]]["param"]["cooldownReduction"]["flat"]*ability_rel\
                        + self.items_data[solution[i]]["param"]["abilityHaste"]["flat"]*ability_rel) / 50) \
                        +  toughness * ((self.items_data[solution[i]]["param"]["health"]["flat"] * 1  + self.items_data[solution[i]]["param"]["health"]["perLevel"] * 18) / 8.5 \
                            + (self.items_data[solution[i]]["param"]["healthRegen"]["percent"])/7 )
                    value -= (self.items_data[solution[i]]["param"]["abilityPower"]["flat"] * 1  + self.items_data[solution[i]]["param"]["abilityPower"]["perLevel"] * 18)
                    item_exists = any(item["name"] == solution[i] for item in self.suggested_items[champ_name])
                    if item_exists:
                        value += 350
                    if self.items_data[solution[i]]["rank"] in ["TURRET", "MINION", "POTION", "DISTRIBUTED"]:
                        value -= 300
                    elif self.items_data[solution[i]]["rank"] == "LEGENDARY":
                        value += 100


                    self.enemy_rel_val[i] = enemy_reliant    
                    self.item_itself_val[i] = value 
                    self.total_items_val[i] = value + enemy_reliant

            case "adc":
                crit_chance = 0
                
                for i in changed_items:   
                    item_crit_chance = self.items_data[solution[i]]["param"]["criticalStrikeChance"]["percent"]   
                    crit_chance += item_crit_chance
                    value = 3 * (self.items_data[solution[i]]["param"]["attackDamage"]["flat"] * 1  + self.items_data[solution[i]]["param"]["attackDamage"]["perLevel"] * 18)\
                        + ((self.items_data[solution[i]]["param"]["cooldownReduction"]["flat"]*ability_rel\
                        + self.items_data[solution[i]]["param"]["abilityHaste"]["flat"]*ability_rel) / 50) \
                        +  toughness * ((self.items_data[solution[i]]["param"]["health"]["flat"] * 1  + self.items_data[solution[i]]["param"]["health"]["perLevel"] * 18) / 8.5 \
                            + (self.items_data[solution[i]]["param"]["healthRegen"]["percent"])/7 ) + (self.items_data[solution[i]]["param"]["attackSpeed"]["flat"]) * 1.8
                    if crit_chance < 100:
                        value += item_crit_chance * 2
                    value -= (self.items_data[solution[i]]["param"]["abilityPower"]["flat"] * 1  + self.items_data[solution[i]]["param"]["abilityPower"]["perLevel"] * 18)
                    
                    item_exists = any(item["name"] == solution[i] for item in self.suggested_items[champ_name])
                    if item_exists:
                        value += 350
                    
                    if self.items_data[solution[i]]["rank"] in ["TURRET", "MINION", "POTION", "DISTRIBUTED"]:
                        value -= 300
                    elif self.items_data[solution[i]]["rank"] == "LEGENDARY":
                        value += 100

                    self.enemy_rel_val[i] = enemy_reliant    
                    self.item_itself_val[i] = value 
                    self.total_items_val[i] = value + enemy_reliant

            case "ad_assasin":
                enemy_reliant = 0

                for i in changed_items:   
                    value = 3 * (self.items_data[solution[i]]["param"]["attackDamage"]["flat"] * 1  + self.items_data[solution[i]]["param"]["attackDamage"]["perLevel"] * 18  +\
                        self.items_data[solution[i]]["param"]["lethality"]["flat"] * 2.5 )+ ((self.items_data[solution[i]]["param"]["cooldownReduction"]["flat"]*ability_rel\
                        + self.items_data[solution[i]]["param"]["abilityHaste"]["flat"]*ability_rel) / 50) \
                        +  toughness * ((self.items_data[solution[i]]["param"]["health"]["flat"] * 1  + self.items_data[solution[i]]["param"]["health"]["perLevel"] * 18) / 8.5 \
                            + (self.items_data[solution[i]]["param"]["healthRegen"]["percent"])/7 ) + (self.items_data[solution[i]]["param"]["attackSpeed"]["flat"]) * 1.2
                    
                    if enemy_reliant == 0:
                        enemy_reliant = self.en_tank * damage_importance * self.items_data[solution[i]]["param"]["armorPenetration"]["percent"]
                    
                    item_exists = any(item["name"] == solution[i] for item in self.suggested_items[champ_name])
                    if item_exists:
                        value += 350
                    value -= (self.items_data[solution[i]]["param"]["abilityPower"]["flat"] * 1  + self.items_data[solution[i]]["param"]["abilityPower"]["perLevel"] * 18)
                    if self.items_data[solution[i]]["rank"] in ["TURRET", "MINION", "POTION", "DISTRIBUTED"]:
                        value -= 300
                    elif self.items_data[solution[i]]["rank"] == "LEGENDARY":
                        value += 100

                    self.enemy_rel_val[i] = enemy_reliant    
                    self.item_itself_val[i] = value 
                    self.total_items_val[i] = value + enemy_reliant
                        
                        
            case "abilityPower":
                for i in changed_items:
                    enemy_reliant = self.en_tank * damage_importance * self.items_data[solution[i]]["param"]["magicPenetration"]["percent"]
                    
                    if damage_importance != 3:
                        enemy_reliant += (self.en_ad * toughness * self.items_data[solution[i]]["param"]["armor"]["flat"] \
                                + self.en_ap * toughness * self.items_data[solution[i]]["param"]["magicResistance"]["flat"])/2

                    value = damage_importance * (self.items_data[solution[i]]["param"]["abilityPower"]["flat"] * 1  + self.items_data[solution[i]]["param"]["abilityPower"]["perLevel"] * 18\
                        + (self.items_data[solution[i]]["param"]["cooldownReduction"]["flat"]*ability_rel\
                        + self.items_data[solution[i]]["param"]["abilityHaste"]["flat"]*ability_rel) / 50 ) \
                        + toughness * ((self.items_data[solution[i]]["param"]["health"]["flat"] * 1  + self.items_data[solution[i]]["param"]["health"]["perLevel"] * 18) / 8.5 \
                            + (self.items_data[solution[i]]["param"]["healthRegen"]["percent"])/7) 
                    
                    item_exists = any(item["name"] == solution[i] for item in self.suggested_items[champ_name])
                    if item_exists:
                        value += 350

                    if self.items_data[solution[i]]["rank"] in ["TURRET", "MINION", "POTION", "DISTRIBUTED"]:
                        value -= 300
                    elif self.items_data[solution[i]]["rank"] == "LEGENDARY":
                        value += 100

                    self.enemy_rel_val[i] = enemy_reliant    
                    self.item_itself_val[i] = value 
                    self.total_items_val[i] = value + enemy_reliant

            case "tank":
                for i in changed_items:
                    enemy_reliant = self.en_ad * toughness * self.items_data[solution[i]]["param"]["armor"]["flat"] \
                                + self.en_ap * toughness * self.items_data[solution[i]]["param"]["magicResistance"]["flat"]

                    value =  (self.items_data[solution[i]]["param"]["health"]["flat"] * 1  + self.items_data[solution[i]]["param"]["health"]["perLevel"] * 18) / 8.5 \
                            + (self.items_data[solution[i]]["param"]["healthRegen"]["percent"])/7 \
                        + (self.items_data[solution[i]]["param"]["cooldownReduction"]["flat"]*ability_rel\
                        + self.items_data[solution[i]]["param"]["abilityHaste"]["flat"]*ability_rel) / 50  
        
                    item_exists = any(item["name"] == solution[i] for item in self.suggested_items[champ_name])
                    if item_exists:
                        value += 350
                    if self.items_data[solution[i]]["rank"] in ["TURRET", "MINION", "POTION", "DISTRIBUTED"]:
                        value -= 300
                    elif self.items_data[solution[i]]["rank"] == "LEGENDARY":
                        value += 100

                    self.enemy_rel_val[i] = enemy_reliant    
                    self.item_itself_val[i] = value 
                    self.total_items_val[i] = value + enemy_reliant
        
        
        sum_value = sum(self.total_items_val)

        #       suma  lista wartosci f celu dla przedmiotu
        return sum_value, self.total_items_val, self.item_itself_val, self.enemy_rel_val

    def simulated_annealing(self,champ_name: str, initial_solution: list, how_to_nieghbour: list, T_init: float, T_final: float, alfa: float, enemy_champs: list):

        # assign values to variables
        T = T_init
        solution = initial_solution.copy()
        f_solution,item_importance_list,value_list,enemy_rel_list = self.objective_function(champ_name,solution,[x for x in range(self.no_of_items)] )
        T_change = [T_init]   # values of temperature in iterations
        f_change = []  # f_values of accepted solutions 
        number_of_iterations = 0
        best_solution = None
        f_best_solution = 0
        counter = 0
        g, actual_g, best_g = None, None, None

        while T > T_final:

            # choose new solution from the neighbours of current solution
            new_solution = []
            

            # take out number corresponding to nighbourhood-making function 
            n = how_to_nieghbour[counter]
            if n not in [4,5,6]:
                new_solution,g,indexes_of_changed_items = self.neighbour_dict[n](solution)

            else:
                # use the same function with different input list to achieve dufferent nighbours
                match n:
                    case 4:
                        new_solution,g,indexes_of_changed_items = self.neighbour_dict[4](solution,item_importance_list)
                    case 5:
                        new_solution,g,indexes_of_changed_items = self.neighbour_dict[4](solution,value_list)
                    case 6:
                        new_solution,g,indexes_of_changed_items = self.neighbour_dict[4](solution,enemy_rel_list)
            
            # update counter and reset if necessary
            counter += 1
            if counter == len(how_to_nieghbour):
                counter = 0
            
            # calculate objective function for new solution
            f_new_solution,item_importance_list,value_list,enemy_rel_list = self.objective_function(champ_name,new_solution,indexes_of_changed_items)

            # compare solutions
            delta = f_new_solution - f_solution

            # if new solution is better -> accept it
            if delta > 0:
                solution = new_solution.copy()
                f_solution = f_new_solution
                f_change.append(f_solution)
                actual_g = g
            # if new solution is worse than current solution calculate propability given by the formula
            else:
                propability = exp(delta / T)
                # if propability is greater than random value form (0,1) accept new solution even though it's worse
                if random() < propability:
                    solution = new_solution.copy()
                    f_solution = f_new_solution
                    f_change.append(f_solution)
                    actual_g = g
                else:
                    f_change.append(f_solution)

            # compare to best solution
            if f_best_solution < f_solution:
                    f_best_solution = f_solution
                    best_solution = solution.copy()
                    best_g = actual_g

            # decrease temperature
            T = T * alfa

            # save temperature and update number of iterations
            T_change.append(T)
            number_of_iterations += 1

        # return solution, f_solution, best_solution, f_best_solution, T_change, f_change, number_of_iterations
        return SolutionHandler(solution, f_solution, actual_g, best_solution, f_best_solution, best_g, T_change, f_change, number_of_iterations)

    def set_no_of_items(self,number):
        if isinstance(number,int) and number in [4,5,6]:
            self.no_of_items = number
        else:
            print("Próba przypisania niewłaściwje wartości do no_of_items")
    
    def gold_setting(self, gold_cap):
        if isinstance(gold_cap,int) and gold_cap >= 0:
            self.gold_cap = gold_cap
        else:
            print("Nieprawidłowa wartość gold_cap - gold_cap musi być większe od 0 i być liczbą całkowitą")


class SolutionHandler:
    def __init__(self,solution, f_solution, actual_g, best_solution, f_best_solution, best_g, T_change, f_change, number_of_iterations):
        # solution, f_solution, best_solution, f_best_solution, T_change, f_change, number_of_iterations
        self.solution = solution
        self.f_solution = f_solution
        self.best_solution = best_solution
        self.f_best_solution = f_best_solution
        self.T_change = T_change
        self.f_change = f_change
        self.number_of_iterations = number_of_iterations
        self.actual_g = actual_g
        self.best_g = best_g

    def obj_func_plot(self):
        ax = plt.subplot()
        ax.plot(self.f_change)
        ax.set(title="Zmiany funkcji celu",xlabel="Iteracje")
        return ax
    
    def temperature_plot(self):
        ax = plt.subplot()
        ax.plot(self.T_change)
        ax.set(title="Temperatura",xlabel="Iteracje")

    def print_solution(self):
        print(f"Rozwiązanie końcowe:\n{self.solution}")
        print(f"Końcowa wartość funkcji celu: {self.f_solution}")
        print(f"Najlepsze rozwiązanie:\n{self.best_solution}")
        print(f"Najlepsza wartość funkcji celu: {self.f_best_solution}")
        print(f"Ilość iteracji: {self.number_of_iterations}")

    def get_string_solution(self):
        to_return = f"Rozwiązanie końcowe:\n{self.solution}\n\
Końcowa wartość funkcji celu: {self.f_solution}\n\
Koszt końcowego rozwiązania: {self.actual_g}\n\n\
Najlepsze rozwiązanie:\n{self.best_solution}\n\
Najlpesza wartość funkcji celu: {self.f_best_solution}\n\
Koszt najlepszego rozwiązania: {self.best_g}\n\n\
Ilość iteracji: {self.number_of_iterations}"
        return to_return

    def obj_func_fig(self):
        fig = Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.f_change)
        ax.set(title="Zmiana funkcji celu",xlabel="Iteracje")
        return fig
    
    def temperature_fig(self):
        fig = Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.T_change)
        ax.set(title="Temperatura",xlabel="Iteracje")
        return fig
    

def resource_path(relative_path):
    """ Uzyskuje absolutną ścieżkę do zasobu, działa zarówno dla .py, jak i .exe """
    if getattr(sys, 'frozen', False):  # Sprawdza, czy aplikacja działa jako .exe
        base_path = sys._MEIPASS  # Ścieżka tymczasowa dla zasobów w PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    example = ['Sunfire Aegis', "Sorcerer's Shoes", 'Base Turret Reinforced Armor (Turret Item)', "Executioner's Calling", 'Elixir of Wrath', "Doran's Ring"]
    random_champs = ['Elise', 'Fiddlesticks', 'Katarina', 'Shyvana', 'Vladimir', 'Teemo']
    ex2 = ['Sunfire Aegis', "Sorcerer's Shoes", 'Base Turret Reinforced Armor (Turret Item)', "Executioner's Calling"]

    alg = Algorithm()
    alg.set_no_of_items(4)
    alg.starting_enemy_parameters(random_champs)
    alg.gold_setting(2000)

    handler = alg.simulated_annealing("Illaoi",ex2,[1],500,10,0.99,random_champs)


    handler.print_solution()

    a1 = handler.obj_func_plot()
    plt.show()

    #a2 = handler.temperature_plot()
    #plt.show()

    #testy funkcji celu
    #seed_akt = seed(42)
    


if __name__ == "__main__":
    main()

