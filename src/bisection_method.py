from scipy.optimize import fsolve, root_scalar
from sympy import symbols, lambdify

# f:   funcion lambda de la ecuacion
# a:   primer extremo del rango
# b:   segundo extremo rango
# tol: valor de toleracion para convergencia
def mybisect(f,a,b,tol=1e-12):
  if a>b : # Si a>b, intercambia  a y b
    t = a; a=b; b=t # Realiza el intercambia
  fa = f(a); fb = f(b) # Evalua f() con las variables: a y b
  if fa*fb > 0: raise ValueError # Si f(a)*f(b) > 0, lanza un error de valor. [1]
  v = 1 # Inicializa la variable v (para ajustar x entre lineas 18 y 19)
  if fa > 0: v = -1 #Si f(a) es positivo, v = -1
  x = 0.5*(a+b) # Obtiene el punto medio entre a y b y lo almacena en x
  k = 1 # Inicializa la variable para la iteracion
  while (b-a>tol) and (a<x) and (x<b): #Itera mientras b - a sea mayor al rango de tolerancia y a < x < b
    if v*f(x)>0: b = x # Si v*f(x) > 0, movemos b al punto x (punto medio entre a y b)
    else: a = x # En el caso contrario movemos a hacia el punto medio x
    x = 0.5*(a+b) # Recalcula el punto medio con el nuevo valor de x o y.
    k += 1 # Incremental el contador 
  return x, k # Tras finalizar el ciclo, retorna el punto x (aproximacion de f(x*)=0) y el numero de iteraciones realizadas

if __name__=='__main__':
  equation_str = input("Enter the equation: ") # Recibe la ecuacion del usuario
  x = symbols('x') # Define la variable de la ecuacion
  equation_expr = eval(equation_str.replace("^", "**")) # Parsea el String de la ecuacion a expression sympy
  f = lambdify(x, equation_expr, 'numpy') # Crea la funcion lambda desde la expresion sympy

  x, k = mybisect(f,1,0) # Invoca el metodo de biseccion implementado
  print('x_bisect =', x, '  after k = ', k, ' iterations.\n') # Imprime en pantalla el valor de x y el numero de iteraciones para converges
  x = fsolve(f,0,full_output=True) # Obtiene el valor de x con la funcion fsolve() de scipy
  print(x, '\n') # Muestra el valor obtenido con x
  print(root_scalar(f,bracket=[0,1], method='bisect')) # Obtiene la solucion con la funcion root_scalar