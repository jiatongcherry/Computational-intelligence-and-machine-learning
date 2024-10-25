import sys, grader, parse
import random
from collections import Counter
from decimal import Decimal, getcontext

def find_true_direction(d, a, n):
    if a == 'exit':
        return 'exit'
    return random.choices(population = d[a], weights = [1 - n*2, n, n])[0]

def update_P_position(grid, action, P_position):
    # 克隆原始网格以防止修改原始数据
    new_grid = [row[:] for row in grid]
    final_step = False
    P_r, P_c = P_position

    # 定义移动方向
    moves = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }

    if action == 'exit':
        final_step = True
        return new_grid, final_step

    # 计算新的位置
    if action in moves:
        delta_r, delta_c = moves[action]
        new_r, new_c = P_r + delta_r, P_c + delta_c

        # 检查新位置是否在网格范围内
        if 0 <= new_r < len(new_grid) and 0 <= new_c < len(new_grid[0]):
            # 检查新位置是否是障碍
            if new_grid[new_r][new_c] != '#':
                # 移动P到新位置，清空原位置
                new_grid[new_r][new_c] = 'P'
            else:
                new_grid[P_r][P_c] = 'P'
        else:
            new_grid[P_r][P_c] = 'P'

    return new_grid, final_step

def find_character(grid, character):
    """
    在给定的二维列表 grid 中查找字符 character 的位置。
    如果找到，返回其位置 (row, col)。
    如果没有找到，返回 None。
    """
    for i, row in enumerate(grid):
        if character in row:
            col = row.index(character)
            return (i, col)
    return None

def grid_to_string(grid):
    result = []
    for row in grid:
        # 在每行的开头添加 4 个空格，并确保每个元素占据 4 个字符宽度
        formatted_row = ''.join(f"{elem:>5}" for elem in row)
        result.append(formatted_row)
    # 将所有行用换行符连接起来
    return '\n'.join(result)

def format_score(score):
    # 转换为 float 判断是否是整数
    score_float = float(score)
    # 如果是整数，强制显示一位小数
    if score_float.is_integer():
        return f"{score_float:.1f}"
    # 如果是小数且不需要尾随的0，则直接返回normalize后的结果
    return f"{score.normalize()}"

def play_episode(problem):
    # 初始化分数
    getcontext().prec = 28
    score = Decimal('0')

    # 设置随机数种子
    seed = problem['seed']
    if seed != -1:
        random.seed(seed, version=1)
    n = problem['noise']
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S','N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}

    # 设置experience中的初始几行
    experience = ''
    experience += "Start state:\n"
    grid = [row[:] for row in problem['grid']]
    S_r, S_c = find_character(grid, "S")
    grid[S_r][S_c] = "P"
    experience += grid_to_string(grid)
    experience += f"\nCumulative reward sum: {format_score(score)}\n"

    # 开始游戏
    while True:
        P_r, P_c = find_character(grid, "P")
        a = problem['policy'][P_r][P_c]
        True_a = find_true_direction(d, a, n)
        new_grid, final_step = update_P_position(problem['grid'], True_a, (P_r, P_c))
        grid = new_grid

        # 判断游戏是否结束
        if final_step:
            experience += "-------------------------------------------- \n"
            experience += "Taking action: exit (intended: exit)\n"
            experience += f"Reward received: {float(problem['grid'][P_r][P_c])}\n"
            experience += "New state:\n"
            experience += grid_to_string(grid)
            score += Decimal(problem['grid'][P_r][P_c])
            experience += f"\nCumulative reward sum: {format_score(score)}"
            return experience
        else:
            score += Decimal(str(problem['living_reward']))
            experience += "-------------------------------------------- \n"
            experience += f"Taking action: {True_a} (intended: {a})\n"
            experience += f"Reward received: {problem['living_reward']}\n"
            experience += "New state:\n"
            experience += grid_to_string(grid)
            experience += f"\nCumulative reward sum: {format_score(score)}\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)

