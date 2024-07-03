# 体認識と顔認識の数から次の行動を決める.

def nextAction (right_p, right_f, left_p, left_f):   # (右側で体認識できた数, 右側で顔認識できた数, 左側で体認識できた数, 左側で顔認識できた数)
    diff_right = right_p - right_f
    diff_left = left_p - left_f
    if (diff_right==0 and diff_left==0):
        next_action = 0
    elif (diff_right==0 and diff_left!=0):
        next_action = 1
    elif (diff_right!=0 and diff_left==0):
        next_action = 2
    elif (diff_right!=0 and diff_left!=0):
        next_action = 3
    return next_action