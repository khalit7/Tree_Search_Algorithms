import utils
import cost_functions
all_paths = utils.read_file("tubedata.csv")
all_routs = utils.get_map_as_dict(all_paths)
staion_zones = utils.get_stations_zones(all_paths)


def tree_search(start,end,algorithm):
    if algorithm == "BFS":
        return BFS(start,end)
    if algorithm == "DFS":
        return DFS_Search(start,end)
    if algorithm[0:3] == "UCS":
        return UCS_Search(start,end,algorithm)
    if algorithm[0:2] == "A*":
        return A_Search(start,end,algorithm)

def BFS(start,end):
    visited = {x: False for x in all_routs.keys()}
    queue = []
    queue.append(
        {"station": start,
         "current_line": "",
         "accumulated cost":0,
         "came_from": "root_station"}
    )
    all_nodes_expanded=[]
    visited[start]=True
    all_nodes_expanded.append(queue[0])
    if start==end:
        return all_nodes_expanded
    goal_found=False
    while queue:
        if(goal_found):
            break
        parent=queue.pop(0)
        for child in all_routs[parent['station']]:
            if (not visited[child['destination']]):
                visited[child['destination']]=True

                temp = {"station": child['destination'],
                 "current_line": child['line'],
                        "accumulated cost":child['avg_time']+parent['accumulated cost'],
                 "came_from": parent}
                queue.append(temp)
                all_nodes_expanded.append(temp)
                if child['destination']==end:
                    goal_found=True
                    break
    return all_nodes_expanded



def DFS_Search(start,end):
    visited = {x: False for x in all_routs.keys()}

    parent = {"station": start,
         "current_line": "",
         "accumulated cost": 0,
         "came_from": "root_station"}

    all_nodes_expanded = []

    if start == end:
        return [parent]
    def DFS(parent):
        nonlocal visited, all_nodes_expanded,end
        if visited[end] == True:
            return
        visited[parent['station']] = True
        all_nodes_expanded.append(parent)
        for child in all_routs[parent['station']]:
            if (not visited[child['destination']]):
                temp = {"station": child['destination'],
                        "current_line": child['line'],
                        "accumulated cost": child['avg_time'] + parent['accumulated cost'],
                        "came_from": parent}
                DFS(temp)
    DFS(parent)
    return all_nodes_expanded

def UCS_Search(start,end,algorithm):
    visited = {x: False for x in all_routs.keys()}
    sorting_tech = {"UCS_time":"accumulated cost","UCS_line_changes":"accumulated changes"}
    queue=[]
    queue.append({"station": start,
         "current_line": "",
         "accumulated cost": 0,
         "accumulated changes":0,
         "came_from": "root_station"} )
    all_nodes_expanded = []
    if start == end:
        return all_nodes_expanded
    while (queue):
        queue.sort(key=lambda x:x[sorting_tech[algorithm]])
        parent = queue.pop(0)
        if (not visited[parent['station']]):
            visited[parent['station']] = True
            all_nodes_expanded.append(parent)
            if parent['station'] == end:
                break
            for child in all_routs[parent['station']]:
                accumulated_cost,accumulated_changes = cost_functions.UCS_cost_function(parent,child)

                temp = {"station": child['destination'],
                        "current_line": child['line'],
                        "accumulated cost": accumulated_cost,
                        "accumulated changes": accumulated_changes,
                        "came_from": parent}
                queue.append(temp)
    return all_nodes_expanded


def A_Search(start,end,algorithm):
    visited = {x: False for x in all_routs.keys()}
    queue = []
    queue.append({"station": start,
                  "current_line": "",
                  "accumulated cost": 0,
                  "accumulated changes": 0,
                  "heuristic_cost":0,
                  "came_from": "root_station"})
    all_nodes_expanded = []
    if start == end:
        return all_nodes_expanded
    while (queue):
        queue.sort(key=lambda x: x["accumulated cost"] + x["heuristic_cost"])
        parent = queue.pop(0)
        if (not visited[parent['station']]):
            all_nodes_expanded.append(parent)
            if parent['station'] == end:
                break
            visited[parent['station']] = True
            for child in all_routs[parent['station']]:
                accumulated_cost,accumulated_changes = cost_functions.UCS_cost_function(parent, child)
                heuristic_cost = cost_functions.heuristic_value (child['destination'],end,staion_zones,algorithm=algorithm)

                temp = {"station": child['destination'],
                        "current_line": child['line'],
                        "accumulated cost": accumulated_cost,
                        "accumulated changes": accumulated_changes,
                        "heuristic_cost": heuristic_cost,
                        "came_from": parent}
                queue.append(temp)
    return all_nodes_expanded