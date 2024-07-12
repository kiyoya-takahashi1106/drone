import sys

# コマンドライン引数から値を取得
if len(sys.argv) > 1:
    input_value = sys.argv[4]
else:
    input_value = input("Enter a value: ")

# 入力された値を整数に変換して表示
print(int(input_value))
