import numpy as np

class Solution:
    def generate_matrix(self, height, width, num_X):
        matrix = np.array([True] * num_X + [False] * (height * width - num_X))
        np.random.shuffle(matrix)
        matrix = matrix.reshape((height, width))
        return matrix

    def dfs(self, x, y, matrix, visited):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        height = len(matrix)
        width = len(matrix[0])
        
        stack = [(x, y)]
        cell_count = 0
        
        while stack:
            cx, cy = stack.pop()
            
            if visited[cx][cy]:
                continue
            
            visited[cx][cy] = True
            cell_count += 1
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                
                if 0 <= nx < height and 0 <= ny < width and matrix[nx][ny] and not visited[nx][ny]:
                    stack.append((nx, ny))

        return cell_count

    def count_string_cells(self, matrix, thresh_hold):
        height = len(matrix)
        width = len(matrix[0])
        visited = [[False for _ in range(width)] for _ in range(height)]
        total_cells = 0
        for i in range(height):
            for j in range(width):
                if matrix[i][j] and not visited[i][j]:
                    string_size = self.dfs(i, j, matrix, visited)
                    if (string_size >= thresh_hold):
                        total_cells += string_size
        return total_cells

    def prob_of_str(self, simulation_time, thresh_hold):
        cells = 0
        general_prob = 0
        for i in range(simulation_time):
            matrix = self.generate_matrix(19, 5, 18)
            general_prob += (self.count_string_cells(matrix, 2) / 18) / simulation_time
        return general_prob

    