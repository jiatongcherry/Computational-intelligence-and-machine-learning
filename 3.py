import pandas as pd
import numpy as np

# """
# Part1
# Directly run this code
# 1.load csv file
# 2.Clean the data, convert numinal and ordinal values into nunmerical type
# 3.Replace 'XXXXXXX' with -1
# 4.attribute feature report
# 5.Store clean data in a new file newdata.csv
# """
#
#
# data = pd.read_csv('analysis_data.csv', header=None)
#
# data.replace('XXXXXXX', np.nan, inplace=True)
# missing_values = data.isnull().sum()
# data.replace(np.nan, -1, inplace=True)
#
#
# season_mapping = {'spring': 0, 'summer': 1, 'autumn': 2, 'winter': 3}
# data[0] = data[0].map(season_mapping)
#
# size_mapping1 = {'small_': 0, 'medium': 1, 'large_': 2}
# data[1] = data[1].map(size_mapping1)
#
# size_mapping2 = {'low___': 0, 'medium': 1, 'high__': 2}
# data[2] = data[2].map(size_mapping2)
#
# data = data.apply(pd.to_numeric, errors='coerce')
#
# #correct merged values
# def correct_merged_values(row):
#     #print(len(row))
#     for index in range(len(row)):
#         #print(index)
#         if isinstance(row[index], str) and row[index].count('.') > 1:
#             #print(1)
#             parts = row[index].split('.')
#             if len(parts) >= 3:
#                 #first value (up to 5 digits after the first decimal)
#                 first_number = f"{parts[0]}.{parts[1][:5]}"
#                 #second value (up to 3 digits before the second decimal)
#                 second_number = f"{parts[2][:3]}.{''.join(parts[3:])}" if len(parts) > 3 else parts[2]
#                 print(first_number, second_number)
#                 row[index] = first_number
#                 row.insert(index + 1, second_number)
#                 break
#     return row
#
# data = data.apply(correct_merged_values, axis=0)
#
# data.to_csv('newdata.csv')
#
# min_values = data.min().tolist()
# max_values = data.max().tolist()
# missing_values = missing_values.tolist()
#
# print("Minimum values per attribute:", min_values)
# print("Maximum values per attribute:", max_values)
# print("Missing", missing_values)


"""
Part2
Directly run this code
1.define compute_similarity function, three different conditions
2.Find the pair with maximum and minimum similarity
3.output sim&dif of object in question
"""
data = pd.read_csv('newdata.csv', header=None)

def compute_similarity(obj1, obj2):
    similarities = []
    valid_indices = []

    for i in range(len(obj1)):
        # 只在比较时检查 -1
        if pd.notna(obj1[i]) and pd.notna(obj2[i]):
            if obj1[i] != -1 and obj2[i] != -1:
                valid_indices.append(i)
                if i == 0:  # Nominal attribute
                    similarity = 1 if obj1[i] == obj2[i] else 0
                elif i in [1, 2]:  # Ordinal attributes
                    similarity = 1 - (abs(obj1[i] - obj2[i]) / 2)
                else:
                    min_value = data[i].min()
                    max_value = data[i].max()
                    max_dissimilarity = max_value - min_value
                    dissimilarity = abs(obj1[i] - obj2[i])

                    if max_dissimilarity != 0:
                        similarity = 1 - (dissimilarity / max_dissimilarity)
                    else:
                        similarity = 1  # identical

                similarities.append(similarity)

    return np.mean(similarities) if similarities else 0


max_similarity = -1
min_similarity = float('inf')
max_pair = None
min_pair = None

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        sim = compute_similarity(data.iloc[i], data.iloc[j])
        if sim > max_similarity:
            max_similarity = sim
            max_pair = (i, j)
        if sim < min_similarity:
            min_similarity = sim
            min_pair = (i, j)

# Query object
query_object = [3, 2, 1, 8.10000, 7.50000, 140.00000, 1.00000, 60.00000, 100.00000, 140.00000, 31.00000, 1.00000, 10.00000, 3.00000, 1.00000, 0.00000, 0.00000, 5.00000]
query_object = pd.Series(query_object)

highest_similarity_to_query = -1
most_similar_object_index = -1

