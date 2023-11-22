import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre
from sympy import symbols, lambdify,  parse_expr

def create_function(n):
  syst = [] # Inicializa el vector vacio para el sistema de ecuaciones

  equation_str = input("Enter the integral: ") # Recibe la ecuacion del usuario
  x = symbols(' '.join(f'x{i}' for i in range(1, n + 1))) # Define la variable de la ecuacion
  equation_expr = parse_expr(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
  F = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy

  return F # Retorna la funcion callable_system(x0) para su utilizacion

def gaussian_quadrature(f, a, b, n):
  x, w = roots_legendre(n)
  x_mapped = 0.5*(b-a)*x + 0.5*(b+a)

  integral = np.sum(w*F(x_mapped))

  return 0.5*(b-a)*integral

if __name__=='__main__':
  """
    TODO: Fix for multidimensional quadrature
  """

  n = 1
  F = create_function(n) # Crea la funcion lambda: F(x)
  a = float(input('Enter the limit a: '))
  b = float(input('Enter the limit b: '))

  if(a>b): t=b; b=a; a=t

  steps = int(input('Enter the number of steps: '))

  integral = gaussian_quadrature(F, a, b, steps)
  print(f'Integral between points {a},{b} with Trapezoidal rule: ', integral) 
