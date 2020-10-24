# dbscan.py
'''
Recreating the DB scan algorithm.

TO DO:
- refactor and comment
'''
class Cluster:
    def __init__(self, cluster_name):
        self.core_points = []
        self.non_core_points = []
        self.name = cluster_name
        
    def add_to_core(self, point):
        self.core_points.append(point)

    def add_to_non_core(self, point):
        self.non_core_points.append(point)

    def get_core_points(self):
        return self.core_points

    def get_non_core_points(self):
        return self.non_core_points

    def get_all_points(self):
        return self.core_points + self.non_core_points

# helper function to get distance between two points
def distance(point_a, point_b):
    return ((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)**(0.5)

class DBScan:
    def __init__(self, max_distance, min_cluster_size):
        self.max_distance = max_distance
        self.min_cluster_size = min_cluster_size
        self.cluster_list = []
        self.noise = []

    def get_neighbors(self, current_point, points):
        return [each for each in points if distance(current_point, each) <= self.max_distance]

    def cluster_creation(self, neighbors, points, cluster):
        if len(neighbors) == 0:
            return cluster
        current_point = neighbors[0]
        neighbors.remove(current_point)
        points.remove(current_point)
        current_neighbors = self.get_neighbors(current_point, points)
        if len(current_neighbors) >= self.min_cluster_size - 1:
            cluster.add_to_core(current_point)
            for each in current_neighbors:
                if each not in neighbors:
                    neighbors.append(each)
        else:
            cluster.add_to_non_core(current_point)
        for each in self.noise:
            if distance(current_point, each) <= self.max_distance:
                self.noise.remove(each)
                cluster.add_to_non_core(each)
        return self.cluster_creation(neighbors, points, cluster)

    def fit(self, points, current_cluster=1):
        if len(points) == 0:
            return
        current_point = points[0]
        points.remove(current_point)
        neighborhood = self.get_neighbors(current_point, points)
        if len(neighborhood) >= self.min_cluster_size - 1:
            new_cluster = Cluster(current_cluster)
            new_cluster.add_to_core(current_point)
            self.cluster_creation(neighborhood, points, new_cluster)
            current_cluster += 1
            self.cluster_list.append(new_cluster)
        else:
            self.noise.append(current_point)        
        self.fit(points, current_cluster=current_cluster)

    def predict(self, point):
        for cluster in self.cluster_list:
            if point in cluster.get_all_points():
                return cluster.name
        for cluster in self.cluster_list:
            for each in cluster.get_core_points():
                if distance(point, each) <= self.max_distance:
                    return cluster.name
                else:
                    return 0