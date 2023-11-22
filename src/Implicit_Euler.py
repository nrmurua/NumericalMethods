import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from sympy import symbols, lambdify, parse_expr, Function, dsolve, Eq, Derivative

def create_function(n):
  equation_str = input("Enter the right part of the ODE: y' = ")  # Recibe la ecuacion del usuario
  x = symbols('y1:' + str(n + 1) + ' t')  # Define la variable de la ecuacion
  equation_expr = parse_expr(equation_str.replace("^", "**"))  # Parsea el String de la ecuacion a expression sympy
  F = lambdify(list(x), equation_expr, modules=['numpy'])  # Crea la funcion lambda desde la expresion sympy

  return F, equation_expr  # Retorna la funcion callable_system(x0) y la expresion sympy

def implicit_euler(F, y0, time, h):
  steps = int(time/h)+1
  y = np.zeros(steps)
  y[0] = y0
  t = np.linspace(0,time,steps)

  for i in range(1, steps):
    fi = F(y[i], t[i])
    print(f'f{i}: {fi}')
    y[i] = y[i-1] + h*fi

  return t, y

if __name__=='__main__':
  F, equation_expr = create_function(1)
  y0 = float(input('Enter the initial condition for y0: '))
  T = float(input('Enter the total integration time T: '))
  h = float(input('Enter the time-step size h: '))

  t, y = implicit_euler(F, y0, T, h)

  # Plot numerical solution
  plt.plot(t, y, label='Implicit Euler')

  '''
    TODO: FIX for comparison with a symbolic solution of the equation
    TODO: Also testing
  '''


  plt.xlabel('Time')
  plt.ylabel('Solution')
  plt.legend()
  plt.show()