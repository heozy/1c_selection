from collections import deque


def send(command):
    print(command, flush=True)


def look(room):
    send("LOOK")
    for _ in graph[room]:
        _, edge_id, _, status = input().split()
        state[edge_id] = status


def walk(start, target):
    # ищем путь по целым ходам обходом в ширину и идём по нему
    prev = {start: None}
    queue = deque([start])
    while queue:
        room = queue.popleft()
        if room == target:
            break
        for edge_id, nxt in graph[room]:
            if state.get(edge_id) == "OK" and nxt not in prev:
                prev[nxt] = (edge_id, room)
                queue.append(nxt)

    path = []
    room = target
    while prev[room] is not None:
        edge_id, room = prev[room]
        path.append(edge_id)

    for edge_id in reversed(path):
        send(f"MOVE {edge_id}")
        input()


def explore(position, todo):
    # осмотр и переходы бесплатны, поэтому обходим всё, куда можно дойти
    while todo:
        room = todo.pop()
        if room in visited:
            continue
        walk(position, room)
        position = room
        visited.add(room)
        look(room)
        for edge_id, nxt in graph[room]:
            if state[edge_id] == "OK" and nxt not in visited:
                todo.append(nxt)
    return position


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

state = {}
visited = set()

position = explore(entrance, [entrance])

# расчищаем самый выгодный обвал, пока выгода больше платы за день
while True:
    best_edge = None
    best_gain = 0
    for room in graph:
        if room not in visited:
            continue
        for edge_id, nxt in graph[room]:
            if state[edge_id] == "BROKEN" and nxt not in visited:
                gain = profit[nxt]
                if gain > best_gain:
                    best_edge, best_gain, target = edge_id, gain, nxt

    if best_edge is None or best_gain <= day_cost:
        break

    send(f"CLEAR {best_edge}")
    input()
    state[best_edge] = "OK"
    position = explore(entrance, [target])

send("END")