for i in range(len(data)):
    sim = compute_similarity(query_object, data.iloc[i])
    if sim > highest_similarity_to_query:
        highest_similarity_to_query = sim
        most_similar_object_index = i

print(f"Maximum similarity: {max_similarity:.2f}; pair with maximum similarity: [{max_pair[0]}, {max_pair[1]}]")
print(f"Object {max_pair[0]} = {data.iloc[max_pair[0]].values}")
print(f"Object {max_pair[1]} = {data.iloc[max_pair[1]].values}")

print(f"Minimum similarity: {min_similarity:.2f}; pair with minimum similarity: [{min_pair[0]}, {min_pair[1]}]")
print(f"Object {min_pair[0]} = {data.iloc[min_pair[0]].values}")
print(f"Object {min_pair[1]} = {data.iloc[min_pair[1]].values}")

print(f"Highest similarity to input object: {highest_similarity_to_query:.2f}; object with highest similarity: {most_similar_object_index}")
print(f"Object {most_similar_object_index} = {data.iloc[most_similar_object_index].values}")


"""
Part3
Directly run this code
1.define compute_euclidean_distance function
2.min_max_normalization function is used to normalize the values of an attribute to a specific range, typically between 0 and 1
3.output distance of object pairs
"""
data = pd.read_csv('newdata.csv', header=None)

def min_max_normalization(column):
    min_val = column.min()
    max_val = column.max()
    return (column - min_val) / (max_val - min_val) if max_val != min_val else column


def compute_euclidean_distance(obj1, obj2):
    interval_values1 = obj1[3:]
    interval_values2 = obj2[3:]

    # 创建一个掩码以检查有效值
    valid_mask = (interval_values1 != -1) & (interval_values2 != -1)

    # 检查是否有有效的索引
    if not valid_mask.any():
        return np.nan

    # 仅过滤有效值
    filtered_values1 = interval_values1[valid_mask]
    filtered_values2 = interval_values2[valid_mask]

    # 归一化值
    normalized1 = min_max_normalization(filtered_values1)
    normalized2 = min_max_normalization(filtered_values2)

    # 计算平方差并求和
    squared_diff = (normalized1 - normalized2) ** 2
    distance = np.sqrt(squared_diff.sum())

    return distance


# Find the pairs with the largest and smallest distances
max_distance = -1
min_distance = float('inf')
max_pair = None
min_pair = None

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        dist = compute_euclidean_distance(data.iloc[i], data.iloc[j])
        if dist is not np.nan:
            if dist > max_distance:
                max_distance = dist
                max_pair = (i, j)
            if dist < min_distance:
                min_distance = dist
                min_pair = (i, j)

# Query object
query_object = [3, 2, 2, 8.10000, 7.50000, 140.00000, 1.00000, 60.00000, 100.00000, 140.00000, 31.00000, 1.00000,
                10.00000, 3.00000, 1.00000, 0.00000, 0.00000, 5.00000]
query_object = pd.Series(query_object)

# Calculate the distance to the query object
smallest_distance_to_query = float('inf')
most_similar_object_index = -1

for i in range(len(data)):
    dist = compute_euclidean_distance(query_object, data.iloc[i])
    if dist is not np.nan and dist < smallest_distance_to_query:
        smallest_distance_to_query = dist
        most_similar_object_index = i


print(f"Maximum distance: {max_distance:.2f}; pair with maximum distance: [{max_pair[0]}, {max_pair[1]}]")
print(f"Object {max_pair[0]} = {data.iloc[max_pair[0]].values}")
print(f"Object {max_pair[1]} = {data.iloc[max_pair[1]].values}")

print(f"Minimum distance: {min_distance:.2f}; pair with minimum distance: [{min_pair[0]}, {min_pair[1]}]")
print(f"Object {min_pair[0]} = {data.iloc[min_pair[0]].values}")
print(f"Object {min_pair[1]} = {data.iloc[min_pair[1]].values}")

print(
    f"Smallest distance to input object: {smallest_distance_to_query:.2f}; object with smallest distance: {most_similar_object_index}")
print(f"Object {most_similar_object_index} = {data.iloc[most_similar_object_index].values}")
