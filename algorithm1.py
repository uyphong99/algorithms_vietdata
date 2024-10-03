import numpy as np
import random

class Solution:
    def simulate_tosses(self, trials: int, prob: float):
        results = []
        for _ in range(trials):
            count = 0
            consecutive_heads = 0
            while consecutive_heads < 3:
                count += 1
                if np.random.rand() <= prob:
                    consecutive_heads += 1
                else:
                    consecutive_heads = 0
            results.append(count)
        return self.compute_mean_and_confidence(results, trials)

    def simulate_2dice(self, trials: int):
        results = []
        list_head = [11, 16, 61, 66]
        for _ in range(trials):
            count = 0
            consecutive_heads = 0
            cur_set = set()
            while len(cur_set) < 3:
                count += 1
                cur_num = random.randrange(1, 7) * 10 + random.randrange(1, 7)
                if cur_num in list_head:
                    if cur_num in cur_set:
                        cur_set.clear()
                    cur_set.add(cur_num)
                else:
                    cur_set.clear()
            results.append(count)
        return self.compute_mean_and_confidence(results, trials)
        
    def compute_mean_and_confidence(self, results, trials):
        mean_tosses = np.mean(results)
        std_error = np.std(results) / np.sqrt(trials)
        confidence_interval = (mean_tosses - 1.96 * std_error, mean_tosses + 1.96 * std_error)
        return mean_tosses, confidence_interval
        
