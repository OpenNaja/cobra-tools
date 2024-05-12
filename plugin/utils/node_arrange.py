# adapted from https://raw.githubusercontent.com/JuhaW/NodeArrange/master/__init__.py

from collections import OrderedDict
from itertools import repeat

import bpy
from bpy.types import NodeFrame, ShaderNodeTexImage, ShaderNodeRGB


class values():
    x_last = 0
    margin_x = 300
    mat_name = ""
    margin_y = 100


def get_prepared_ui_area(context):
    # Skip if Shader Editor exists
    for area in context.screen.areas:
        if area is None:
            continue

        if area.ui_type == 'ShaderNodeTree':
            return {'area': area, 'old_ui_type': area.ui_type}

    # Change area.ui_type to Shader Editor otherwise
    # Loop as node_columns safety if the current area is None
    for area in context.screen.areas:
        if area is None:
            continue

        area_data = {'area': area, 'old_ui_type': area.ui_type}
        area.ui_type = 'ShaderNodeTree'
        return area_data

    # unlikely but present for code safety
    return {'area': None, 'old_ui_type': None}


def nodes_iterate(b_mat, tree, nodeoutput):
    node_columns = [[nodeoutput, ], ]
    level = 0
    while node_columns[level]:
        node_columns.append([])
        # print ("level:",level)
        for node in node_columns[level]:
            # print ("while: level:", level)
            for input_node in get_input_nodes(node):
                node_columns[level + 1].append(input_node)
        level += 1
    # delete last empty list
    del node_columns[level]
    level -= 1

    # remove duplicate nodes at the same level, first wins
    for x, nodes in enumerate(node_columns):
        node_columns[x] = list(OrderedDict(zip(node_columns[x], repeat(None))))

    # remove duplicate nodes in all levels, last wins
    for col_1 in range(level, 1, -1):
        # print ("col_1:",col_1, node_columns[col_1])
        for node_1 in node_columns[col_1]:
            # print ("node_1:",node_1)
            for col_2 in range(col_1 - 1, 0, -1):
                for node_2 in node_columns[col_2]:
                    if node_1 == node_2:
                        # print ("Duplicate node found:", node_1)
                        # print ("Delete node:", node_2)
                        node_columns[col_2].remove(node_2)
                        break

    # redraw to get the node dimensions
    tree.nodes.update()
    prev_mat = bpy.context.object.active_material
    bpy.context.object.active_material = b_mat
    area_data = get_prepared_ui_area(bpy.context)
    # Redraw nodes in the node tree
    bpy.ops.wm.redraw_timer(type='DRAW_WIN', iterations=1)
    # Restore active area.ui_type
    area = area_data['area']
    old_area_ui_type = area_data['old_ui_type']
    if area is not None and area.ui_type != old_area_ui_type:
        area.ui_type = old_area_ui_type
    bpy.context.object.active_material = prev_mat

    # put child nodes without outputs at the bottom of their frame
    frames = {frame: [] for frame in tree.nodes if isinstance(frame, NodeFrame)}
    for node in tree.nodes:
        if isinstance(node, (ShaderNodeRGB, ShaderNodeTexImage)):
            if not has_outputs(node):
                children = frames.get(node.parent, None)
                if children is not None:
                    children.append(node)

    values.x_last = 0
    for level, nodes in enumerate(node_columns):
        # include any stray child nodes after the last used node of a frame
        temp_nodes = []
        for node in reversed(nodes):
            frame_children = frames.pop(node.parent, None)
            if frame_children is not None:
                temp_nodes.extend(frame_children)
            temp_nodes.append(node)
        nodes_arrange(tree, temp_nodes, level)


def has_outputs(node, socket_id=""):
    for node_socket in node.outputs:
        if node_socket.is_linked:
            return True


def get_input_nodes(node, socket_id=""):
    for node_socket in node.inputs:
        if node_socket.is_linked:
            # skip nodes that don't fit
            if socket_id and socket_id not in node_socket.name:
                continue
            for node_link in node_socket.links:
                yield node_link.from_node


def nodes_arrange(tree, nodes, level):
    print(level, nodes)
    # node x positions
    widthmax = max([x.dimensions.x for x in nodes])
    xpos = values.x_last - (widthmax + values.margin_x) if level != 0 else 0
    # print ("nodes, xpos", nodes,xpos)
    values.x_last = xpos

    # node y positions
    y = 0
    for node in nodes:
        height = node.dimensions.y
        y += height + values.margin_y
        node.location.y = y
        node.location.x = xpos
        # if node.hide:
        # 	height = node.dimensions.y
        # else:
        # 	height = node.dimensions.y
        print(height, node.label)

    print(level, y)
    for node in nodes:
        node.location.y -= (y / 2)

