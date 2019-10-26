import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def regression(t, f, xlabels, power=6, xlim_added=10, ylim_added=50, title=""):
    colors = ['blue', 'black', 'grey', 'cyan', 'magenta', 'yellow']
    for current_power in range(power):
        base = pd.DataFrame([[time ** i for time in t] for i in range(current_power + 1)], columns=t)
        c = calculate_polynomial_regression_coef(f, base)
        print("Coefficients: ")
        print(c)
        y = []
        for value in t:
            y.append(np.sum(np.multiply(c, [value ** i for i in range(current_power + 1)])))
        print(y)
        print(f)
        error = np.sum((f - y) ** 2) ** (1/2)
        print("Approximation error: " + str(error))
        name = ""
        index = 0
        for coef in c:
            if index > 0:
                name += " + " + str('{:06.2f}'.format(coef)) + " * t ^ " + str(index)
            else:
                name += str('{:06.2f}'.format(coef))
            index += 1
        plt.plot(y, color=colors[current_power % 6], label=name + ', e = ' + str('{:06.2f}'.format(error)))

    plt.plot(f, color='green', label='available data')
    plt.legend()
    plt.xlim(t[0] - xlim_added, t[-1] + xlim_added)
    plt.ylabel("Count")
    plt.ylim(np.min(f) - ylim_added, np.max(f) + ylim_added)
    plt.xlabel("Year")
    plt.xticks(t, xlabels, rotation='vertical')
    plt.title(title)
    plt.show()

def calculate_polynomial_regression_coef(f, B):
    return np.dot((np.dot(f, np.transpose(B))),
                       np.linalg.inv(np.dot(B, np.transpose(B))))

disasters_data = pd.read_csv('number-of-natural-disaster-events.csv')
disasters_data = disasters_data[disasters_data['Entity'] == 'All natural disasters']
data_sequence = np.array(disasters_data['Number of reported natural disasters (reported disasters)'])
time_sequence = np.array([time for time in range(len(data_sequence))])
regression(time_sequence, data_sequence, [str(1900 + number) if (1900 + number) % 10 == 0
                                                       else ""
                                                       for number in range(len(data_sequence))],
           title='All natural disasters by year (1900-2018)', power=6)
