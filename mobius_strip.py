import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import euclidean

class MobiusStrip:
    def __init__(self, R=1.0, w=0.2, n=100):
        # Initialize parameters:
        # R: radius of the central circle
        # w: width of the strip
        # n: number of points for mesh resolution
        self.R = R
        self.w = w
        self.n = n
        
        # Parameter u runs along the length of the strip [0, 2π]
        self.u = np.linspace(0, 2 * np.pi, n)
        # Parameter v runs across the width [-w/2, w/2]
        self.v = np.linspace(-w / 2, w / 2, n)
        
        # Create meshgrid of parameters for surface coordinates
        self.U, self.V = np.meshgrid(self.u, self.v)
        
        # Compute 3D coordinates from parametric equations
        self.X, self.Y, self.Z = self._compute_mesh()

    def _compute_mesh(self):
        # Parametric equations defining Mobius strip surface:
        # (R + v*cos(u/2)) * cos(u)
        # (R + v*cos(u/2)) * sin(u)
        # v * sin(u/2)
        U, V = self.U, self.V
        X = (self.R + V * np.cos(U / 2)) * np.cos(U)
        Y = (self.R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    def surface_area(self):
        # Calculate approximate surface area via numerical integration
        dU = self.u[1] - self.u[0]  # step size along u
        dV = self.v[1] - self.v[0]  # step size along v
        
        # Compute partial derivatives of surface wrt u and v
        Xu = np.gradient(self.X, dU, axis=1)
        Yu = np.gradient(self.Y, dU, axis=1)
        Zu = np.gradient(self.Z, dU, axis=1)
        Xv = np.gradient(self.X, dV, axis=0)
        Yv = np.gradient(self.Y, dV, axis=0)
        Zv = np.gradient(self.Z, dV, axis=0)
        
        # Calculate magnitude of the cross product of partial derivatives (Jacobian)
        cross_prod = np.sqrt((Yu * Zv - Zu * Yv)**2 +
                             (Zu * Xv - Xu * Zv)**2 +
                             (Xu * Yv - Yu * Xv)**2)
        
        # Surface area ≈ sum of Jacobian values * dU * dV (area elements)
        return np.sum(cross_prod) * dU * dV

    def edge_length(self):
        # Calculate length of one edge (v = w/2 side) of the Mobius strip
        edge_coords = np.array([
            # Parametric coordinates for edge curve (fixed v = w/2)
            ((self.R + self.w / 2 * np.cos(u / 2)) * np.cos(u),
             (self.R + self.w / 2 * np.cos(u / 2)) * np.sin(u),
             self.w / 2 * np.sin(u / 2))
            for u in self.u
        ])
        
        # Sum Euclidean distances between consecutive points on the edge curve
        return sum(euclidean(edge_coords[i], edge_coords[i + 1])
                   for i in range(len(edge_coords) - 1))

    def plot(self):
        # 3D plot of the Mobius strip surface
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot surface with light blue color, semi-transparent
        ax.plot_surface(self.X, self.Y, self.Z, color='skyblue', edgecolor='gray', alpha=0.8)
        
        ax.set_title("Mobius Strip")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    mobius = MobiusStrip(R=1.0, w=0.2, n=200)
    
    # Calculate and print surface area and edge length approximations
    area = mobius.surface_area()
    edge = mobius.edge_length()
    print(f"Surface Area ≈ {area:.5f}")
    print(f"Edge Length ≈ {edge:.5f}")
    
    # Visualize the strip
    mobius.plot()
