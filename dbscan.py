# dbscan.py
'''
Recreating the DB scan algorithm.
'''
class Cluster:
    '''
    cluster class that will store the core and non core values of each cluster
    '''
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
    '''
    model that runs the DBScan algorithm on a set of data

    it will determine the clusters that are present in a data set or if a point is noise
    '''
    def __init__(self, max_distance, min_cluster_size):
        self.max_distance = max_distance
        self.min_cluster_size = min_cluster_size
        self.cluster_list = []
        self.noise = []

     # helper function to get all points within the desired distance
    def get_neighbors(self, current_point, points):
        return [each for each in points if distance(current_point, each) <= self.max_distance]

    def cluster_creation(self, neighbors, points, cluster):
        '''
        recursive function that will take a cluster and add all of its core and non core points
        '''
        # base case
        if len(neighbors) == 0:
            return cluster
        current_point = neighbors[0]
        neighbors.remove(current_point)
        points.remove(current_point)
        # getting points within range
        current_neighbors = self.get_neighbors(current_point, points)
        # adding core points
        if len(current_neighbors) >= self.min_cluster_size - 1:
            cluster.add_to_core(current_point)
            # points within range that have not previously been found should be added to the list of points to check
            for each in current_neighbors:
                if each not in neighbors:
                    neighbors.append(each)
        # adding non core points
        else:
            cluster.add_to_non_core(current_point)
        # checking to see if points that were previously thought of as noise are in fact non core points
        for each in self.noise:
            if distance(current_point, each) <= self.max_distance:
                self.noise.remove(each)
                cluster.add_to_non_core(each)
        return self.cluster_creation(neighbors, points, cluster)

    def fit(self, points, current_cluster=1):
        '''
        recursive function that will process a data set and determine any clusters or noise
        '''
        # base case
        if len(points) == 0:
            return
        current_point = points[0]
        points.remove(current_point)
        # getting points within range
        neighborhood = self.get_neighbors(current_point, points)
        # if the point has at least the minimum amount of neighbors create a cluster
        if len(neighborhood) >= self.min_cluster_size - 1:
            new_cluster = Cluster(current_cluster)
            new_cluster.add_to_core(current_point)
            # using helper function to add all of the core and non core points to the cluster
            self.cluster_creation(neighborhood, points, new_cluster)
            current_cluster += 1
            self.cluster_list.append(new_cluster)
        # if a point does not have at least the minimum number of neighbors add it to noise
        else:
            self.noise.append(current_point)        
        self.fit(points, current_cluster=current_cluster)

    def predict(self, point):
        '''
        will return a 0 if noise, or it will return which cluster number a point is a member of        
        '''
        for cluster in self.cluster_list:
            if point in cluster.get_all_points():
                return cluster.name
        if point in self.noise:
            return 0