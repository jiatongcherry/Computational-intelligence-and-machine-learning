import sys, grader, parse
import random

def calculate_V(grid, policy, value, noise, living_reward, discount, position):
    d = {'N':['N','E','W'], 'S':['S','E','W'], 'E': ['E', 'N', 'S'], 'W': ['W', 'N', 'S'], 'exit':'exit'}
    r, c = position
    intented_action = policy[r][c]
    move = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}
    if intented_action == 'exit':
        return grid[r][c]
    else:
        V = 0
        new_r, new_c = r + move[intented_action][0], c + move[intented_action][1]
        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and grid[new_r][new_c] != '#':
            V_intented = (1 - noise * 2) * (living_reward + discount * value[new_r][new_c])
            V += V_intented
        else:
            V_intented = (1 - noise * 2) * (living_reward + discount * value[r][c])
            V += V_intented

        other1_action = d[intented_action][1]
        new_r, new_c = r + move[other1_action][0], c + move[other1_action][1]
        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and grid[new_r][new_c] != '#':
            V_other1 = noise * (living_reward + discount * value[new_r][new_c])
            V += V_other1
        else:
            V_other1 = noise * (living_reward + discount * value[r][c])
            V += V_other1

        other2_action = d[intented_action][2]
        new_r, new_c = r + move[other2_action][0], c + move[other2_action][1]
        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and grid[new_r][new_c] != '#':
            V_other2 = noise * (living_reward + discount * value[new_r][new_c])
            V += V_other2
        else:
            V_other2 = noise * (living_reward + discount * value[r][c])
            V += V_other2

        return V

def list_to_formatted_string(matrix):
    formatted_rows = []
    for row in matrix:
        # 每个元素根据内容格式化：若为'#'则用'##### '，否则显示为'   0.00'格式
        formatted_row = ''.join([f"| ##### |" if val == '#' else f"| {val:6.2f}|" for val in row])
        formatted_rows.append(formatted_row)
    # 将所有行连接为多行字符串，每行换行
    return '\n'.join(formatted_rows)

def policy_evaluation(problem):

    # 创建value，记录每一个位置的V值
    value = [['#' if cell == '#' else 0 for cell in row] for row in problem['grid']]

    # 初始化return_value
    return_value = ''
    iterations = problem['iterations']
    return_value += "V^pi_k=0\n"
    return_value += list_to_formatted_string(value)

    # 开始迭代计算
    while iterations > 1:
        iterations -= 1
        new_value = [['#' if cell == '#' else 0 for cell in row] for row in problem['grid']]

        #循环遍历，计算每一个位置的值
        grid_row = len(problem['grid'])
        grid_col = len(problem['grid'][0])

        for i in range(grid_row):
            for j in range(grid_col):
                if problem['grid'][i][j] == '#':
                    V = "#"
                else:
                    V = calculate_V(problem['grid'], problem['policy'], value, problem['noise'], problem['livingReward'], problem['discount'], (i, j))
                new_value[i][j] = V

        value = new_value
        return_value += "\n"
        return_value += f"V^pi_k={problem['iterations'] - iterations}\n"
        return_value += list_to_formatted_string(value)

    return return_value

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)