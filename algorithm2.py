import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math

class Solution:    
    def simulation(self, project_length, constrain, owner_join):
        days = -1
        income = 0
        
        if owner_join:
            # potion, speed, price
            owner = [0, 2, 1000]
        else:
            owner = [0, 0, 0]
            
        potion = np.array([0, 0, 0, owner[0]])
        speed = np.array([1.0, 1.0, 1.0, owner[1]])
        price = np.array([1000, 1000, 1000, owner[2]])
        
        while income < constrain and days < project_length:
            days += 1
            self.boost_speed(potion, speed)
            if (days % 7 == 5 or days % 7 == 6):
                income += self.weekend_income(speed, price, potion)
                continue
            casted_speed = self.cast_spells(speed, price)
            income += self.get_daily_income(casted_speed, price, potion)
        return income

    
     
    def cast_spells(self, speed, price):
        rd = random.choices(range(3), k = 2)
        for i in rd:
            speed[i] = speed[i] * (1 + 0.18)
        for i in rd:
            price[i] += 100

        casted_speed = np.copy(speed)

        numbers = [1, 2]
        probabilities = [0.82, 0.18]

        for i in rd:
            casted_speed[i] = casted_speed[i] *  random.choices(numbers, probabilities)[0]

        return casted_speed
    
    def boost_speed(self, potion, speed):
        for i in range(0, len(potion)):
            speed[i] = speed[i] * (1 + (potion[i] % 10) * 0.07)
            potion[i] = potion[i] // 10

    # Get the total income in a day and increase portion (side effect)
    def get_daily_income(self, speed, price, potion):
        daily_potion = np.floor(speed)
        daily_income = np.sum(np.multiply(daily_potion, price))
        potion = np.add(daily_potion, potion)
        return daily_income

    # Check if it's profitable in weekend
    def weekend_income(self, speed, price, potion):
        daily_output = np.floor(speed)
        income = np.sum(np.multiply(daily_output, price)) - 7000
        if income > 0:
            potion = np.add(potion, daily_output)
            return income
        return 0

    # Create dataframe with project's length and probability as column
    def init_dataframe_prob(self, owner_join):
        prob = []

        for i in range(25):
            count = 0
            for j in range(10000):
                if self.simulation(i, 1000000, owner_join) >= 1000000:
                    count += 1
            prob.append(count / 10000)

        df = pd.DataFrame({"project_length": list(range(25)), "probability": prob})

        return df

    
    def get_income_list(self, owner_join):
        income_list = []
        sampling = np.random.choice(50, 1000, replace=True)

        income = []

        for num in sampling:
            income.append(self.simulation(num, float('inf'), owner_join))
        df = pd.DataFrame({"project_length": sampling, "income": income})
        return df

    def plot_prob(self, owner_join):
        df = self.init_dataframe_prob(owner_join)
        plt.figure(figsize=(10, 6))
        plt.plot(df['project_length'], df['probability'], marker='o', linestyle='-', color='blue', label='Probability')

        plt.xlabel('Project Length')
        plt.ylabel('Probability')
        plt.title('Project Length vs Probability')
        plt.grid(True)
        plt.legend()

        plt.show()
        
    def plot_income_QQ(self, owner_join):
        df = self.get_income_list(owner_join)
        
        plt.figure(figsize=(10, 6))
        stats.probplot(df['income'], dist="expon", plot=plt)
        plt.title('QQ Plot of Income')
        plt.xlabel('Theoretical Quantiles')
        plt.ylabel('Sample Quantiles')
        plt.grid()
        plt.show()

    def plot_distribution(self, owner_join):
        df = self.get_income_list(owner_join)
        
        # Histogram and Density Plot
        plt.figure(figsize=(10, 6))
        sns.histplot(df['income'], bins=30, kde=True, color='blue', stat="density", alpha=0.5)
        plt.title('Income Distribution with Density Estimate')
        plt.xlabel('Income')
        plt.ylabel('Density')
        plt.show()

        

        
        