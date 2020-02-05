from nanome._internal._ui import _Menu

def _receive_menu(network, arg, request_id):
        #unpacks the arg tuple.
        temp_menu = arg[0]
        temp_nodes = arg[1]
        temp_contents = arg[2]

        plugin_menu = network._plugin.menu # dead API
        plugin_menu._copy_data(temp_menu)
        root_id = temp_menu._root_id
        
        live_nodes = plugin_menu._get_all_nodes()
        live_contents = plugin_menu._get_all_content()
        #creates map of live content
        content_dict = {}
        for content in live_contents:
            content_dict[content._id] = content
        #creates map of live nodes
        node_dict = {}
        for node in live_nodes:
            node_dict[node._id] = node
        #updates existing content with data.
        #adds any new content.
        for content in temp_contents:
            if content._content_id in content_dict:
                l_content = content_dict[content._content_id]
                l_content._copy_values_deep(content)
            else:
                content_dict[content._content_id] = content
        #updates existing nodes with data.
        #adds any new nodes.
        for node in temp_nodes:
            if node._id in node_dict:
                l_node = node_dict[node._id]
                l_node.copy_values_shallow(node)
            else:
                node_dict[node._id] = node
        #reconnects all the nodes and contents using ids.
        for node in temp_nodes:
            l_node = node_dict[node._id]
            l_node._clear_children()
            for child_id in node._child_ids:
                l_node._add_child(node_dict[child_id])
            del node._child_ids
            if (node._content_id == None):
                l_node._set_content(None)
            else:
                l_node._set_content(content_dict[node._content_id])
            del node._content_id
        #corrects the root.
        plugin_menu.root = node_dict[root_id]
        network._call(request_id, plugin_menu)