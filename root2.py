# 手順➀BFSでmapをgroupごとに分ける. groupごとの輪郭を格納していく.(これはroot4.pyの前身となる.)

# droneの初期位置はMap[0][0]に下向き(↓)を想定
map = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
      ]
M = len(map)  # y軸方向
N = len(map[0])  # x軸方向
movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 動き方(上, 下, 左, 右)
people_lst = []  # 人がいる場所
groups = []
around_groups = []

# people_lstを作る
for i in range(M):
    for j in range(N):
        if map[i][j] == 1:
            people_lst.append([i, j])
people_lst_copy = people_lst.copy()

# BFSでstartを含むグループ化する. ついでにgroupの輪郭たちも格納していく.
def bfs(start):
    queue = [start]
    group = []
    around_group = []
    while queue:
        y, x = queue.pop(0)
        if ([y, x] in people_lst):
            people_lst.remove([y, x])
            group.append([y, x])
            for movement_y, movement_x in movements:
                new_y, new_x = y + movement_y, x + movement_x
                if(0 <= new_y < M and 0 <= new_x < N and [new_y, new_x] in people_lst):
                    queue.append([new_y, new_x])
                if(0 > new_y or new_y >= M or 0 > new_x or new_x >= N or [new_y, new_x] not in people_lst_copy):
                    if [y, x] not in around_group:  # 同じ点を複数回追加しないようにする
                        around_group.append([y, x])   # 輪郭をappendしていく.
    return  group, around_group

while people_lst:
    start = people_lst[0]
    group, around_group = bfs(start)
    groups.append(group)
    around_groups.append(around_group)

print("groups", groups)
print("around_groups", around_groups)



"""
まずmapを取得するためになにかしらしないといけない(ex:椅子に重力センサを付けて人が座ってるか座ってないかを判定するなど)
"""