""" Oslo Python Package for VASP """

from sys import version_info
ver = version_info[0]*10 + version_info[1]
if ver < 26:
    raise Exception("oppvasp requires python version 2.6 or higher")


import numpy as np
import time

# INCOMPLETE TABLE!
# vdw is van der Waals radius
# masses in g/mol
elements = {
  1 : { 'mass' : 1.0079,  'name': 'Hydrogen',   'symb': 'H',  'vdw': 1.20 },
  2 : { 'mass' : 4.0026,  'name': 'Helium',     'symb': 'He', 'vdw': 1.40 }, 
  3 : { 'mass' : 6.941,   'name': 'Lithium',    'symb': 'Li', 'vdw': 1.82 }, 
  4 : { 'mass' : 9.0122,  'name': 'Beryllium',  'symb': 'Be', 'vdw': 1.53 }, 
  5 : { 'mass' : 10.811,  'name': 'Boron',      'symb': 'B',  'vdw': 1.92 }, 
  6 : { 'mass' : 12.0107, 'name': 'Carbon',     'symb': 'C',  'vdw': 1.70 }, 
  7 : { 'mass' : 14.0067, 'name': 'Nitrogen',   'symb': 'N',  'vdw': 1.55 }, 
  8 : { 'mass' : 15.9994, 'name': 'Oxygen',     'symb': 'O',  'vdw': 1.52 }, 
  9 : { 'mass' : 18.9984, 'name': 'Fluorine',   'symb': 'F',  'vdw': 1.47 }, 
 10 : { 'mass' : 20.1797, 'name': 'Neon',       'symb': 'Ne', 'vdw': 1.54 }, 
 11 : { 'mass' : 22.9897, 'name': 'Sodium',     'symb': 'Na', 'vdw': 2.27 }, 
 12 : { 'mass' : 24.305,  'name': 'Magnesium',  'symb': 'Mg', 'vdw': 1.73 }, 
 13 : { 'mass' : 26.9815, 'name': 'Aluminum',   'symb': 'Al', 'vdw': 1.84 }, 
 14 : { 'mass' : 28.0855, 'name': 'Silicon',    'symb': 'Si', 'vdw': 2.10 }, 
 15 : { 'mass' : 30.9738, 'name': 'Phosphorus', 'symb': 'P',  'vdw': 1.80 }, 
 16 : { 'mass' : 32.065,  'name': 'Sulfur',     'symb': 'S',  'vdw': 1.80 }, 
 17 : { 'mass' : 35.453,  'name': 'Chlorine',   'symb': 'Cl', 'vdw': 1.75 }, 
 18 : { 'mass' : 39.948,  'name': 'Argon',      'symb': 'Ar', 'vdw': 1.88 }, 
 19 : { 'mass' : 39.0983, 'name': 'Potassium',  'symb': 'K',  'vdw': 2.75 }, 
 20 : { 'mass' : 40.078,  'name': 'Calcium',    'symb': 'Ca', 'vdw': 2.31 }, 
 21 : { 'mass' : 44.9559, 'name': 'Scandium',   'symb': 'Sc', 'vdw': 2.11 }, 
 22 : { 'mass' : 47.867, 'name': 'Titanium', 'symb': 'Ti' }, 
 23 : { 'mass' : 50.9415, 'name': 'Vanadium', 'symb': 'V' }, 
 24 : { 'mass' : 51.9961, 'name': 'Chromium', 'symb': 'Cr' }, 
 25 : { 'mass' : 54.938, 'name': 'Manganese', 'symb': 'Mn' }, 
 26 : { 'mass' : 55.845, 'name': 'Iron', 'symb': 'Fe' }, 
 27 : { 'mass' : 58.9332, 'name': 'Cobalt', 'symb': 'Co' }, 
 28 : { 'mass' : 58.6934, 'name': 'Nickel', 'symb': 'Ni' }, 
 29 : { 'mass' : 63.546, 'name': 'Copper', 'symb': 'Cu' }, 
 30 : { 'mass' : 65.39, 'name': 'Zinc', 'symb': 'Zn' }, 
 31 : { 'mass' : 69.723, 'name': 'Gallium', 'symb': 'Ga' }, 
 32 : { 'mass' : 72.64, 'name': 'Germanium', 'symb': 'Ge' }, 
 33 : { 'mass' : 74.9216, 'name': 'Arsenic', 'symb': 'As' }, 
 34 : { 'mass' : 78.96, 'name': 'Selenium', 'symb': 'Se' }, 
 35 : { 'mass' : 79.904, 'name': 'Bromine', 'symb': 'Br' }, 
 36 : { 'mass' : 83.8, 'name': 'Krypton', 'symb': 'Kr' }, 
 37 : { 'mass' : 85.4678, 'name': 'Rubidium', 'symb': 'Rb' }, 
 38 : { 'mass' : 87.62, 'name': 'Strontium', 'symb': 'Sr' }, 
 39 : { 'mass' : 88.9059, 'name': 'Yttrium', 'symb': 'Y' }, 
 40 : { 'mass' : 91.224, 'name': 'Zirconium', 'symb': 'Zr' }, 
 41 : { 'mass' : 92.9064, 'name': 'Niobium', 'symb': 'Nb' }, 
 42 : { 'mass' : 95.94, 'name': 'Molybdenum', 'symb': 'Mo' }, 
 43 : { 'mass' : 98, 'name': 'Technetium', 'symb': 'Tc' }, 
 44 : { 'mass' : 101.07, 'name': 'Ruthenium', 'symb': 'Ru' }, 
 45 : { 'mass' : 102.9055, 'name': 'Rhodium', 'symb': 'Rh' }, 
 46 : { 'mass' : 106.42, 'name': 'Palladium', 'symb': 'Pd' }, 
 47 : { 'mass' : 107.8682, 'name': 'Silver', 'symb': 'Ag' }, 
 48 : { 'mass' : 112.411, 'name': 'Cadmium', 'symb': 'Cd' }, 
 49 : { 'mass' : 114.818, 'name': 'Indium', 'symb': 'In' }, 
 50 : { 'mass' : 118.71, 'name': 'Tin', 'symb': 'Sn' }, 
 51 : { 'mass' : 121.76, 'name': 'Antimony', 'symb': 'Sb' }, 
 52 : { 'mass' : 127.6, 'name': 'Tellurium', 'symb': 'Te' }, 
 53 : { 'mass' : 126.9045, 'name': 'Iodine', 'symb': 'I' }, 
 54 : { 'mass' : 131.293, 'name': 'Xenon', 'symb': 'Xe' }, 
 55 : { 'mass' : 132.9055, 'name': 'Cesium', 'symb': 'Cs' }, 
 56 : { 'mass' : 137.327, 'name': 'Barium', 'symb': 'Ba' }, 
 57 : { 'mass' : 138.9055, 'name': 'Lanthanum', 'symb': 'La' }, 
 58 : { 'mass' : 140.116, 'name': 'Cerium', 'symb': 'Ce' }, 
 59 : { 'mass' : 140.9077, 'name': 'Praseodymium', 'symb': 'Pr' }, 
 60 : { 'mass' : 144.24, 'name': 'Neodymium', 'symb': 'Nd' }, 
 61 : { 'mass' : 145, 'name': 'Promethium', 'symb': 'Pm' }, 
 62 : { 'mass' : 150.36, 'name': 'Samarium', 'symb': 'Sm' }, 
 63 : { 'mass' : 151.964, 'name': 'Europium', 'symb': 'Eu' }, 
 64 : { 'mass' : 157.25, 'name': 'Gadolinium', 'symb': 'Gd' }, 
 65 : { 'mass' : 158.9253, 'name': 'Terbium', 'symb': 'Tb' }, 
 66 : { 'mass' : 162.5, 'name': 'Dysprosium', 'symb': 'Dy' }, 
 67 : { 'mass' : 164.9303, 'name': 'Holmium', 'symb': 'Ho' }, 
 68 : { 'mass' : 167.259, 'name': 'Erbium', 'symb': 'Er' }, 
 69 : { 'mass' : 168.9342, 'name': 'Thulium', 'symb': 'Tm' }, 
 70 : { 'mass' : 173.04, 'name': 'Ytterbium', 'symb': 'Yb' }, 
 71 : { 'mass' : 174.967, 'name': 'Lutetium', 'symb': 'Lu' }, 
 72 : { 'mass' : 178.49, 'name': 'Hafnium', 'symb': 'Hf' }, 
 73 : { 'mass' : 180.9479, 'name': 'Tantalum', 'symb': 'Ta' }, 
 74 : { 'mass' : 183.84, 'name': 'Tungsten', 'symb': 'W' }, 
 75 : { 'mass' : 186.207, 'name': 'Rhenium', 'symb': 'Re' }, 
 76 : { 'mass' : 190.23, 'name': 'Osmium', 'symb': 'Os' }, 
 77 : { 'mass' : 192.217, 'name': 'Iridium', 'symb': 'Ir' }, 
 78 : { 'mass' : 195.078, 'name': 'Platinum', 'symb': 'Pt' }, 
 79 : { 'mass' : 196.9665, 'name': 'Gold', 'symb': 'Au' }, 
 80 : { 'mass' : 200.59, 'name': 'Mercury', 'symb': 'Hg' }, 
 81 : { 'mass' : 204.3833, 'name': 'Thallium', 'symb': 'Tl' }, 
 82 : { 'mass' : 207.2, 'name': 'Lead', 'symb': 'Pb' }, 
 83 : { 'mass' : 208.9804, 'name': 'Bismuth', 'symb': 'Bi' }, 
 84 : { 'mass' : 209, 'name': 'Polonium', 'symb': 'Po' }, 
 85 : { 'mass' : 210, 'name': 'Astatine', 'symb': 'At' }, 
 86 : { 'mass' : 222, 'name': 'Radon', 'symb': 'Rn' }, 
 87 : { 'mass' : 223, 'name': 'Francium', 'symb': 'Fr' }, 
 88 : { 'mass' : 226, 'name': 'Radium', 'symb': 'Ra' }, 
 89 : { 'mass' : 227, 'name': 'Actinium', 'symb': 'Ac' }, 
 90 : { 'mass' : 232.0381, 'name': 'Thorium', 'symb': 'Th' }, 
 91 : { 'mass' : 231.0359, 'name': 'Protactinium', 'symb': 'Pa' }, 
 92 : { 'mass' : 238.0289, 'name': 'Uranium', 'symb': 'U' }, 
 93 : { 'mass' : 237, 'name': 'Neptunium', 'symb': 'Np' }, 
 94 : { 'mass' : 244, 'name': 'Plutonium', 'symb': 'Pu' }, 
 95 : { 'mass' : 243, 'name': 'Americium', 'symb': 'Am' }, 
 96 : { 'mass' : 247, 'name': 'Curium', 'symb': 'Cm' }, 
 97 : { 'mass' : 247, 'name': 'Berkelium', 'symb': 'Bk' }, 
 98 : { 'mass' : 251, 'name': 'Californium', 'symb': 'Cf' }, 
 99 : { 'mass' : 252, 'name': 'Einsteinium', 'symb': 'Es' }, 
 100 : { 'mass' : 257, 'name': 'Fermium', 'symb': 'Fm' }, 
 101 : { 'mass' : 258, 'name': 'Mendelevium', 'symb': 'Md' }, 
 102 : { 'mass' : 259, 'name': 'Nobelium', 'symb': 'No' }, 
 103 : { 'mass' : 262, 'name': 'Lawrencium', 'symb': 'Lr' }, 
 104 : { 'mass' : 261, 'name': 'Rutherfordium', 'symb': 'Rf' }, 
 105 : { 'mass' : 262, 'name': 'Dubnium', 'symb': 'Db' }, 
 106 : { 'mass' : 266, 'name': 'Seaborgium', 'symb': 'Sg' }, 
 107 : { 'mass' : 264, 'name': 'Bohrium', 'symb': 'Bh' }, 
 108 : { 'mass' : 277, 'name': 'Hassium', 'symb': 'Hs' }, 
 109 : { 'mass' : 268, 'name': 'Meitnerium', 'symb': 'Mt' }
}

