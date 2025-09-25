import sys
from math import ceil, floor

INF_NEG = -10**30

def construir(arreglo):
    n = len(arreglo)
    if n == 0:
        return [], []
    tabla_maximos = [arreglo[:] ]
    nivel = 1
    while (1 << nivel) <= n:
        nivel_anterior = tabla_maximos[nivel-1]
        tamaño = n - (1<<nivel) + 1
        nivel_actual = [0]*tamaño
        mitad = 1 << (nivel-1)
        for i in range(tamaño):
            a = nivel_anterior[i]
            b = nivel_anterior[i + mitad]
            nivel_actual[i] = a if a >= b else b
        tabla_maximos.append(nivel_actual)
        nivel += 1
    logaritmos = [0]*(n+1)
    for i in range(2, n+1):
        logaritmos[i] = logaritmos[i//2] + 1
    return tabla_maximos, logaritmos

def max(tabla_maximos, logaritmos, inicio, fin):
    if inicio > fin:
        return INF_NEG
    k = logaritmos[fin - inicio + 1]
    a = tabla_maximos[k][inicio]
    b = tabla_maximos[k][fin - (1<<k) + 1]
    return a if a >= b else b

def resolver_caso(k, n, datosCreatividad):
    creatividad = datosCreatividad + [0]
    digitos = []
    x = n
    for _ in range(6):
        digitos.append(x % 10)
        x //= 10
    siguiente = [0]
    max_siguiente = 0
    
    for p in range(5, -1, -1):
        creatividad_actual = creatividad[p]
        digito_actual = digitos[p]
        max_entrada = digito_actual + 10 * max_siguiente
        resultado_actual = [INF_NEG] * (max_entrada + 1)
        valores_transformados = [siguiente[c] + 3 * creatividad_actual * c for c in range(max_siguiente + 1)]
        lista_residuos = []
        tablas = []
        tablas_logaritmos = []
        for residuo in range(3):
            arr = []
            multiplicador = 0
            while 3 * multiplicador + residuo <= max_siguiente:
                arr.append(valores_transformados[3 * multiplicador + residuo] + creatividad_actual * multiplicador)
                multiplicador += 1
            lista_residuos.append(arr)
            tabla_maximos, logaritmos = construir(arr)
            tablas.append(tabla_maximos)
            tablas_logaritmos.append(logaritmos)
        
        for c_actual in range(max_entrada + 1):
            limite_inferior = ceil((c_actual - digito_actual) / 10) if (c_actual > digito_actual) else 0
            if limite_inferior < 0: limite_inferior = 0
            limite_superior = floor((9 * k + c_actual - digito_actual) / 10)
            if limite_superior > max_siguiente: limite_superior = max_siguiente
            if limite_inferior > limite_superior:
                continue
            mejor_sol = INF_NEG
            for residuo in range(3):
                inicio_q = (limite_inferior - residuo + 2) // 3
                fin_q = (limite_superior - residuo) // 3
                if inicio_q < 0: inicio_q = 0
                if fin_q >= 0 and inicio_q <= fin_q and len(lista_residuos[residuo]) > 0:
                    sol_parcial = max(tablas[residuo], tablas_logaritmos[residuo], inicio_q, fin_q)
                    sol_parcial += creatividad_actual * ((digito_actual - c_actual + residuo) // 3)
                    if sol_parcial > mejor_sol:
                        mejor_sol = sol_parcial
            resultado_actual[c_actual] = mejor_sol
        siguiente = resultado_actual
        max_siguiente = max_entrada
    return siguiente[0]

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        k = int(next(it)); n = int(next(it))
        P0 = int(next(it)); P1 = int(next(it)); P2 = int(next(it)); P3 = int(next(it)); P4 = int(next(it))
        ans = resolver_caso(k, n, [P0, P1, P2, P3, P4])
        print(ans)
        sys.stdout.flush()

if __name__ == "__main__":
    main()