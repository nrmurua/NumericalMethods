import numpy as np
import matplotlib.pyplot as plt

# Define the function
def my_function(x1, x2, t):
    return x1 * np.sqrt(t) + x2 * t

# Generate some sample data
x1 = 60
x2 = -10
t_values = np.linspace(0, 10, 100)  # Adjust the range and number of points as needed
y_values = my_function(x1, x2, t_values)

# Plot the function
plt.plot(t_values, y_values, label=r'$x_1 \sqrt{t} + x_2 t$')
plt.xlabel('t')
plt.ylabel('Function Value')
plt.title('Plot of x1*sqrt(t) + x2*t')
plt.legend()
plt.grid(True)
plt.show()