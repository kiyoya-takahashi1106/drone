# 手順➀BFSでmapをgroupごとに分ける.

map = [
        [1, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 1, 1, 1]
      ]
M = len(map)  # y軸方向
N = len(map[0])  # x軸方向
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 動き方(上, 下, 左, 右)
people_lst = []  # 人がいる場所
groups = []

# people_lstを作る
for i in range(M):
    for j in range(N):
        if map[i][j] == 1:
            people_lst.append([i, j])
print("people_lst", people_lst)

# BFSでstartを含むグループ化する
def bfs(start):
    queue = [start]
    group = []
    while queue:
        y, x = queue.pop(0)
        if ([y, x] in people_lst):
            people_lst.remove([y, x])
            group.append([y, x])
            for movement_y, movement_x in movements:
                new_y, new_x = y + movement_y, x + movement_x
                if (0 <= new_y < M and 0 <= new_x < N and [new_y, new_x] in people_lst):
                    queue.append([new_y, new_x])
    return group

while people_lst:
    start = people_lst[0]
    group = bfs(start)
    groups.append(group)

print("groups", groups)



"""
まずmapを取得するためになにかしらしないといけない(ex:椅子に重力センサを付けて人が座ってるか座ってないかを判定するなど)
"""