def get_atomic_number_from_symbol(atomic_symbol):
    """
    returns the atomic number corresponding to a given atomic symbol
    """
    symb = atomic_symbol.strip() # trim
    for k,v in elements.items():
        if v['symb'] == symb:
            return k
    print "Warning: Atomic symbol '%s' not found!" % (symb)
    return -1

def direct_to_cartesian(positions, basis):
    """
    Converts positions in direct coordinates into cartesian coordinates using a given basis.

    Parameters
    ----------
    positions : num_steps x num_atoms x 3 numpy array
        Array containing the direct coordinates of num_atoms atoms for num_steps steps
    basis : num_steps x 3 x 3 numpy array
        Array containg the lattice vectors in Cartesian coordinates

    """
    if positions == None:
        return None
    #print "converting to cartesian basis..."
    t1 = time.clock()
    
    # Alternative 1
    #pos = np.array([np.dot(p,b) for p,b in zip(positions, basis)]) # there is surely some faster way!

    if basis.ndim == 3:
        # time-dependent basis
    
        # Alternative 2 is about 10 times faster than alternative 1
        pos = np.zeros(positions.shape)
        if pos.ndim == 2 or pos.ndim == 3:
            i = 0
            for p,b in zip(positions,basis):
                pos[i] = np.dot(p,b)
                i += 1
        #elif pos.ndim == 2:
            # single coordinate set
            # for some reason, this is really slow:
            #   pos = np.dot(positions, basis)

        else:
            raise StandardError("positions is of wrong dimensions")
    
    else:

        if np.allclose(basis[[0,0,1,1,2,2],[1,2,0,2,0,1]],np.zeros(6)):
            # orthorhombic
            if np.allclose(basis.diagonal(),np.tile(basis[0,0],3)):
                # cubic
                pos = positions * basis[0,0]
            else:
                print "not supported yet"
        else:
            print "not supported yet"

    
    # Alternative 3: if the cell is static (3 x 3 instead of nsteps x 3 x 3):
    # perhaps we can use tensordot anyway? I'm not sure.
    #pos = np.tensordot(positions, basis, axes=([2],[0]))
    
    tdiff = time.clock() - t1
    if tdiff > 1:
        print "Conversion to cartesian basis took",round(tdiff, 3),"seconds. This function should be optimized!"
    # We could make a Fortran module doing the conversion... 
    #for i in range(pos.shape[0]): # axis 0   : 4 
    #    pos3[i] = np.dot(pos[i],basis[i])
    #    for j in range(pos.shape[1]): # axis 1 : 5
    #        #pos2[i,j] = np.dot(pos[i,j],basis[i,j])
    #        for k in range(pos.shape[2]): # axis 2 : 3
    #            for l in range(pos.shape[2]): # axis 2 : 3
    #                pos2[i,j,k] += pos[i,j,l] * basis[i,l,k]
    return pos


def cartesian_to_direct(positions, basis):
    """
    Converts positions in cartesian coordinates into direct coordinates using a given basis.

    Parameters
    ----------
    positions : num_steps x num_atoms x 3 numpy array
        Array containing the cartesian coordinates of num_atoms atoms for num_steps steps
    basis : num_steps x 3 x 3 numpy array
        Array containg the lattice vectors in Cartesian coordinates

    """
    if positions == None:
        return None
    pos = np.zeros(positions.shape)
    i = 0
    inv_basis = np.linalg.inv(basis)
    
    if pos.ndim == 3:
        # trajectory
        for p,b in zip(positions, inv_basis):
            pos[i] = np.dot(p,b)
            i += 1
    elif pos.ndim == 2:
        # single coordinate set
        pos = np.dot(positions, inv_basis)
    else:
        raise StandardError("positions is of wrong dimensions")

    return pos