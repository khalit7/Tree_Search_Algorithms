#algorithms implemented:
# BFS ==> normal BFS
# DFS ==> normal DFS
# UCS_time ==> UCS that considers the time as the cost
# UCS_line_changes ==> UCS that condiders the number of line changes as the cost
# A*_zone_based ==> A* search that uses the time as the cost and difference between zones as the heuristic
# A*_dijkstra_based ==> A* search that uses the time as the cost and the actual cost to the goal as the heuristic
import os
import sys

import utils
import tree_search
import collect_stats

algorithms = ["BFS","DFS","UCS_time","UCS_line_changes","A*_zone_based","A*_dijkstra_based"]
## get user input
exit = False
while True:
    if (exit):
        break
    print()
    start_station = input("Enter your starting station : ").strip()
    if (not tree_search.all_routs[start_station]): # no station has that name:
        input("no station has that name, press enter to try again")
        if sys.stdin and sys.stdin.isatty():
            # running in terminal
            os.system("cls")
        continue
    print()
    end_station = input("Enter your destination : ").strip()
    if (not tree_search.all_routs[end_station]): # no station has that name:
        input("no station has that name, press enter to try again")
        if sys.stdin and sys.stdin.isatty():
            # running in terminal
            os.system("cls")
        continue
    print()

    if (start_station == end_station):
        print("you are already at your destination")
        print()
        input("Press enter to try another trip")
        if sys.stdin and sys.stdin.isatty():
            # running in terminal
            os.system("cls")
        continue

    while True:
        try:
            print("select a number to specify the algorithm for the search : ")
            print()
            print("-1", "==>", "exit")
            print("-2", "==>", "exit and choose another trip")
            for i in range(len(algorithms)):
                print(str(i),"==>",algorithms[i])
            print("6","==>","collect stats of all algorithms in a neat looking table")
            choice = input("your choice : ")
            print()
            if (choice=="-1"):
                exit=True
                break
            if (choice == "-2"):
                break
                if sys.stdin and sys.stdin.isatty():
                    # running in terminal
                    os.system("cls")
            if (choice=="6"):
                collect_stats.collect_stats(start_station,end_station,algorithms)
                print()
                input("Press enter to try another algorithm")
                if sys.stdin and sys.stdin.isatty():
                    # running in terminal
                    os.system("cls")
                continue
            algorithm = algorithms[int(choice)]
            all_expanded_nodes = tree_search.tree_search(start_station,end_station,algorithm)
            number_of_nodes_expanded = len(all_expanded_nodes)
            path = utils.get_path(all_expanded_nodes)
            total_cost = utils.get_total_cost(path)
            num_of_changes=utils.get_number_of_lines(path)
            information = utils.get_line_information(path)

            print("The path : ")
            print()
            print(utils.beautify_path(path))
            print()
            print("Total time for the trip : " , total_cost , "mins")
            print("number of lines used" , num_of_changes , "lines")
            print("Number of nodes expanded ", number_of_nodes_expanded,"node")
            print()
            print()
            print("ride guide : ")
            print()
            print("\n".join(information))
            print()
            input("Press enter to try another algorithm")
            if sys.stdin and sys.stdin.isatty():
                # running in terminal
                os.system("cls")
            continue
        except:
            print()
            input("you have entered something wrong .. press enter to try again")
            if sys.stdin and sys.stdin.isatty():
                # running in terminal
                os.system("cls")
            break
