# Calcula experiencia
def multiplica_por_2(num):
    arr = []
    for i in range(num+1):
        arr.append(i*2)
    # print(arr)
    return arr
multiplica_por_2(5)
# Debe retornar: [0, 2, 4, 6, 8, 10]

# Analiza publicaciones
def suma_y_resta(arr):
    # arr debe tener 2 valores en [0] y [1]
    print(arr[0] + arr[1])
    return arr[0] - arr[1]
print(suma_y_resta([120, 115]))
# Imprime: 235 y retorna: 5


# Puntaje ajustado
def sumatoria_menos_longitud(arr):
    sum = 0
    for i in arr:
        sum += i
    print(f"Suma total = {sum}, lontigud = {len(arr)}")
    return sum - len(arr)
print(sumatoria_menos_longitud([10, 5, 3, 7]))
# Suma total = 25, longitud = 4, debe retornar: 21


# Ajusta visualizaciones
def valores_multiplicados_segundo(arr):
    print(len(arr))
    newArr = []
    if len(arr) < 2:
        return newArr
    for i in arr:
        newArr.append(i * arr[1])
    return newArr

print(valores_multiplicados_segundo([100, 3, 50, 20]))
# Imprime: 4 y retorna: [300, 9, 150, 60]

print(valores_multiplicados_segundo([100]))
# Imprime: 1 y retorna: []


# Genera precio fijo
def valor_multiplicado_longitud(par1,par2):
    newArr = []
    for i in range(par2):
        newArr.append(par1 * par2)
    return newArr
print(valor_multiplicado_longitud(5, 2))
# Debe retornar: [10, 10]

print(valor_multiplicado_longitud(7, 5))
# Debe retornar: [35, 35, 35, 35, 35]