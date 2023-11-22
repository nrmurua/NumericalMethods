from scipy.misc import derivative
from scipy.optimize import fsolve, root_scalar
from sympy import symbols, lambdify

def newton_method1d(F, x0, tol=1e-12, maxit=100, h=1e-10):
  x = x0 # Prepara el valor x
  for iteration in range(maxit): # Itera hasta un maximo de veces
      fx = F(x) # Evalua F(x)
      dfx = derivative(F, x, dx=h) # Obtiene la derivada numerica de F con respecto a x

      if abs(dfx) < tol: # Si el valor absoluto de la derivada numerica es menor que la tolerancia
         raise ValueError("Derivative is close to zero. May not converge") # Lanza error indicando que |dfx| se acerca a 0
      
      x -= fx/dfx # Actualiza el valor de x con (fx/dfx): x(k+1) = x(k) - s, s=fx/dfx

      if abs(fx) < tol: # Si el valor absoluto de la funcion evaluada en x es menor que la tolerancia
        return x, iteration+1 # Retorna el valor de x y el numero de iteraciones ejecutadas
      
  raise ValueError("Newton's method didn't converge on ", maxit, ' steps') # Si llega a este punto no se obtuvo convergencia, indica un error

if __name__=='__main__':
  equation_str = input("Enter the equation: ") # Recibe la ecuacion del usuario
  x = symbols('x') # Define la variable de la ecuacion
  equation_expr = eval(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
  f = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy

  a = input('Enter initial guess (x0): ') # Recibe x0
  x0 = float(a) # Parsea a float

  x, k = newton_method1d(f,x0) # Invoca el metodo de biseccion implementado
  print('x_nm =', x, '  after k = ', k, ' iterations.\n') # Imprime en pantalla el valor de x y el numero de iteraciones para converges
  print(root_scalar(f,x0=x0, method='newton')) # Obtiene la solucion con la funcion root_scalar
