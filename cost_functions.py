import tree_search
import utils

#UCS cost functions ==> time based cost function, number of line changes cost function
def UCS_cost_function(parent, child):

        accumulated_cost = child['avg_time'] + parent['accumulated cost']

        if (parent['current_line'] != child['line']):
            return (accumulated_cost,parent['accumulated changes'] + 1)
        return (accumulated_cost,parent['accumulated changes'])



# getting the heuristic value depending on the zones difference
def heuristic_zoneBased(current,end,stationsZones):
  if(current==end):
    return 0
  return max(abs(min(stationsZones[current])-max(stationsZones[end])),abs(min(stationsZones[end])-max(stationsZones[current])))


#getting the heuristic value using optimal search algorithm
def heuristic_dijkstraBased (current,end):
    all_nodes_expanded = tree_search.UCS_Search(current,end,algorithm="UCS_time")
    if(all_nodes_expanded.__len__()==0):
        return 0
    path = utils.get_path(all_nodes_expanded)
    total_cost = utils.get_total_cost(path)
    return total_cost

def heuristic_value (current,end,stationsZones,algorithm):
    if algorithm == "A*_zone_based":
        return heuristic_zoneBased(current,end,stationsZones)
    elif algorithm == "A*_dijkstra_based":
        return heuristic_dijkstraBased(current,end)
    else:
        raise Exception("invalid algorithm")