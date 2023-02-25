import nrrd
import numpy as np
from skimage import measure
from mayavi import mlab
from collections import defaultdict
from queue import Queue

def compute_adj_list(fac):
    adj_list = defaultdict(list)
    for face in fac:
        for i in range(len(face)):
            node1 = face[i]
            node2 = face[(i+1)%len(face)]
            if node2 not in adj_list[node1]:
                adj_list[node1].append(node2)
            if node1 not in adj_list[node2]:
                adj_list[node2].append(node1)
    for key, value in adj_list.items():
        adj_list[key] = value
    return dict(adj_list)

def get_components(dictionary):
    components = []
    Mark = set()
    for startnode in dictionary.keys():
        if startnode in Mark:
            continue
        component = []
        queue = []
        queue.append(startnode)
        while queue:
            n = queue.pop(0)
            Mark.add(n)
            component.append(n)
            for mi in dictionary[n]:
                if mi not in Mark:
                    queue.append(mi)
                    Mark.add(mi)
        components.append(component)
    return components

class surface:
    def __init__(self):
        self.verts = None
        self.faces = None
        self.normals = None
        self.color = [1., 0., 0.]
        self.mlab_handle = None
        self.opacity = 1

    def createSurfaceFromVolume(self, img, voxsz, isolevel):
        self.verts, self.faces, self.normals, values = measure.marching_cubes(img, isolevel, spacing=voxsz)

    def display(self, axes=False):
        # mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
        if self.mlab_handle is None:
            self.mlab_handle = mlab.triangular_mesh(self.verts[:, 0], self.verts[:, 1], self.verts[:, 2], self.faces,
                                                    color=(self.color[0], self.color[1], self.color[2]),
                                                    opacity=self.opacity)

        else:
            self.mlab_handle.mlab_source.set(x=self.verts[:, 0], y=self.verts[:, 1], z=self.verts[:, 2])

        if axes == True:
            mlab.axes(self.mlab_handle)

        mlab.show()

    def bfs(graph, start):
        visited = set()
        queue = Queue()
        queue.put(start)
        while not queue.empty():
            vertex = queue.get()
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    queue.put(neighbor)
        return visited

    def connectedComponents(self):
        print(np.shape(self.faces))
        print(np.shape(self.verts))
        edges = compute_adj_list(self.faces)
        components = get_components(edges)
        return components











