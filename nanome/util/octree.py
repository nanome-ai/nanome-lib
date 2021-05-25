class Octree:
    """
    | Tree containing inserted objects and their positions.
    | Commonly used to get neighboring objects.
    """

    def __init__(self, world_size=5000, max_per_node=8):
        self._max_objects = max_per_node
        self._world_size = world_size
        # internally we use half sizes because they are faster.
        self._root = Octree._OctNode((0, 0, 0), world_size / 2)
        self._knowns = {}

    def remove(self, data):
        """
        | Remove a data node from the Octree.

        :param data: The data to remove from the Octree
        :type data: :class:`object`
        """
        if data in self._knowns:
            node = self._knowns[data]
            del self._knowns[data]
            if data in node.here:
                node.here.remove(data)
            return True
        else:
            return False

    def move(self, data, new_position):
        """
        | Move a data node in the octree.

        :param data: Data node in the octree to move
        :type data: :class:`object`
        :param new_position: New position for the data node
        :type new_positon: :class:`~nanome.util.Vector3`
        """
        self.remove(data)
        self.add(data, new_position)

    def add(self, data, position):
        """
        | Add a data node to the octree.

        :param data: Data node to add to the octree
        :type data: :class:`object`
        :param position: Position of this data node
        :type positon: :class:`~nanome.util.Vector3`
        """
        try:
            entry = Octree._Entry(data, position)
            self._root.add(self, entry)
        except RecursionError:
            from . import Logs
            Logs.error("Maximum recursion depth reached. Make sure you don't add more than the max_objects number of objects with the exact same position.")
            raise

    def get_near(self, pos, radius, max_result_nb=None):
        """
        | Get nodes within the octree neighboring a position.

        :param pos: Position to check around
        :type pos: :class:`~nanome.util.Vector3`
        :param radius: Radius around position where nodes within will be returned
        :type radius: :class:`float`
        :param max_result_nb: Maximum number of neighbors to return
        :type max_result_nb: :class:`int`
        """
        near_objs = []
        self.get_near_append(pos, radius, near_objs, max_result_nb)
        return near_objs

    def get_near_append(self, pos, radius, out_list, max_result_nb=None):
        """
        | Functions like get_near, but with an externally controlled list.

        :param pos: Position to check around
        :type pos: :class:`~nanome.util.Vector3`
        :param radius: Radius around position where nodes within will be returned
        :type radius: :class:`float`
        :param out_list: Parent-scoped list to append search neighbors to
        :type out_list: :class:`list`
        :param max_result_nb: Maximum number of neighbors to return
        :type max_result_nb: :class:`int`
        """
        self._root.near(pos, radius * radius, out_list, max_result_nb)
        return out_list

    def print_out(self):
        """
        | Prints out information about the octree.
        """
        print("knowns:", len(self._knowns))
        print("Root:")
        self._root.print_out(0)

    class _Entry:
        def __init__(self, data, pos):
            self.data = data
            self.pos = pos

    class _OctNode:
        def __init__(self, position, h_size):
            self.position = position
            self.h_size = h_size
            # overestimation to prevent misses.
            self.sqrRadius = h_size * h_size * 3
            self.branches = None
            self.here = []

        def add(self, tree, entry):
            if self.branches is None and len(self.here) < tree._max_objects:
                self._add_here(tree, entry)
                return
            if self.branches is None:
                self._subdivide(tree)
            self.branches[self._findBranch(entry.pos)].add(tree, entry)

        def _add_here(self, tree, entry):
            self.here.append(entry)
            tree._knowns[entry.data] = self

        def _subdivide(self, tree):
            q_size = self.h_size / 2
            p = self.position  # parent position
            o = q_size  # offset
            OctNode = Octree._OctNode
            self.branches = [OctNode((p[0] - o, p[1] - o, p[2] - o), q_size),  # ---
                             OctNode((p[0] + o, p[1] - o, p[2] - o), q_size),  # +--
                             OctNode((p[0] - o, p[1] + o, p[2] - o), q_size),  # -+-
                             OctNode((p[0] + o, p[1] + o, p[2] - o), q_size),  # ++-
                             OctNode((p[0] - o, p[1] - o, p[2] + o), q_size),  # --+
                             OctNode((p[0] + o, p[1] - o, p[2] + o), q_size),  # +-+
                             OctNode((p[0] - o, p[1] + o, p[2] + o), q_size),  # -++
                             OctNode((p[0] + o, p[1] + o, p[2] + o), q_size)]  # +++
            # move children down
            while(len(self.here) > 0):
                entry = self.here[-1]
                del self.here[-1]
                self.add(tree, entry)

        def _findBranch(self, pointPos):
            vec1 = self.position
            vec2 = pointPos
            result = 0
            for i in range(3):
                result += (vec1[i] <= vec2[i]) << i
            return result

        def print_out(self, depth):
            if len(self.here) > 0 or self.branches is not None:
                print(depth * ' ' + "Depth:", str(depth), "center:", str(self.position), "size:", str(self.h_size), "entries:", str(len(self.here)))
                if self.branches is not None:
                    for branch in self.branches:
                        branch.print_out(depth + 1)

        def near(self, pos, radiusSqr, near_objs, max_result_nb=None):
            # sqr comparison to avoid root
            if Octree._OctNode._sqr_distance(pos, self.position) <= self.sqrRadius + radiusSqr:
                if self.branches is not None:
                    for branch in self.branches:
                        max_result_nb = branch.near(pos, radiusSqr, near_objs, max_result_nb)
                        # if a child branch got the max nb of result, return
                        if max_result_nb is not None and max_result_nb <= 0:
                            return max_result_nb
                else:
                    for entry in self.here:
                        if Octree._OctNode._sqr_distance(pos, entry.pos) < radiusSqr:
                            near_objs.append(entry.data)
                            # if this branch got the max nb of result, return
                            if max_result_nb is not None:
                                max_result_nb -= 1
                                if max_result_nb <= 0:
                                    return max_result_nb

                return max_result_nb

        @staticmethod
        def _sqr_distance(pos1, pos2):
            x = pos1[0] - pos2[0]
            y = pos1[1] - pos2[1]
            z = pos1[2] - pos2[2]
            return x * x + y * y + z * z
