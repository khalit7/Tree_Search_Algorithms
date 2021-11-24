import csv
from collections import defaultdict
# zones not available in given dataset
missingEndStationsZone={
  "Epping":[6],
  "Heathrow Terminal 3":[6],
  "Upminster":[6],
  "New Cross Gate":[2],
  "Watford":[7],
  "New Cross":[2],
  "Amersham":[9],
  "Brixton":[2],
  "Morden":[4],
  "Uxbridge":[6]
}
# reading and cleaning data
def read_file(file_name):
    map = []
    with open(file_name, 'r') as csvfile:
        x = csv.reader(csvfile)
        for row in x:
            map.append(row)
    # editing one wrong entry
    map[342][2:4]=[]
    map[342][1]=map[343][0]
    # cleaning
    for i in map:
        i[0] = i[0].strip().replace('"',"")
        i[1] = i[1].strip().replace('"', "")
        i[2] = i[2].strip().replace('"', "")
        i[3] = i[3].strip().replace('"', "")
        i[4] = i[4].strip().replace('"', "")
        i[5] = i[5].strip().replace('"', "")
    return map
# returns all zones with their corrosponding zones
def get_stations_zones(map):
      stationsZones={}
      for data in map:
        # translating the value of a,b,c,d zones to it's equvillent number
        if(data[4]=='a') or (data[4]=='b'):
          mainZone=7
        elif(data[4]=='c'):
          mainZone=8
        elif(data[4]=='d'):
          mainZone=9
        else:
          mainZone=int(data[4])
        if (data[5] == 'a') or (data[5] == 'b'):
          SecondaryZone = 7
        elif (data[5] == 'c'):
          SecondaryZone = 8
        elif (data[5] == 'd'):
          SecondaryZone = 9
        else:
          SecondaryZone = int(data[5])
        # geeting the zones of each station
        if(SecondaryZone==0):
          stationsZones[data[0]]=[mainZone]
        else:
          stationsZones[data[0]]=[mainZone,SecondaryZone]

        # adding the missing end stations zones
      for key, value in missingEndStationsZone.items():
        stationsZones[key] = value
      return stationsZones



def get_map_as_dict(map):
  all_routs = defaultdict(list)
  for path in map:
      start = path[0]
      end = path[1]
      line = path[2]
      avg_time= [int(s) for s in path[3] if s.isdigit()][0]
      main_zone = path[4]
      secondary_zone = path[5]
      all_routs[start].append({"destination":end,"line":line,"avg_time":avg_time,"main_zone":main_zone,"secondary_zone":secondary_zone})
      all_routs[end].append({"destination":start,"line":line,"avg_time":avg_time,"main_zone":main_zone,"secondary_zone":secondary_zone})
  return all_routs

def get_path(all_nodes_expanded):
  node = all_nodes_expanded[-1]
  path=[]
  while node["came_from"] != "root_station":
    path.append(node)

    node = node["came_from"]

  path.append(all_nodes_expanded[0])
  path.reverse()
  return path

def get_total_cost(path):

  cost = path[-1]["accumulated cost"]

  return cost

def get_number_of_lines (path):
    lines=set()
    for p in range(1,len(path)):
        lines.add(path[p]['current_line'])
    return len(lines)

def get_line_information(path):
    line=path[1]['current_line']
    information =[]
    if len(path)>0:
        start=0
        for p in range(1,len(path)):
            if line != path[p]['current_line'] or p==len(path)-1:
                information.append(line+" Line " + "From :"+path[start]['station'] + " To : "+path[p]['station'])
                line = path[p]['current_line']
                start=p

        return information
    else:
        return []


def beautify_path(path):
  beauty_path = []
  for p in path:
    beauty_path.append(p["station"])
  return " ==> ".join(beauty_path)