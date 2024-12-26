import numpy as np

class ACO_TSP:
    def __init__(self, points, n_dim, distance, size_pop=10, max_iter=20, distance_matrix=None, alpha=1, beta=1, rho=0.1):
        self.points = points
        self.n_dim = n_dim
        self.size_pop = size_pop
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.distance = distance
        self.distance_matrix = distance_matrix
        self.prob_matrix_distance = 1 / (distance_matrix + 1e-10 * np.eye(n_dim, n_dim))
        self.Tau = np.ones((n_dim, n_dim))
        self.Table = np.zeros((size_pop, n_dim)).astype(int)
        self.y = None
        self.generation_best_X, self.generation_best_Y, self.generation_best_N = [], [], []
        self.x_best_history, self.y_best_history = self.generation_best_X, self.generation_best_Y
        self.best_x, self.best_y = None, None

    def run(self):
        best_iter_length = []
        best_iter_target = []
        best_gen = 0

        for i in range(self.max_iter):
            self._construct_solutions()
            y_best_iter, unvis_best_iter, best_gen = self._update_best_solution(i, best_iter_length, best_iter_target, best_gen)
            self._update_pheromones()

        self.best_x = self.generation_best_X[best_gen]
        self.best_y = self.generation_best_Y[best_gen]

        return self.best_x, self.best_y, self.n_dim - unvis_best_iter - 2

    def construct_solutions(self):
        prob_matrix = self._calculate_probabilities()
        for j in range(self.size_pop):
            self._construct_solution_for_ant(j, prob_matrix)

    def calculate_probabilities(self):
        prob_matrix = (self.Tau ** self.alpha) * (self.prob_matrix_distance) ** self.beta
        return prob_matrix / (prob_matrix.sum(axis=1, keepdims=True) + 1e-10)

    def construct_solution_for_ant(self, ant_index, prob_matrix):
        taboo_set_dist = []
        local_route_length = 0
        for k in range(self.n_dim - 2):
            taboo_set = self._get_taboo_set(ant_index, local_route_length)
            allow_list = self._get_allow_list(taboo_set)
            next_point = self._choose_next_point(allow_list, prob_matrix, ant_index, local_route_length)
            self._update_table_and_check_distance(ant_index, next_point, local_route_length, taboo_set_dist)
            local_route_length = self._update_local_route_length(next_point, local_route_length, ant_index, taboo_set_dist)
        self._complete_solution(ant_index, taboo_set_dist)

    def get_taboo_set(self, ant_index, local_route_length):
        return set(self.Table[ant_index, :local_route_length + 1])

    def get_allow_list(self, taboo_set):
        return list(set(range(self.n_dim - 1)) - taboo_set)

    def choose_next_point(self, allow_list, prob_matrix, ant_index, local_route_length):
        return np.random.choice(allow_list, size=1, p=prob_matrix[self.Table[ant_index, local_route_length], allow_list])[0]

    def update_table_and_check_distance(self, ant_index, next_point, local_route_length, taboo_set_dist):
        y = np.array([self._calculate_total_distance(self.Table[ant_index], local_route_length + 1)])
        if (y[0] + self._calculate_distance(next_point, self.n_dim - 1)) > self.distance:
            taboo_set_dist.append(next_point)
            self.Table[ant_index, local_route_length + 1] = 0
            return
        self.Table[ant_index, local_route_length + 1] = next_point

    def update_local_route_length(self, next_point, local_route_length, ant_index, taboo_set_dist):
        if next_point not in taboo_set_dist:
            return local_route_length + 1
        return local_route_length

    def complete_solution(self, ant_index, taboo_set_dist):
        self.Table[ant_index, self.n_dim - 1 - len(taboo_set_dist)] = self.n_dim - 1

    def calculate_total_distance(self, routine, num_points):
        return sum([self.distance_matrix[routine[i], routine[i + 1]] for i in range(num_points)])

    def calculate_distance(self, i, j):
        return self.distance_matrix[i, j]

    def update_best_solution(self, current_iteration, best_gen):
        y_best_iter = 2 * self.distance
        unvis_best_iter = self.n_dim

        for i, ant in enumerate(self.Table):
            y = self._calculate_total_distance(ant, self.n_dim - self.generation_best_N[i][0])
            if self.generation_best_N[i][0] < unvis_best_iter or (self.generation_best_N[i][0] == unvis_best_iter and y < y_best_iter):
                unvis_best_iter = self.generation_best_N[i][0]
                y_best_iter = y
                best_gen = current_iteration
        return y_best_iter, unvis_best_iter, best_gen

    def update_pheromones(self):
        delta_tau = np.zeros((self.n_dim, self.n_dim))
        for ant in self.Table:
            for k in range(self.n_dim - 1 - self.generation_best_N[ant][0]):
                n1, n2 = ant[k], ant[k + 1]
                delta_tau[n1, n2] += 1 / self._calculate_total_distance(ant, self.n_dim - 1)
        self.Tau = (1 - self.rho) * self.Tau + delta_tau
