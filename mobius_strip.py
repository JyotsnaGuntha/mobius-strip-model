import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import euclidean

class MobiusStrip:
    def __init__(self, R=1.0, w=0.2, n=100):
        self.R = R
        self.w = w
        self.n = n
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self.X, self.Y, self.Z = self._compute_mesh()

    def _compute_mesh(self):
        U, V = self.U, self.V
        X = (self.R + V * np.cos(U / 2)) * np.cos(U)
        Y = (self.R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    def surface_area(self):
        dU = self.u[1] - self.u[0]
        dV = self.v[1] - self.v[0]
        Xu = np.gradient(self.X, dU, axis=1)
        Yu = np.gradient(self.Y, dU, axis=1)
        Zu = np.gradient(self.Z, dU, axis=1)
        Xv = np.gradient(self.X, dV, axis=0)
        Yv = np.gradient(self.Y, dV, axis=0)
        Zv = np.gradient(self.Z, dV, axis=0)
        cross_prod = np.sqrt((Yu * Zv - Zu * Yv)**2 +
                             (Zu * Xv - Xu * Zv)**2 +
                             (Xu * Yv - Yu * Xv)**2)
        return np.sum(cross_prod) * dU * dV

    def edge_length(self):
        edge_coords = np.array([
            ((self.R + self.w / 2 * np.cos(u / 2)) * np.cos(u),
             (self.R + self.w / 2 * np.cos(u / 2)) * np.sin(u),
             self.w / 2 * np.sin(u / 2))
            for u in self.u
        ])
        return sum(euclidean(edge_coords[i], edge_coords[i + 1])
                   for i in range(len(edge_coords) - 1))

    def plot(self):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, color='skyblue', edgecolor='gray', alpha=0.8)
        ax.set_title("Mobius Strip")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    mobius = MobiusStrip(R=1.0, w=0.2, n=200)
    area = mobius.surface_area()
    edge = mobius.edge_length()
    print(f"Surface Area ≈ {area:.5f}")
    print(f"Edge Length ≈ {edge:.5f}")
    mobius.plot()
