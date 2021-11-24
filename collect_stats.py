import utils
import tree_search
import timeit
from tabulate import tabulate
import pandas as pd

def collect_stats(start_station,end_station,algorithms):
    df = pd.DataFrame(columns=["Algorithm","time to destination","number of tube lines used","nodes expanded","time taken"])
    for algorithm in algorithms:
        begin = timeit.default_timer()
        all_expanded_nodes=tree_search.tree_search(start_station,end_station,algorithm)
        end = timeit.default_timer()
        number_of_nodes_expanded = len(all_expanded_nodes)
        path = utils.get_path(all_expanded_nodes)
        total_cost = utils.get_total_cost(path)
        num_lines = utils.get_number_of_lines(path)
        df = df.append({"Algorithm": algorithm, "time to destination": total_cost, "number of tube lines used": num_lines, "nodes expanded": number_of_nodes_expanded,
                        "time taken": end-begin}, ignore_index=True)

    print(tabulate(df, headers='keys', tablefmt='psql'))
