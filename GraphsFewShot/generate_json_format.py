import pickle
import os
import json
import random


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
        return data

def dump_pickle(file_name, data):
    with open(file_name, "wb") as f:
        pickle.dump(data, f)


def load_json(file_name):
    with open(file_name, 'rb') as f:
        data = json.load(f)
        return data


def random_split(lst, ratios=None, seed=None):
    """
    随机划分列表元素
    参数：
    - lst: 待划分的列表
    - ratios: 划分比例列表，如[6, 2, 2]
    - seed: 随机种子
    返回：
    - 划分后的列表组成的列表
    """
    if ratios is None:
        ratios = [0.6, 0.2, 0.2]
    if seed is not None:
        random.seed(seed)

    assert sum(ratios) == 1, "划分比例之和应为1"

    # 随机打乱列表
    random.shuffle(lst)

    # 计算每个部分的长度
    total_len = len(lst)
    lengths = [int(total_len * ratio) for ratio in ratios]
    # 划分列表
    result = [lst[sum(lengths[:i]):sum(lengths[:i+1])] for i in range(len(lengths))]

    return result


def preprocess(datasetname):
    # 根据图的id找到label
    graph2label = {}
    equal_dict_path = os.path.join('./datasets/' + datasetname, "raw/equal_dict.json")
    equal_dict = load_json(equal_dict_path)
    for i in range(len(equal_dict.keys())):
        g_list = equal_dict[list(equal_dict.keys())[i]]
        for g in g_list:
            graph2label[g] = i

    # 生成json_format
    graph_list_path = os.path.join('./datasets/' + datasetname, "raw/graph_list.pickle")
    graph_list = load_pickle(graph_list_path)
    for i in range(len(graph_list)):
        graph = graph_list[i]
        node2id = {}
        for node in graph.nodes():
            if node not in node2id.keys():
                node2id[node] = len(node2id)
        graph_info = {'edges': [], 'labels': {}, 'target': -1}
        edges = list(set(graph.edges()))
        edges = [list(edge) for edge in edges]
        for edge in edges:
            edge[0] = node2id[edge[0]]
            edge[1] = node2id[edge[1]]
        graph_info['edges'] = edges
        for node in graph.nodes():
            graph_info['labels'][str(node2id[node])] = str(node2id[node])
        graph_info['target'] = graph2label[i]
        # 指定要保存的文件路径
        dir_ = os.path.join('./datasets/' + datasetname, 'json_format')
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        file_path = os.path.join(dir_, f"{i + 1}.json")
        # 将字典存储为 JSON 文件
        with open(file_path, "w") as json_file:
            json.dump(graph_info, json_file)
    return None



preprocess('Apache-par')

# node_attributes  [[] []]
# train_set.pickle
# ['label2graphs', 'graph2nodes', 'graph2edges']
