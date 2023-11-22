import numpy as np
from sympy import symbols, lambdify,  parse_expr
import matplotlib.pyplot as plt

def create_system(n):
    print('Indicate variables as x1, x2, ..., and t for time') # Print de instruccion
    
    equation_str = input("Enter the equation: ") # Recibe el modelo matematico
    variables = symbols(' '.join(f'x{i}' for i in range(1, n + 1)) + ' t') # Define las variables que se utilizaran para evaluar la funcion
    equation_expr = parse_expr(equation_str.replace("^", "**")) # Parsea el string de la ecuacion
    F = lambdify(variables, equation_expr, 'numpy') # Transforma el modelo a una funcion lambda

    def callable_system(x, time_vector): # Se define una funcion invocable que evalua F(x,t)
        model_predictions = F(*x, time_vector) # Se obtiene la prediccion del modelo
        return model_predictions # Retorna la prediccion del modelo, termina la funcion invocable

    return callable_system # Se retorna la funcion invocable

def numerical_jacobian(F, x, time_vector, h=1e-12):
    nx = len(x) # Obtiene la cantidad de parametros
    n_output = len(F(x, time_vector)) # Obtiene la cantidad de evaluaciones de cada f(x,t_i)

    J = np.zeros((n_output, nx)) # Inicializa las dimensiones para la matriz Jacobiana

    for i in range(nx): # Por cada parametro
        xh = x.copy() # Crea una copia de los parametros
        xh[i] += h # Le suma 'h' al x_i por el cual se esta diferenciando
        J[:, i] = (F(xh, time_vector) - F(x, time_vector)) / h # Almacena todos los resultados obtenidos de la derivada parcial con respecto a x_i

    return J # Retorna la matriz Jacobiana

def gauss_newton(F, x0, t, observed_data, maxit=100000, tol=1e-10):
  x = x0.copy() # Crea una copia del vector de valores iniciales x0
  print(f'Initial parameters value:\n\n', x, '\n\n') # Print x para debug

  for it in range(maxit): # Itera hasta 'maxit' veces
    s = F(x, t) - observed_data # Obtiene los residuos evaluando F(x)
    print(f'Residuals on iteration {it+1}:\n\n', s,'\n\n') # Print s para debug
    J = numerical_jacobian(F, x,t) # Obtiene la matriz jacobiana
    print(f'Jacobian on iteration {it+1}:\n\n', J, '\n\n') # Print J para debug
    delta_x = np.linalg.lstsq(J, s, rcond=None)[0] # Computa delta_x para la actualizacion de los parametros
    print(f'Update value on iteration {it+1}:\n\n', delta_x,'\n\n') # Print delta_x para debug
    x -= delta_x # Actualiza el valor de x
    print(f'Parameters value after iteration {it+1}:\n\n', x, '\n\n') # Print x para debug
    print(f'Norm of update value after iteration {it+1}:\n\n', np.linalg.norm(delta_x), '\n\n') # Print norm para debug
    if np.linalg.norm(delta_x) < tol: # Si la norma de delta_x (correccion) es suficientemente pequeña
      return x, it+1 # Retorna los valores aproximados de los parametros x y el numero de iteraciones realizadas
    
  raise ValueError("Gauss-Newton did not converge.") # En caso de llegar a este punto, no hubo convergencia

def read_data(src):
  filename = src # Copia el nombre del archivo txt que contiene los datos
  
  with open(filename, 'r') as file: # Abre el archivo txt
    rows, columns = map(int,file.readline().split()) # Obtiene el numero de filas y columnas desde la primera linea del archivo txt
    data = np.empty((rows, columns)) # inicializa la matriz data con sus dimensiones respectivas

    for i in range(rows): # Itera por el numero de filas
      row_data = list(map(float, file.readline().split())) # Obtiene el valor de cada fila en el archivo txt
      data[i,:] = row_data # Copia los valores de la fila a la matriz data

    return data # Retorna la matriz con los datos

def split_columns(data, col): 
  return [data[:,i] for i in range(col)] # Retorna cada columna de una matriz como un arreglo independiente 

def read_times(src):
  filename = src # Copia el nombre del archivo txt que contiene los datos

  with open(filename, 'r') as file: # Abre el archivo txt
      num_rows = int(file.readline()) # Obtiene el numero de filas desde la primera linea del archivo txt
      t = np.zeros(num_rows) # inicializa el vector tiempo con sus dimensiones respectivas

      for i in range(num_rows): # Itera por el numero de filas
          t[i] = float(file.readline()) # Copia los valores de la fila a la matriz data

  return t # Retorna el vector con los tiempos

if __name__ == '__main__':
    data = read_data('numerical_methods/src/data/C.txt') # Lectura de datos experimentales
    print(data) # Print para debug
    n_cols = data.shape[1] # Se obtiene el numero de columnas
    cols_vect = split_columns(data, n_cols) # Se divide la matriz data en un arreglo de vectores columna

    t = read_times('numerical_methods/src/data/TC.txt') # Lectura de tiempos asociados a los valores observados
    print(t) # Print para debug

    # Print de las columnas para debug
    for i, c in enumerate(cols_vect):
        print(f"Column {i + 1} vector:")
        print(c)
        print() 


    n = int(input('Enter the number of variables (t doesn`t count): ')) # Se obtiene el numero de variables (sin considera lols tiempos t)
    F = create_system(n) # Se invoca el metodo para crear el modelo
    x0 = [] # Se inicializa un arreglo de parametros vacio

    for i in range(n): # Itera por cada parametro
        a = input(f'Enter initial guess (x{i+1}): ') # Obtiene el valor inicial para el parametro 
        a = float(a) # Parsea a float
        x0.append(a) # Lo agrega al arreglo de parametros

    x, it = gauss_newton(F, x0, t, cols_vect[0]) # Aplica el metodo de Gauss Newton utilizando la funcion, los parametros, el tiempo, y los datos observados (cols_vect[i])

    # En caso de ejecutar la siguiente seccion, el metodo de Gauss Newton obtuvo convergencia
    # Prints informativos de solucion y para debug

    print('Gauss-Newton converged')
    print('Parameters for the model: \n\n', x, '\n\n')
    print('Number of iterations: ', it)

    # La siguiente seccion genera un grafico comparativo entre los valores observados y los resultados del modelo utilizado con los parametros obtenidos

    observed_data = cols_vect[0]
    fitted_model = F(x, t)

    plt.scatter(t, observed_data, label='Observed Data')
    plt.plot(t, fitted_model, label='Fitted Model', color='red')
    plt.xlabel('Time')
    plt.ylabel('Observations')
    plt.legend()
    plt.title('Observed Data and Fitted Model')
    plt.show()