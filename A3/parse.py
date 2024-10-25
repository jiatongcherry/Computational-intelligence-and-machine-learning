def read_grid_mdp_problem_p1(file_path):
    problem = {}
    grid = []
    policy = []
    current_section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("seed:"):
                problem['seed'] = int(line.split(':')[1].strip())
            elif line.startswith("noise:"):
                problem['noise'] = float(line.split(':')[1].strip())
            elif line.startswith("livingReward:"):
                problem['living_reward'] = float(line.split(':')[1].strip())
            elif line == "grid:":
                current_section = 'grid'
            elif line == "policy:":
                current_section = 'policy'
            else:
                if current_section == 'grid':
                    row = line.split()
                    grid.append(row)
                elif current_section == 'policy':
                    row = line.split()
                    policy.append(row)

    problem['grid'] = grid
    problem['policy'] = policy

    return problem

def read_grid_mdp_problem_p2(file_path):
    # 初始化 problem 字典
    problem = {
        "grid": [],
        "policy": []
    }

    # 读取文件内容
    with open(file_path, 'r') as file:
        # 读取每一行
        lines = file.readlines()

        # 标志是否进入 grid 或 policy 数据区
        in_grid_section = False
        in_policy_section = False

        for line in lines:
            line = line.strip()  # 去除行首尾的空格
            # 跳过空行
            if not line:
                continue

            # 判断是否进入 grid 数据区
            if line.startswith("grid:"):
                in_grid_section = True
                in_policy_section = False
                continue
            # 判断是否进入 policy 数据区
            elif line.startswith("policy:"):
                in_policy_section = True
                in_grid_section = False
                continue

            # 解析 grid 数据区
            if in_grid_section:
                grid_row = []
                for x in line.split():
                    if x == '_':  # 可移动的普通格子
                        grid_row.append(0)
                    elif x == 'S':  # 起点
                        grid_row.append('S')
                    elif x == '#':  # 墙壁，无法通行
                        grid_row.append('#')
                    else:
                        grid_row.append(int(x))  # 终点的奖励值或惩罚值
                problem["grid"].append(grid_row)
            # 解析 policy 数据区
            elif in_policy_section:
                policy_row = line.split()
                problem["policy"].append(policy_row)
            # 解析前面的键值数据区
            else:
                key, value = line.split(': ')
                # 判断数据类型并存储在字典中
                problem[key] = int(value) if value.isdigit() else float(value) if '.' in value else value

    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("discount:"):
            problem['discount'] = float(line.split(":")[1].strip())
        elif line.startswith("noise:"):
            problem['noise'] = float(line.split(":")[1].strip())
        elif line.startswith("livingReward:"):
            problem['livingReward'] = float(line.split(":")[1].strip())
        elif line.startswith("iterations:"):
            problem['iterations'] = int(line.split(":")[1].strip())
        elif line.startswith("grid:"):
            problem['grid'] = []
        elif line.strip():  # Process grid rows
            row = [cell.strip() if cell.strip() in ('_', '#', 'S') else float(cell.strip()) for cell in line.split()]
            problem['grid'].append(row)

    return problem
