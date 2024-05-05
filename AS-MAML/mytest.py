import pickle
import os
import json
import random
import networkx as nx


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
    dir_ = './data/Apache-par'
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    entity_embeddings_path = os.path.join('./data/' + datasetname, "raw/entity_embeddings.pickle")
    node_attribures = load_pickle(entity_embeddings_path)
    node_attribures_path = os.path.join(dir_, datasetname + '_node_attributes.pickle')
    dump_pickle(node_attribures_path, node_attribures.tolist())

    graph_list_path = os.path.join('./data/' + datasetname, "raw/graph_list.pickle")
    graph_list = load_pickle(graph_list_path)
    graph_num = len(graph_list)
    equal_dict_path = os.path.join('./data/' + datasetname, "raw/equal_dict.json")
    equal_dict = load_json(equal_dict_path)
    graph2label = {}
    train_part = []
    val_part = []
    test_part = []
    for key in equal_dict.keys():
        graphs = equal_dict[key]
        split_res = random_split(graphs)
        train_part.extend(split_res[0])
        val_part.extend(split_res[1])
        test_part.extend(split_res[2])

    # train_set.pickle
    train_set = {'label2graphs': {}}
    for i in range(len(equal_dict.keys())):
        g_list = equal_dict[list(equal_dict.keys())[i]]
        for g in g_list:
            graph2label[g] = i
        train_set['label2graphs'][i] = []
    for g in train_part:
        train_set['label2graphs'][graph2label[g]].append(g)
    train_set['graph2nodes'] = {}
    train_set['graph2edges'] = {}
    for i in train_part:
        train_set['graph2nodes'][i] = list(graph_list[i].nodes())
        edges = list(set(graph_list[i].edges()))
        train_set['graph2edges'][i] = [list(edge) for edge in edges]
    train_set_path = os.path.join(dir_, datasetname + '_train_set.pickle')
    dump_pickle(train_set_path, train_set)

    # val_set.pickle
    val_set = {'label2graphs': {}}
    for i in range(len(equal_dict.keys())):
        val_set['label2graphs'][i] = []
    for g in val_part:
        val_set['label2graphs'][graph2label[g]].append(g)
    val_set['graph2nodes'] = {}
    val_set['graph2edges'] = {}
    for i in val_part:
        val_set['graph2nodes'][i] = list(graph_list[i].nodes())
        edges = list(set(graph_list[i].edges()))
        val_set['graph2edges'][i] = [list(edge) for edge in edges]
    val_set_path = os.path.join(dir_, datasetname + '_val_set.pickle')
    dump_pickle(val_set_path, val_set)

    # test_set.pickle
    test_set = {'label2graphs': {}}
    for i in range(len(equal_dict.keys())):
        test_set['label2graphs'][i] = []
    for g in test_part:
        test_set['label2graphs'][graph2label[g]].append(g)
    test_set['graph2nodes'] = {}
    test_set['graph2edges'] = {}
    for i in test_part:
        test_set['graph2nodes'][i] = list(graph_list[i].nodes())
        edges = list(set(graph_list[i].edges()))
        test_set['graph2edges'][i] = [list(edge) for edge in edges]
    test_set_path = os.path.join(dir_, datasetname + '_test_set.pickle')
    dump_pickle(test_set_path, test_set)

    return node_attribures


# node_attribures_path=os.path.join('data/Apache-par/raw', "graph_list.pickle")
node_attribures_path=os.path.join('data/TRIANGLES',"TRIANGLES_train_set.pickle")


data = load_pickle(node_attribures_path)
print(data)
preprocess('Apache-par')

# node_attributes  [[] []]
# train_set.pickle
# ['label2graphs', 'graph2nodes', 'graph2edges']
