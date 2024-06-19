map = [
        [1, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 1, 1, 1]
      ]
M = len(map)
N = len(map[0])
groups = [
            [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]], 
            [[2, 2], [2, 3], [3, 3]], 
            [[3, 0]], 
            [[4, 1], [5, 1], [4, 2], [5, 0], [5, 2], [5, 3]]
         ]
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # 動き方(上, 下, 左, 右)

def bfs(group):
    all_paths = []
    for start in group:
        queue = [(start, [start], 0)]   # (current position, path, count_waste)
        visited = set()
        visited.add(tuple(start))
        
        while queue:
            (x, y), path, count_waste = queue.pop(0)
            
            if all(map[i][j] == 0 or (i, j) in visited for i in range(M) for j in range(N)):
                all_paths.append((path, count_waste))
                break
            
            for dx, dy in movements:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < M and 0 <= new_y < N and map[new_x][new_y] == 1 and (new_x, new_y) not in visited:
                    queue.append(((new_x, new_y), path + [(new_x, new_y)], count_waste))
                    visited.add((new_x, new_y))
                
                # 0 を通る場合もカウントして探索を続ける
                elif 0 <= new_x < M and 0 <= new_y < N and map[new_x][new_y] == 0:
                    queue.append(((new_x, new_y), path + [(new_x, new_y)], count_waste + 1))
                    visited.add((new_x, new_y))
    
    # 最短ルートを探す
    if all_paths:
        min_waste_path = min(all_paths, key=lambda x: x[1])
        return min_waste_path[0]  # 最短ルートを返す
    
    return []

def find_paths():
    all_paths = []
    for group in groups:
        path = bfs(group)
        if path:
            all_paths.append(path)
    return all_paths

all_path = find_paths()
print(all_path)

# path中で0を通る数をカウントする関数
def count_zeros(map, path):
    count_zero = 0
    for i, j in path:
        if map[i][j] == 0:
            count_zero += 1
    return count_zero

zero_count_lst = []
for path in all_path:
    zero_count_lst.append(count_zeros(map, path))

min_zero_count = min(zero_count_lst)
min_zero_path = all_path[zero_count_lst.index(min_zero_count)]  # 0を一番通らないpath

# 出力
for x, y in min_zero_path:
    print(f"({x}, {y})")
