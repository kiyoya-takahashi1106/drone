# 手順➁root2.pyで分けた各グループごとにBFSで探索する.

# droneの初期位置はMap[0][0]に下向き(↓)を想定
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
groups = [[[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]], 
          [[2, 2], [2, 3], [3, 3]], 
          [[3, 0]], 
          [[4, 1], [5, 1], [4, 2], [5, 0], [5, 2], [5, 3]]
         ]
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(group, all_path, path, visited_lst, count_waste, x, y):
    if not (0 <= x < M and 0 <= y < N and map[x][y] == 1 and not visited_lst[x][y]):
        return
    visited_lst[x][y] = True
    path.append((x, y))
    print(path)

    # すべて探索していればall_pathに入れる
    if all(map[i][j] == 0 or visited_lst[i][j] == True for i in range(M) for j in range(N)):
        all_path.append(path[:])
    # まだ探索してない箇所があれば探索する
    else:
        for dx, dy in movements:
            new_x = x + dx
            new_y = y + dy
            dfs(visited_lst, path, new_x, new_y)
        
    path.pop()   # 戻るときにパスから削除
    visited_lst[x][y] = False   # 戻るときに訪問リストを戻す


def find_paths(group):
    all_path = []
    visited_lst = [[False]*N for hoge in M]
    # groupの中から開始する
    for [x, y] in group:
        count_waste = 0
        path = []
        dfs(group, all_path, path, visited_lst, count_waste, x, y)
        # 1だけ通って一筆書きならこのgroupの探索終了
        if(count_waste == 0):
            break

for group in groups:
    find_paths(group)



"""
"""