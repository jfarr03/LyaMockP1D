import numpy as np
import matplotlib.pyplot as plt

# code to make mock Lya spectra following McDonald et al. (2006)
# copied from c++ code in Cosmology/LNLyaF


def power_amplitude(z):
  """function that affects the evolution of 1D power with z"""
  return 58.6*pow((1+z)/4.0,-2.82)

def tau_amplitude(z):
  """function that affects the evolution of the optical depth with z"""
  return 0.374*pow((1+z)/4.0,5.10)

def power_kms(z,k_kms,dv_kms=10.0,simple=False):
  # option for debugging
  if simple: return 100.0
  # power from McDonald et al. (2006)
  A = power_amplitude(z)
  k1 = 0.001
  n = 0.7
  R1 = 5.0
  # compute term without smoothing
  P = A * (1.0+pow(0.01/k1,n)) / (1.0+pow(k_kms/k1,n))
  # smooth with Gaussian and top hat
  kdv = np.fmax(k_kms*dv_kms,0.000001)
  P *= np.exp(-pow(k_kms*R1,2)) * pow(np.sin(kdv/2)/(kdv/2),2)
  return P

def get_density(z_c,var_delta,z,delta):
  tau_pl=2.0
  # relative amplitude 
  rel_amp = power_amplitude(z)/power_amplitude(z_c)
  return np.exp(tau_pl*(delta*np.sqrt(rel_amp)-0.5*var_delta*rel_amp))

def get_tau(z,density):
  A = tau_amplitude(z)
  return A*density

def get_flux(z_c,tau):
  return np.exp(-tau)

def get_redshifts(z_c,N2,dv_kms):
  """get redshift for each cell in the array"""
  N = np.power(2,N2)
  L_kms = N * dv_kms
  c_kms = 2.998e5
  if (L_kms > 4 * c_kms):
    print('Array is too long, approximations break down.')
    exit()
  # get indices
  i = range(N)
  z = (1+z_c)*pow(1-(i-N/2+1)*dv_kms/2.0/c_kms,-2)-1
  return z

def get_gaussian_field(z_c, N2, dv_kms, seed=666):
  # length of array
  N = np.power(2,N2)
  # number of Fourier modes
  NF=int(N/2+1)
  # setup random number generator
  gen = np.random.RandomState(seed)
  # generate random Fourier modes
  modes = np.empty(NF,dtype=complex)
  modes[:].real = gen.normal(size=NF)
  modes[1:-1].imag = gen.normal(size=NF-2)
  # get frequencies (wavenumbers in units of s/km)
  k_kms = np.fft.rfftfreq(N)*2*np.pi/dv_kms
  # normalize to desired power
  modes[-1:1].real *= np.sqrt(power_kms(z_c,k_kms[-1:1]))
  modes[-1:1].imag = 0
  modes[1:-1].real *= np.sqrt(0.5*power_kms(z_c,k_kms[1:-1]))
  modes[1:-1].imag *= np.sqrt(0.5*power_kms(z_c,k_kms[1:-1]))
  # inverse FFT to get (normalized) delta field
  delta = np.fft.irfft(modes) * np.sqrt(N/dv_kms)
  return delta


# central redshift
z_c = 3.0
# number of cells (power of two)
N2 = 15
# cell width (in km/s)
dv_kms=10
# get redshift for each cell
z = get_redshifts(z_c,N2,dv_kms)

# get Gaussian field
delta = get_gaussian_field(z_c,N2,dv_kms)
var_delta = np.var(delta)
print('mean delta =', np.mean(delta))
print('var delta =', var_delta)
plt.plot(z,delta)
plt.xlabel('z')
plt.ylabel('Gaussian field')
plt.show()

# from Gaussian field to lognormal density
density = get_density(z_c,var_delta,z,delta)
print('mean density =', np.mean(density))
print('var density =', np.var(density))
plt.semilogy(z,density)
plt.xlabel('z')
plt.ylabel('density')
plt.show()

# from lognormal density to optical depth
tau = get_tau(z,density)
print('mean tau =', np.mean(tau))
print('var tau =', np.var(tau))
plt.semilogy(z,tau)
plt.xlabel('z')
plt.ylabel('optical depth')
plt.show()

# from optical depth to flux
flux = get_flux(z_c,tau)
print('mean flux =', np.mean(flux))
print('var flux =', np.var(flux))
plt.plot(z,flux)
plt.xlabel('z')
plt.ylabel('transmitted flux fraction')
plt.xlim(3.0,3.1)
plt.show()


