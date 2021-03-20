class Octree:
    """
    | Tree containing inserted atoms and their positions.
    | Commonly used to get atoms near other atoms.
    """
    def __init__(self, world_size=5000, max_per_node=8):
        self._max_objects = max_per_node
        self._world_size = world_size
        #internally we use half sizes because they are faster.
        self._root = Octree._OctNode((0,0,0), world_size/2)
        self._knowns = {}

    def remove(self, data):
        """
        | Remove a data node from the Octree

        :param data: The data to remove from the Octree
        :type data: :class:`Object`
        """
        if data in self._knowns:
            node = self._knowns[data]
            del self._knowns[data]
            if (data in node.here):
                node.here.remove(data)
            return True
        else:
            return False

    def move(self, data, new_position):
        """
        | Move a data node in the octree

        :param data: Data node in the octree to move
        :param new_position: New position of the data node
        :type data: :class:`Object`
        :type new_positon: :class:`~nanome.util.Vector3`
        """
        self.remove(data)
        self.add(data, new_position)

    def add(self, data, position):
        """
        | Add a data node to the octree

        :param data: Data node to add to the octree
        :param position: Position of this data node
        :type data: :class:`Object`
        :type positon: :class:`~nanome.util.Vector3`
        """
        try:
            entry = Octree._Entry(data, position)
            self._root.add(self, entry)
        except RecursionError:
            from . import Logs
            Logs.error("Maximum recursion depth reached. Make sure you don't add more than the max_objects number of objects with the exact same position.")
            raise
    
    def get_near(self, pos, radius, max_result_nb = None):
        """
        | Get the nodes within the octree that are near a specific position

        :param pos: Position to check near
        :param radius: Get nodes within this radius of the position
        :param max_result_nb: Number of results to get
        :type pos: :class:`~nanome.util.Vector3`
        :type radius: float
        :type max_result_nb: int
        """
        near_objs = []
        self.get_near_append(pos, radius, near_objs, max_result_nb)
        return near_objs

    def get_near_append(self, pos, radius, out_list, max_result_nb = None):
        """
        | Helper function to append specific object if it is near
        """
        self._root.near(pos, radius*radius, out_list, max_result_nb)
        return out_list

    def print_out(self):
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
            #overestimation to prevent misses.
            self.sqrRadius = h_size*h_size*3
            self.branches = None
            self.here = []

        def add(self, tree, entry):
            if self.branches == None and len(self.here) < tree._max_objects:
                self._add_here(tree, entry)
                return
            if self.branches == None:
                self._subdivide(tree)
            self.branches[self._findBranch(entry.pos)].add(tree, entry)
            
        def _add_here(self, tree, entry):
            self.here.append(entry)
            tree._knowns[entry.data] = self

        def _subdivide(self, tree):
            q_size = self.h_size/2
            p = self.position #parent position
            o = q_size #offset
            OctNode = Octree._OctNode
            self.branches = [OctNode((p[0]-o,p[1]-o,p[2]-o), q_size),#---
                             OctNode((p[0]+o,p[1]-o,p[2]-o), q_size),#+--
                             OctNode((p[0]-o,p[1]+o,p[2]-o), q_size),#-+-
                             OctNode((p[0]+o,p[1]+o,p[2]-o), q_size),#++-
                             OctNode((p[0]-o,p[1]-o,p[2]+o), q_size),#--+
                             OctNode((p[0]+o,p[1]-o,p[2]+o), q_size),#+-+
                             OctNode((p[0]-o,p[1]+o,p[2]+o), q_size),#-++
                             OctNode((p[0]+o,p[1]+o,p[2]+o), q_size)]#+++
            #move children down
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
            if (len(self.here) > 0 or self.branches != None):
                print(depth*' ' + "Depth:", str(depth), "center:", str(self.position), "size:", str(self.h_size), "entries:", str(len(self.here)))
                if( self.branches != None):
                    for branch in self.branches:
                        branch.print_out(depth+1)

        def near(self, pos, radiusSqr, near_objs, max_result_nb = None):
            #sqr comparison to avoid root
            if (Octree._OctNode._sqr_distance(pos, self.position) <= self.sqrRadius + radiusSqr):
                if (self.branches != None):
                    for branch in self.branches:
                        max_result_nb = branch.near(pos, radiusSqr, near_objs, max_result_nb)
                        # if a child branch got the max nb of result, return
                        if max_result_nb != None and max_result_nb <= 0:
                            return max_result_nb
                else:
                    for entry in self.here:
                        if (Octree._OctNode._sqr_distance(pos, entry.pos) < radiusSqr):
                            near_objs.append(entry.data)
                            # if this branch got the max nb of result, return
                            if max_result_nb != None:
                                max_result_nb -= 1
                                if max_result_nb <= 0:
                                    return max_result_nb

                return max_result_nb


        @staticmethod
        def _sqr_distance(pos1, pos2):
            x = pos1[0]-pos2[0]
            y = pos1[1]-pos2[1]
            z = pos1[2]-pos2[2]
            return x*x+y*y+z*z