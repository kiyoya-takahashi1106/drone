# 死ぬほどお試し(roo3.pyの前身となるコード多分)
# DFSを用いて1を一筆書き出来たらRoot発見できる(孤島に1が存在したりしてたら探索不可)

map = [
        [1, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 1 ,1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [1, 1, 1, 0]
      ]   
M = len(map)
N = len(map[0])
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # 動き方(上, 下, 左, 右)
all_path = []   # すべての探索pathを入れる

def dfs(visited_lst, path, x, y):   # (x,y)は探索してる場所
    if not (0 <= x < M and 0 <= y < N and map[x][y] == 1 and not visited_lst[x][y]):
        return   # 条件に合わなかったら親にreturn
    visited_lst[x][y] = True   # 訪問したからTrueにする
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
    print("-------------------------")

def find_paths():
    visited_lst = [[False] * N for hoge in range(M)]   # 初期化
    # 各1のところから探索開始している()
    for x in range(M):   
        for y in range(N):
            if map[x][y] == 1 and visited_lst[x][y] != True:
                path = []
                dfs(visited_lst, path, x, y)
    return all_path

find_paths()
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
min_zero_path = all_path[zero_count_lst.index(min_zero_count)]   # 0を一番通らないpath

# 出力
for x, y in min_zero_path:
    print(f"({x}, {y})")

