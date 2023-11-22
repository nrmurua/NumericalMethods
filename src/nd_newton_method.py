import numpy as np
from scipy.linalg import solve
from sympy import symbols, lambdify,  parse_expr

def create_system(n):
  syst = [] # Inicializa el vector vacio para el sistema de ecuaciones

  for i in range(n):
    equation_str = input(f"Enter the equation {i+1}: ") # Recibe la ecuacion del usuario
    x = symbols(' '.join(f'x{i}' for i in range(1, n + 1))) # Define la variable de la ecuacion
    equation_expr = parse_expr(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
    fi = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy
    syst.append(fi) # Agrega la funcion lambda al sistema de ecuaciones

  F = np.array(syst) # Crea el np.array F
  
  # Definicion de funcion para evaluar F
  def callable_system(x0): # Recibe un arreglo con n parametros, donde n es tambien la dimension de F
    return np.array([fi(*x0) for fi in F]) # Retorna la evaluacion de F(x0)

  return callable_system # Retorna la funcion callable_system(x0) para su utilizacion

# Funcion para calcular la matriz Jacobiana
def numerical_jacobian(F, x, h=1e-10):
  n = len(x) # Obtiene el largo del vector x
  J = np.zeros((n,n)) # Inicializa las dimensiones para la matriz jacobiana

  

  for i in range(n): # Itera con respecto a la dimension de x
    xh = x.copy() # Copia x en el vector xh
    xh[i] += h # Le suma h a cada posicion del vector xh (xh = x+h)
    J[:,i] = (F(xh)-F(x))/h # Calcula la derivada numerica con: (f(x+h)-f(x))/h por cada x_i

  return J # Retorna la matriz Jacobiana

# Funcion de metodo de newton en n dimensiones
def newton_method_nd(F, x0, tol=1e-12, maxit=100):
  x=x0 # Inicializa x con x0

  for i in range(maxit): # Itera hasta maxit veces
    fx = F(x) # Evalua F(x)
    J = numerical_jacobian(F,x) # Obtiene la matriz Jacobiana

    print(fx, '  ', i) # Debug

    delta_x = solve(J, fx) # Resuelve el sistema lineal

    x -= delta_x # Actualiza x = x-delta_x, delta_x = s

    if np.linalg.norm(fx) < tol: # Si la norma de fx es menor a la tolerancia
      return x, i+1 # Retorna x como aproximacion de x* y el numero de iteraciones realizadas
    
  raise ValueError("Newton's method did not converge") # Si llega a este punto no hubo convergencia, se indica con un error.

if __name__=='__main__':
  n = int(input('Enter the number of equations: ')) # Recibe el numero de ecuaciones

  F = create_system(n) # Crea el sistema de ecuacion evaluable F
  x0 = [] # Inicializa un arreglo de parametros vacio

  for i in range(n): # Itera hasta n, n:=dimension de F y de x
    a = input(f'Enter initial guess (x{i}): ') # Recibe xi
    a = float(a) # Parsea xi float
    x0.append(a) # Agrega xi al arreglo de parametros x0

  x, k = newton_method_nd(F,x0) # Invoca el metodo de newton para n dimensiones
  print('x_nm =', x, '  after k = ', k, ' iterations.\n') # Imprime en pantalla el valor de x y el numero de iteraciones para converges