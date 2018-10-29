import datetime
import json
import statics


# CREATE BLANK GRAPH
def create_new_graph():
    return {
        'nodes': [],
        'edges': []
    }


# WRITE GRAPH
def write_graph(graph, final=False):
    if final:
        name = str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + '_graph.json'
    else:
        name = 'graph.json'
    with open(statics.DATA_FOLDER + name, 'w') as fp:
        json.dump(graph, fp)


# READ GRAPH
def read_graph(name=statics.DEFAULT_DATAFILE_NAME):
    with open(statics.DATA_FOLDER + name, 'r') as fp:
        data = json.load(fp)
    return data


# ADD NODE
def add_node(name: str, description: str, subs: int, target_graph=None):
    if target_graph is None:
        graph = read_graph()
    else:
        graph = target_graph

    # node does not exist
    if not any(d['name'] == name for d in graph['nodes']):
        graph['nodes'].append(
            {'name': name,
             'description': description,
             'subs': subs}
        )
        write_graph(graph)


# ADD EDGE BETWEEN NODES
def add_edge(source: str, target: str, target_graph=None):
    if target_graph is None:
        graph = read_graph()
    else:
        graph = target_graph

    # edge does not exist
    if any(d['source'] == source for d in graph['edges']) and any(d['target'] == target for d in graph['edges']):
        # find and increase value
        try:
            next((item for item in graph['edges'] if item['source'] == source and item['target'] == target), None)['value'] += 1
        except:
            pass
    else:
        graph['edges'].append(
            {
                'source': source,
                'target': target,
                'value': 0
            }
        )

    write_graph(graph)


# CONNECT
def connect(source: str, target: str, target_graph=None):
    if target_graph is None:
        graph = read_graph()
    else:
        graph = target_graph

    add_node(source, None, None)
    add_node(target, None, None)
    add_edge(source, target)


# TEST
def test():
    graph = create_new_graph()
    write_graph(graph)
    connect('dickmove', 'counterstrike')
    print(read_graph()['edges'])


if __name__ == '__main__':
    test()

'''
# READ VISITED
def read_visited():
    with open(statics.DATA_FOLDER + 'visited.json', 'r') as fp:
        data = json.load(fp)
    return data


# WRITE VISITED
def add_to_visited(add: str, final=False):
    visited = read_visited()

    if add not in visited:
        visited.append(add)
        if final:
            name = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '_visited.json'
        else:
            name = 'visited.json'
        with open(statics.DATA_FOLDER + name, 'w') as fp:
            json.dump(visited, fp)
        return True
    return False
'''
