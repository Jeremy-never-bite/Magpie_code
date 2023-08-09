import numpy as np
def cal_c_a_ratio(satellite_coordinate):
    n = len(satellite_coordinate)
    I = np.zeros([3,3])
    for i in range(3):
        for j in range(3):
            for k in range(n):
                I[i][j] = I[i][j] + satellite_coordinate[k][i]*satellite_coordinate[k][j]
    # print(I)
    eigenvalue, featurevector = np.linalg.eig(I)
    # print("eigenvalue:", eigenvalue)
    # print("featurevector:", featurevector)
    c = min(eigenvalue)**0.5
    a = max(eigenvalue)**0.5
    rng=range(len(eigenvalue))
    mindex=min(rng,key=lambda x:eigenvalue[x])
    c_a_minor = featurevector[:,mindex]
    # print("c/a=", c/a)
    return c/a, c_a_minor

def cal_alpha(L, N = 8):
    maxn = len(L)
    for i in range(maxn):
        L[i] = L[i]/np.linalg.norm(L[i])
    npoints = 10000
    Vec_ran = np.zeros((npoints, 3))
    dlong = np.pi*(3-5**0.5)
    dz = 2.0/npoints
    long = 0.
    z = 1-dz/2
    for k in range(npoints):
        r = (1-z*z)**0.5
        Vec_ran[k] = [np.cos(long)*r, np.sin(long)*r, z]
        z = z - dz
        long = long + dlong
    direction = Vec_ran
    alpha = 90
    re = 0
    for i in range(npoints):
        angle = np.zeros(maxn)
        for j in range (maxn):
            angle[j] = np.rad2deg(np.arccos(abs(np.dot(direction[i], L[j]))))
        angle.sort()
        if angle[N -1] < alpha:
            alpha = angle[N-1]
            re = i
    alpha_axis = direction[re]
    return alpha, alpha_axis


def cal_angle(e1,e2):
    return np.arccos(abs(np.dot(e1,e2)))*180/np.pi



def read_central_r200(simulation_name):
    simulation_num = int(simulation_name[1])
    if simulation_name[3:] == 'zcut7':
        if simulation_num == 4:
            centerIndex = 2
        elif simulation_num == 5:
            centerIndex = 2
        else:
            centerIndex = 1
    elif simulation_name[3:] == '7DM_GAS':
        if simulation_num == 2:
            centerIndex = 2
        elif simulation_num == 4:
            centerIndex = 3
        else:
            centerIndex = 1
    h = 0.6777
    mw_stellar, mw_snap, mw_groupnum, mw_subgroupnum, mw_subpos, mw_redshift, mw_halo = \
                find_main_branch_stellar_new(199, centerIndex, 0)
    snap = mw_snap
    groupnum = mw_groupnum
    r200 = []
    # m200 = []

    filedir = '/Simulations/Magpie/' + simulation_name 
    filename = os.listdir(filedir)
    filename_group = [name for name in filename if name[:6]=='groups' and name[-3:]!='tar']
    Num = np.array([int(filename[7:10]) for filename in filename_group])
    for i in snap[::-1]:
        print(i)
        j = np.where(Num==i)[0][0]
        filedir_group = filedir + '/' + filename_group[j]
        filenamelist_all_group = os.listdir(filedir_group)
        filenamelist_group = [filenamelist_all_group[i] for i in range(len(filenamelist_all_group))\
                            if filenamelist_all_group[i].split('.')[0][:17] == 'eagle_subfind_tab' ]
        R200 = []
        # M200 = []
        for k in range(len(filenamelist_group)):
            filedata_group = h5py.File(filedir_group + '/' + filenamelist_group[k][:30] + '.%0.f.hdf5' % k, 'r')
            catalog = list(filedata_group['FOF'].keys())
            if 'Group_R_Crit200' in catalog:
                R200 += list(filedata_group['FOF/Group_R_Crit200'])
                # M200 += list(filedata_group['FOF/Group_M_Crit200'])
        R200 = np.vstack(R200)
        # M200 = np.vstack(M200)
        if len(R200) < groupnum[snap==i]-1:
            r200.append(np.array([[0]]))
        else:
            r200.append(R200[groupnum[snap==i]-1])
        # m200.append(M200[groupnum[snap==i]-1])
    mw_r200 = np.array([r200[i][0][0] for i in range(len(r200))])[::-1]    # cMpc/h
    mw_r200_phy = mw_r200 * 1/(1+mw_redshift) * 1000 / h   
    return mw_r200_phy[1:][::-1]


def cal_rms(pos):
    rms_min = 300
    # generate 10000 direction
    npoints = 10000
    Vec_ran = np.zeros((npoints, 3))
    dlong = np.pi*(3-5**0.5)
    dz = 2.0/npoints
    long = 0.
    z = 1-dz/2
    for k in range(npoints):
        r = (1-z*z)**0.5
        Vec_ran[k] = [np.cos(long)*r, np.sin(long)*r, z]
        z = z - dz
        long = long + dlong
    direction = Vec_ran
    # for each direction, calculate rms, find the rms_min

    point = np.array([0, 0, 0])  # 平面上的一点
    satellite_num = len(pos)
    for j in range(len(direction)):
        distances = []
        for i in range(satellite_num):
            distances.append(abs(np.dot(direction[j], pos[i] - point)))
        rms = 0
        for i in range(satellite_num):
            rms += distances[i]**2
        rms = (rms/satellite_num)**0.5
        if rms < rms_min:
            rms_min = rms
    return rms_min