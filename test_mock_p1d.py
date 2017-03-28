import numpy as np
import matplotlib.pyplot as plt
import mock_p1d as mock

# central redshift
z_c = 3.0
# number of cells (power of two)
N2 = 15
# cell width (in km/s)
dv_kms=10
# get redshift for each cell
z = mock.get_redshifts(z_c,N2,dv_kms)

# get Gaussian field
delta = mock.get_gaussian_field(z_c,N2,dv_kms)
var_delta = np.var(delta)
print('mean delta =', np.mean(delta))
print('var delta =', var_delta)
plt.plot(z,delta)
plt.xlabel('z')
plt.ylabel('Gaussian field')
plt.show()

# from Gaussian field to lognormal density
density = mock.get_density(z_c,var_delta,z,delta)
print('mean density =', np.mean(density))
print('var density =', np.var(density))
plt.semilogy(z,density)
plt.xlabel('z')
plt.ylabel('density')
plt.show()

# from lognormal density to optical depth
tau = mock.get_tau(z,density)
print('mean tau =', np.mean(tau))
print('var tau =', np.var(tau))
plt.semilogy(z,tau)
plt.xlabel('z')
plt.ylabel('optical depth')
plt.show()

# from optical depth to flux
flux = mock.get_flux(z_c,tau)
print('mean flux =', np.mean(flux))
print('var flux =', np.var(flux))
plt.plot(z,flux)
plt.xlabel('z')
plt.ylabel('transmitted flux fraction')
plt.xlim(3.0,3.1)
plt.show()

