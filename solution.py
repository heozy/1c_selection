def send(command):
    print(command, flush=True)


# чтение карты
input()
day_cost = 0
entrance = None
profit = {}
graph = {}
prob = {}

while True:
    parts = input().split()
    if parts[0] == "END":
        break
    if parts[0] == "day_cost":
        day_cost = float(parts[1])
    elif parts[0] == "entrance":
        entrance = parts[1]
    elif parts[0] == "vertex":
        profit[parts[1]] = float(parts[2])
        graph[parts[1]] = []
    elif parts[0] == "edge":
        edge_id, a, b = parts[1], parts[2], parts[3]
        graph[a].append((edge_id, b))
        graph[b].append((edge_id, a))
        prob[edge_id] = float(parts[4])

send("END")
