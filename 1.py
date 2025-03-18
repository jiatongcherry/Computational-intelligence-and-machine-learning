import numpy as np
import pandas as pd
import random

# 假设的门店数据（需求量）
data = {
    '门店编号': ['1', '2', '3', '4', '5', '6'],
    '门店位置': ['盒马鲜生1', '盒马鲜生2', '盒马鲜生3', '盒马鲜生4', '盒马鲜生5', '盒马鲜生6'],
    '需求量': [6000, 4000, 11000, 5000, 7000, 9000]
}

# 创建DataFrame
df = pd.DataFrame(data)
print(df)

# 手动输入距离矩阵
distance_matrix = np.array([
    [0, 28, 25, 11, 39, 36, 47],  # 仓储中心到各门店的距离
    [28, 0, 43, 22, 37, 10, 14],
    [25, 28, 0, 22, 60, 44, 45],
    [11, 22, 22, 0, 38, 26, 39],
    [39, 37, 60, 38, 0, 17, 16],
    [36, 10, 44, 26, 17, 0, 4.8],
    [47, 14, 45, 39, 16, 4.8, 0]
])

# 遗传算法参数
population_size = 60  # 种群规模
max_generations = 90  # 最大遗传代数
mutation_rate = 0.05  # 变异概率
vehicle_capacity = 8000 * 2  # 车辆载重（单位：公斤）


# 适应度函数
def fitness(route):
    total_distance = 0
    total_load = 0

    for i in range(len(route) - 1):
        # 计算距离
        if route[i] < len(distance_matrix) and route[i + 1] < len(distance_matrix):
            total_distance += distance_matrix[route[i], route[i + 1]]

        # 计算负载
        if route[i + 1] > 0:  # 只在访问门店时增加负载
            load = df['需求量'][route[i + 1] - 1]  # 需求量从1开始
            total_load += load

            # 检查负载是否超过容量
            if total_load > vehicle_capacity:
                return 0, 0, route  # 如果超重，适应度为0

            # 检查是否还有足够的容量去下一个门店
            if i + 2 < len(route) and route[i + 2] > 0:  # 检查下一个门店
                next_load = df['需求量'][route[i + 2] - 1]  # 需求量
                if total_load + next_load > vehicle_capacity:
                    return 0, 0, route  # 不允许访问

    return 1 / total_distance if total_distance > 0 else 0, total_load, route


# 初始化种群
def initialize_population():
    population = []
    for _ in range(population_size):
        # 随机选择部分门店进行配送
        route = random.sample(range(1, len(df) + 1), random.randint(1, len(df)))  # 随机选择1到所有门店
        population.append([0] + route + [0])  # 添加仓储中心到路径
    return population


# 选择操作
def selection(population):
    tournament_size = 5
    selected = []
    for _ in range(population_size):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda r: fitness(r)[0])  # 选择适应度最高的
        selected.append(winner)
    return selected


# 交叉操作
def crossover(parent1, parent2):
    size = len(parent1)

    # 确保路径中至少有两个门店以进行交叉
    if size <= 3:  # 只有仓库和一个门店的情况
        return parent1[:]  # 直接返回父母路径的副本

    child = [-1] * size
    start, end = sorted(random.sample(range(1, size - 1), 2))  # 随机选择交叉区间
    child[start:end] = parent1[start:end]

    # 填充父母中缺失的基因
    current_position = 0
    for gene in parent2[1:-1]:
        while gene in child:  # 跳过已存在的基因
            current_position += 1
            if current_position >= len(parent2) - 1:
                break
            gene = parent2[current_position]
        # 填充子代中为 -1 的位置
        for idx in range(1, size - 1):
            if child[idx] == -1:
                child[idx] = gene
                break

    child[0] = 0  # 开始点
    child[-1] = 0  # 结束点

    # 检查并填充任何仍为 -1 的位置
    for idx in range(1, size - 1):
        if child[idx] == -1:
            for gene in parent1[1:-1]:
                if gene not in child:
                    child[idx] = gene
                    break

    return child


# 变异操作
def mutate(route):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(1, len(route) - 1), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]  # 交换两个基因
        print(f"变异后的路径: {route}")  # 输出变异后的路径


# 遗传算法主循环
def genetic_algorithm():

    print(1)
    population = initialize_population()
    for generation in range(max_generations):
        population = selection(population)
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        # 只保留有效路径
        population = [route for route in new_population if fitness(route)[0] > 0]

        if not population:  # 如果没有有效路径，终止
            print(2)
            break

    best_route = max(population, key=lambda r: fitness(r)[0])
    print(best_route)
    return best_route


# 计算车容利用率
def calculate_capacity_utilization(route):
    total_load = 0
    for i in range(1, len(route) - 1):
        if route[i] > 0:  # 确保索引有效
            total_load += df['需求量'][route[i] - 1]  # 需求量从1开始
    utilization = (total_load / vehicle_capacity) * 100
    return utilization


# 主程序
if __name__ == "__main__":
    best_route = genetic_algorithm()
    print(f"最佳路径: {best_route}")  # 打印最佳路径以供调试

    # 检查路径中是否有无效值
    if -1 in best_route or len(set(best_route)) != len(best_route):
        print("错误: 路径中包含无效值或重复值")
    else:
        fitness_value, total_load, route = fitness(best_route)

        # 检查适应度返回值
        if fitness_value == 0:
            print("错误: 适应度为零，无法计算最小距离")
        else:
            min_distance = 1 / fitness_value
            capacity_utilization = calculate_capacity_utilization(best_route)

            # 输出结果
            print(f"在大约经过 {max_generations} 次迭代后，达到最小路程，实现最优路径。")
            print(f"根据算法结果，可以得出盒马鲜生用了1组厢式货车完成了{len(df)}家门店的配送，")
            print(f"并且使车容量利用率达到了 {capacity_utilization:.2f}%。")
            print(f"具体的配送线路为: {' -> '.join(map(str, route))}")
            print(f"最小路程: {min_distance:.2f} 公里")