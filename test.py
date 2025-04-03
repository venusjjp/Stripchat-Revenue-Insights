import sys
from main import main

if len(sys.argv) == 1:
    nickname = input('请输入主播昵称:')
else:
    nickname = sys.argv[1]
main(nickname)
