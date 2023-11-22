from scipy.optimize import fsolve, root_scalar
from sympy import symbols, lambdify

def secant(f, x0, x1, maxit=50, tol=1e-12):
  f0 = f(x0) # Evalua f(x0)
  for k in range(maxit): # Itera 'maxit' veces
    fn = f(x1) # Evalua f(x1)
    print ('x1 = ', x1, 'f(x1) = ', fn) # Mostrando progreso
    s = fn * (x1 - x0)/(fn - f0) # Obtiene la variacion para x1 
    x0 = x1; x1 -= s # x0 <---x1, x1 se actualiza a x1-s
    if abs(s)<tol: # Si el valor absoluto de s es menor a la tolerancia (Convergencia):
      return x1, k # Retorna x1 como aproximacion de x* y el numero de iteraciones realizadas
    f0 = fn # Actualiza f0 para repetir el proceso 
  x = None # Sin convergencia
  return x, maxit # Retorna x=null y el conteo ded todas las iteraciones

if __name__=='__main__':
  equation_str = input("Enter the equation: ") # Recibe la ecuacion del usuario
  x = symbols('x') # Define la variable de la ecuacion
  equation_expr = eval(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
  f = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy

  a = input("Enter x0: ") # Recibe x0
  b = input("Enter x1: ") # Recibe x1

  x0 = float(a) # Parsea x0 a float
  x1 = float(b) # Parsea x1 a float

  x, k = secant(f,x0,x1) # Invoca el metodo de secante implementado
  print('x_secant =', x, '  after k = ', k, ' iterations.\n') # Imprime en pantalla el valor de x y el numero de iteraciones para converger
  print(root_scalar(f, x0=x0, x1=x1, method='secant')) # Obtiene la solucion con la funcion root_scalar
