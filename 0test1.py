# droneの初期位置はMap[0][0]に下向き(↓)を想定
Map = [
        [1, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 1, 0] 
      ]
y_Distance = 30
x_Distance = 50
root = [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2], [1, 2], [1, 3], [1, 2]]   # (y, x)

for i, (y, x) in enumerate(root):   # i:idxnum
    if(i == 0):
        pass
    else:
        change_y, change_x = y - old_y, x - old_x
        if(change_y == 0):   # x方向に動く
            hoge = "left"
            distance = x_Distance * change_x
        else:                # y方向に動く
            hoge = "forward"
            distance = y_Distance * change_y
        print(f"{hoge} {distance}")
    old_y, old_x = y, x