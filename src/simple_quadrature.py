import numpy as np
from sympy import symbols, lambdify,  parse_expr

def create_function(n):
  syst = [] # Inicializa el vector vacio para el sistema de ecuaciones

  equation_str = input("Enter the integral: ") # Recibe la ecuacion del usuario
  x = symbols(' '.join(f'x{i}' for i in range(1, n + 1))) # Define la variable de la ecuacion
  equation_expr = parse_expr(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
  F = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy

  return F # Retorna la funcion callable_system(x0) para su utilizacion

def trapezoidal_rule(F, a, b, n):
  h = (b - a)/n
  integral = 0.5 * (F(a) + F(b))

  for i in range(1,n):
    integral += F(a + i*h)

  integral *= h
  return integral

def simpson_rule(F, a, b, n):
  if n%2 != 0:
    raise ValueError("Number of subintervals (n) should be an even number")
  
  h = (b-a)/n
  x_values = np.linspace(a,b,n+1)
  y_values = F(x_values)

  integral = h / 3 * (y_values[0] + 4 * np.sum(y_values[1:-1:2]) + 2 * np.sum(y_values[2:-2:2]) + y_values[-1])
    
  return integral

if __name__=='__main__':
  """
    TODO: Fix for multidimensional quadrature
  """
  n = 1 # Recibe el numero de ecuaciones
  F = create_function(n) # Crea el sistema de ecuacion evaluable F
  a = float(input('Enter the limit a: '))
  b = float(input('Enter the limit b: '))

  if(a>b): t=b; b=a; a=t

  steps = int(input('Enter the number of steps: '))

  integral = trapezoidal_rule(F, a, b, steps)
  print(f'Integral between points {a},{b} with Trapezoidal rule: ', integral) 

  if steps%2 != 0: steps += 1

  integral = simpson_rule(F, a, b, steps)
  print(f'Integral between points {a},{b} with Simpson rule: ', integral) 