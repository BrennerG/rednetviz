import persistor as db
import statics as STATS


# removes nodes from the graph, that are not linked to any other node
def clean_unconnected_nodes(graph):
    sources = [edge['source'] for edge in graph['edges']]
    targets = [edge['target'] for edge in graph['edges']]
    corrected_nodes = [node for node in graph['nodes'] if node['name'] in sources or node['name'] in targets]
    graph['nodes'] = corrected_nodes
    return graph


# removes edges whose value is 0
def remove_edges(graph, threshold=0):
    corrected = [edge for edge in graph['edges'] if edge['value'] > threshold]
    graph['edges'] = corrected
    return clean_unconnected_nodes(graph)


# remove any self references
def remove_self_references(graph):
    corrected_edges = [edge for edge in graph['edges'] if edge['source'] != edge['target']]
    graph['edges'] = corrected_edges
    return clean_unconnected_nodes(graph)


def rename_for_viz_1(graph):
    id = 0

    # give nodes ids
    for node in graph['nodes']:
        node['id'] = id
        id += 1

    for edge in graph['edges']:
        for node in graph['nodes']:

            # replace node_names in edges with node_ids
            if edge['source'] == node['name']:
                edge['source'] = node['id']
            if edge['target'] == node['name']:
                edge['target'] = node['id']

        # give edges types (value?)
        edge['type'] = edge['value']

    # rename edges to links
    graph['links'] = graph.pop('edges')

    return graph


if __name__ == '__main__':
    FILENAME = 'overnight.json'
    raw = db.read_graph(FILENAME)
    print(len(raw['nodes']), len(raw['edges']))

    # SET THRESHOLD
    THRESHOLD = 1
    new = remove_edges(raw, THRESHOLD)
    new = remove_self_references(new)

    # RENAME STUFFS
    renamed = rename_for_viz_1(new)

    print(len(renamed['nodes']), len(renamed['links']))
    db.write_graph(new, True)
