# 手順➃root4.pyで決めたrootをまとめる.(ex:forward5回を1回にまとめたりする.)

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
root = [[0, 2], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [4, 3], [5, 3], [5, 2], [4, 2], [4, 1], [5, 1], [5, 0], [4, 0], [3, 0]]
delete_idx = []

# 一つ前と同じ移動の仕方ならその真ん中にあるrootを消す関数.
# ex:[[0, 0], [1, 0], [2, 0]]というrootがあれば2つの移動はどちたもy軸方向に正の方に移動してるのでこれらをまとめて[[0, 0], [2, 0]]とする.
def ware_up_root():   
    for i, [element_y, element_x] in enumerate(root):
        if(i == 0):
            now_input_y, now_input_x = element_y, element_x
        elif(i == 1):
            once_prev_input_y, once_prev_input_x = now_input_y, now_input_x
            now_input_y, now_input_x = element_y, element_x
        else:
            secound_prev_input_y, secound_prev_input_x = once_prev_input_y, once_prev_input_x
            once_prev_input_y, once_prev_input_x = now_input_y, now_input_x
            now_input_y, now_input_x = element_y, element_x
            change_y = secound_prev_input_y - now_input_y
            change_x = secound_prev_input_x - now_input_x
            if(change_x == -2 or change_x == 2 or change_y == -2 or change_y == 2):
                delete_idx.append(i - 1)   # 消すidxを格納

    delete_idx.reverse()   # 逆にしないと後ろidxが一つずつずれる
    for idx in delete_idx:
        root.pop(idx)
    return root

print(ware_up_root())