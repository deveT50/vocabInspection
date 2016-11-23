# coding: utf-8
import heapq
import itertools
#http://qiita.com/masashi127/items/0c794e28f4b295ad82c6

def astar(start, goal):
    # 探索した座標を格納する経路リスト
    passed_list = [start]
    # 初期スコア
    #=それまでの移動マス数+その点からゴールまでの最短距離S→h、h→G
    init_score = distance(passed_list) + heuristic(start,goal)
    # 探索済み座標と、その座標に辿り着いた経路のスコアを格納
    #dictで格納{その点：その点でのスコア}
    #dictにはhashbleな値しか格納できない. listはunhashble
    checked = {start: init_score}
    # 経路リストとそのスコアを格納する探索ヒープ
    #リスト[]
    #heapはスタックとは異なり、
    searching_heap = []
    # 探索ヒープに経路リストを格納
    #heapqは要素をソートして保持する.popしたものはheapq中で最小のものであることが保証される
    #形式：（heap, (key,value)）
    heapq.heappush(searching_heap, (init_score, passed_list))
    # 探索不可能になるまで
    while len(searching_heap) > 0:
        # 現在までに探索した経路の中から、スコアが最小になる
        # ときのスコアと経路リストを取得
        #passed_listは経路リスト。値とリストを一緒に格納したから
        score, passed_list = heapq.heappop(searching_heap)
        # 最後に探索した座標
        last_passed_pos = passed_list[-1]
        # 最後に探索した座標が目的地なら探索ヒープを返す
        if last_passed_pos == goal:
            return passed_list
        # 最後に探索した座標の八方を探索
        # 壁にぶつからない値の組が帰る
        for pos in nexts(last_passed_pos):
            # 経路リストに探索中の座標を追加した一時リストを作成
            new_passed_list = passed_list + [pos]
            # 一時リストのスコアを計算
            pos_score = distance(new_passed_list) + heuristic(pos,goal)
            # 探索中の座標が、他の経路で探索済みかどうかチェック
            # 探索済みの場合、前回のスコアと今回のスコアを比較
            # 今回のスコアのほうが大きい場合、次の方角の座標の探索へ
            if pos in checked and checked[pos] <= pos_score:
                continue
            # 今回のスコアのほうが小さい場合、チェック済みリストに格納
            # 探索ヒープにスコアと経路リストを格納
            # スコアをより小さいものに更新
            checked[pos] = pos_score
            #新しく探索スべき座標として追加。
            #次のループの最初にゴールかどうか調べるとき、この座標が最小スコアならこれがチェックされることもあるだろう。
            heapq.heappush(searching_heap, (pos_score, new_passed_list))

    return []

def nexts(pos):
        ''' 探索中の座標から八方の座標を計算するジェネレーター'''
        #wall = "O"
        #+1,-1,''の組み合わせ（直積）である、9通りの値の組を作る
        for a, b in itertools.product([' + 1', ' - 1', ''], repeat=2):

            if a or b:
                #値の組を現在地に足して、壁に当たらなければ、タプルで返す
                #if dungeon[eval('pos[0]' + a)][eval('pos[1]' + b)] != wall:
                yield (eval('pos[0]' + a), eval('pos[1]' + b))

def heuristic(pos,goal):
    ''' 探索中の座標からゴールまでの最短距離のスコア '''
    #ユークリッド距離
    return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5

def distance(path):
    ''' スタートから探索中の座標までの距離のスコア '''
    #単に移動したマスの数
    return len(path)

def render_path(path):
    ''' 結果の出力 '''
    buf = [[ch for ch in l] for l in dungeon]

    for pos in path[1:-1]:
        buf[pos[0]][pos[1]] = "*"

    buf[path[0][0]][path[0][1]] = "s"
    buf[path[-1][0]][path[-1][1]] = "g"
    return ["".join(l) for l in buf]





if __name__ == "__main__":
    '''
    dungeon = [
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        'OS  O     O     O         O          O',
        'O   O  O  O  O            O    OOOO GO',
        'O      O     O  O   OOOO  O    O  OOOO',
        'OOOOOOOOOOOOOOOOOO  O     O    O     O',
        'O                O  O     O          O',
        'O        OOO     O  O     OOOOOOOOO  O',
        'O  OO    O    OOOO  O     O      OO  O',
        'O   O    O          O     O  O   O   O',
        'O   OOO  O          O        O   O   O',
        'O        O          O        O       O',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        ]
    '''
    #ある特定の単語の使用を避けて、目的のトピックの単語までの経路を導出できる。
    #単語空間は100次元とか。視覚的には2次元に落とすか、asterの方を100次元に対応させる。
    dungeon = [
        'OOOOOOOOOOOOOOOOO    O G OOO OOOOOOOOO',
        'OS  O     O     O   OOOOO            O',
        'O   O  O  O  O          OOO    OOOO GO',
        'O      O     O  O   OOOO  O    O  OOOO',
        'OOOOOOOOOOOOOOOOOO  O     O    O     O',
        'O                O  O     O          O',
        'O        OOO     O  O     OOOOOOOOO  O',
        'O  OO    O    OOOO  O     O      OO  O',
        'O   O    O          O     O  O   O   O',
        'O   OOO  O          O        O   O   O',
        'O        O          O        O       O',
        'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
        ]

    def find_ch(ch):
        for i, l in enumerate(dungeon):

            for j, c in enumerate(l):

                if c == ch:
                    return (i, j)
    # スタート
    init = find_ch("S")
    # ゴール
    goal = find_ch("G")

    

    path = astar(init, goal)

    if len(path) > 0:
        print("\n".join(render_path(path)))
    #探索すべき点がなくなって、なおかつゴールを発見できていなければ、|path|=0で終了するので
    else:
        print('failed')
