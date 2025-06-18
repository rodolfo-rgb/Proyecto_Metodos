import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def Graph_restrictions(restrictions, type, Z):
    x = np.linspace(0, 20, 400)
    plt.figure(figsize=(10, 6))

    # Graficar restricciones
    for i, restriction in enumerate(restrictions):
        a, b, c = restriction
        if b != 0:
            y = (c - a*x) / b
            plt.plot(x, y, label=f'Restricción {i+1}')
        else:
            x_val = c / a
            plt.axvline(x=x_val, label=f'Restricción {i+1}')

    plt.xlim(0, max(x))
    plt.ylim(0, max(x))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Método Gráfico - Programación Lineal')
    plt.legend()
    plt.grid()

    faseable_points = []

    for xi in np.linspace(0, 20, 200):
        for yi in np.linspace(0, 20, 200):
            faseable = True
            for a, b, c in restrictions:
                if a*xi + b*yi > c + 1e-5:
                    faseable = False
                    break
            if faseable:
                faseable_points.append((xi, yi))

    if faseable_points:
        faseable_points = np.array(faseable_points)
        plt.scatter(faseable_points[:, 0], faseable_points[:, 1], s=1, color='gray', alpha=0.5)

    # Resolver el problema de optimización
    c = -np.array(Z) if type.lower() == 'max' else np.array(Z)
    A = []
    b_vals = []
    for a, b, c_restriction in restrictions:
        A.append([a, b])
        b_vals.append(c_restriction)

    res = linprog(c, A_ub=A, b_ub=b_vals, bounds=(0, None))
    if res.success:
        x_opt, y_opt = res.x
        plt.scatter([x_opt], [y_opt], color='red', s=50, label='Óptimo')
        plt.legend()
        print(f"\nSolución óptima: x = {x_opt:.2f}, y = {y_opt:.2f}")
        print(f"Valor óptimo de Z: {np.dot(Z, [x_opt, y_opt]):.2f}")
    else:
        print("No se encontró una solución óptima.")

    plt.show()


def main():
    print("MÉTODO GRÁFICO - PROGRAMACIÓN LINEAL")
    type = input("¿Tipo de optimización? ('max' o 'min'): ").strip().lower()

    # Ingresar función objetivo
    Z = []
    Z.append(float(input("Coeficiente de x en Z: ")))
    Z.append(float(input("Coeficiente de y en Z: ")))

    # Ingresar restricciones
    restrictions = []
    n = int(input("¿Cuántas restricciones deseas ingresar?: "))
    for i in range(n):
        print(f"\nRestricción {i+1}: a*x + b*y <= c")
        a = float(input("  a: "))
        b = float(input("  b: "))
        c = float(input("  c: "))
        restrictions.append([a, b, c])

    Graph_restrictions(restrictions, type, Z)

if __name__ == "__main__":
    main()
