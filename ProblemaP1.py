import sys
from math import ceil, floor, log2

INF_NEG = -10**30

def construir(arr):
    n = len(arr)
    if n == 0:
        return [], []
    K = int(log2(n)) + 1
    st = [arr[:] ]
    j = 1
    while (1 << j) <= n:
        prev = st[j-1]
        tamano = n - (1<<j) + 1
        cur = [0]*tamano
        mitad = 1 << (j-1)
        for i in range(tamano):
            a = prev[i]
            b = prev[i + mitad]
            cur[i] = a if a >= b else b
        st.append(cur)
        j += 1
    lg = [0]*(n+1)
    for i in range(2, n+1):
        lg[i] = lg[i//2] + 1
    return st, lg

def max(st, lg, Iz, Der):
    if Iz > Der:
        return INF_NEG
    k = lg[Der - Iz + 1]
    a = st[k][Iz]
    b = st[k][Der - (1<<k) + 1]
    return a if a >= b else b

def resolver_caso(k, n, P):
    pesos = P + [0]
    nd = []
    x = n
    for _ in range(6):
        nd.append(x % 10)
        x //= 10
    siguiente = [0]
    max_siguiente = 0
    
    for p in range(5, -1, -1):
        Pp = pesos[p]
        ndp = nd[p]
        max_in = ndp + 10 * max_siguiente
        F = [INF_NEG] * (max_in + 1)
        H = [siguiente[c] + 3*Pp*c for c in range(max_siguiente + 1)]
        A = []
        ST = []
        LG = []
        for r in range(3):
            arr = []
            q = 0
            while 3*q + r <= max_siguiente:
                arr.append(H[3*q + r] + Pp*q)
                q += 1
            A.append(arr)
            st, lg = construir(arr)
            ST.append(st)
            LG.append(lg)
        
        for c_in in range(max_in + 1):
            L = ceil((c_in - ndp) / 10) if (c_in > ndp) else 0
            if L < 0: L = 0
            U = floor((9*k + c_in - ndp) / 10)
            if U > max_siguiente: U = max_siguiente
            if L > U:
                continue
            best = INF_NEG
            for r in range(3):
                qL = (L - r + 2) // 3
                qU = (U - r) // 3
                if qL < 0: qL = 0
                if qU >= 0 and qL <= qU and len(A[r]) > 0:
                    part = max(ST[r], LG[r], qL, qU)
                    part += Pp * ((ndp - c_in + r) // 3)
                    if part > best:
                        best = part
            F[c_in] = best
        siguiente = F
        max_siguiente = max_in
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