import numpy as np

np.random.seed = 7


class Ant:
    graph = []
    EVA = 0.75
    Q = 1000000  # for easy comprehension of possibilities
    pheromone_random_range = 0.01, 0.1
    ALPHA = 0.5
    BETA = 1

    def __init__(self, vertex, num_vertices):
        self.graph_shape = num_vertices, num_vertices
        self.graph_pheromones = np.random.random(size=self.graph_shape)
        self.graph_pheromones = np.random.uniform(low=Ant.pheromone_random_range[0],
                                                  high=Ant.pheromone_random_range[0],
                                                  size=self.graph_shape)
        self.vertex = vertex or 0
        self.visited = np.zeros(num_vertices)
        self.num_vertices = num_vertices
        self.path = [vertex]
        self.length = 0
        self.visited[self.vertex] = 1

        self.move()

    def can_move(self):
        return np.count_nonzero(self.visited) < len(self.visited)

    def available_vertices(self):
        available = []
        for num, status in enumerate(self.visited):
            if status == 0:
                available.append(num)
        return available

    def move_on(self, vertices):
        probabilities = [(vertex, self.p(vertex, vertices)) for vertex in vertices]
        vertex, p = probabilities[0]
        best_vertex = vertex
        max_prob = p
        for vertex, p in probabilities:
            if max_prob < p:
                best_vertex = vertex
                max_prob = p

        self.path.append(best_vertex)

        self.length += Ant.graph[self.vertex][best_vertex]

        self.visited[best_vertex] = 1
        self.vertex = best_vertex

    def move(self):
        while self.can_move():
            self.move_on(self.available_vertices())
        else:
            index = 1
            while index < len(self.path):
                tau0 = self.graph_pheromones[self.path[index - 1]][self.path[index]]
                self.graph_pheromones[self.path[index - 1]][self.path[index]] = (1 - Ant.EVA) * tau0 + 1 / self.length
                index += 1
            self.back()

    def p(self, vertex, vertices):
        i = self.vertex
        j = vertex
        length = Ant.graph[i][j]
        tau = self.graph_pheromones[i][j]
        summary = 0
        for vertex in vertices:
            summary += Ant.graph[self.vertex][vertex] ** Ant.ALPHA / self.graph_pheromones[self.vertex][vertex] ** Ant.BETA

        if length != 0:
            return Ant.Q * (tau ** Ant.ALPHA) / (length ** Ant.BETA) / summary
        else:
            return 0

    def back(self):
        self.path.append(self.path[0])
        self.length += Ant.graph[self.vertex][self.path[0]]

    @staticmethod
    def calculate_min_path(input_matrix):
        """
        :param input_matrix: square matrix with lengths between vertices
        :return: minimum length to move along all vertices
        """
        for raw in input_matrix:
            Ant.graph.append(raw)
        size = len(Ant.graph[0])
        ants = [Ant(i, size) for i in range(size)]
        min_path = min(ant.length for ant in ants)
        return min_path


if __name__ == '__main__':
    row_number = 0
    lines = []
    while True:
        line = input()
        lines.append([int(i) for i in line.split()])
        row_number += 1
        number_of_vertices = len(lines[0])
        if number_of_vertices == row_number:
            break

    min_path_length = Ant.calculate_min_path(lines)
    print(min_path_length)
