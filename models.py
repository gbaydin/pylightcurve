from tasks import *
pi = np.pi

gauss30 = [
    [0.1028526528935588, -0.0514718425553177],
    [0.1028526528935588, 0.0514718425553177],
    [0.1017623897484055, -0.1538699136085835],
    [0.1017623897484055, 0.1538699136085835],
    [0.0995934205867953, -0.2546369261678899],
    [0.0995934205867953, 0.2546369261678899],
    [0.0963687371746443, -0.3527047255308781],
    [0.0963687371746443, 0.3527047255308781],
    [0.0921225222377861, -0.4470337695380892],
    [0.0921225222377861, 0.4470337695380892],
    [0.0868997872010830, -0.5366241481420199],
    [0.0868997872010830, 0.5366241481420199],
    [0.0807558952294202, -0.6205261829892429],
    [0.0807558952294202, 0.6205261829892429],
    [0.0737559747377052, -0.6978504947933158],
    [0.0737559747377052, 0.6978504947933158],
    [0.0659742298821805, -0.7677774321048262],
    [0.0659742298821805, 0.7677774321048262],
    [0.0574931562176191, -0.8295657623827684],
    [0.0574931562176191, 0.8295657623827684],
    [0.0484026728305941, -0.8825605357920527],
    [0.0484026728305941, 0.8825605357920527],
    [0.0387991925696271, -0.9262000474292743],
    [0.0387991925696271, 0.9262000474292743],
    [0.0287847078833234, -0.9600218649683075],
    [0.0287847078833234, 0.9600218649683075],
    [0.0184664683110910, -0.9836681232797472],
    [0.0184664683110910, 0.9836681232797472],
    [0.0079681924961666, -0.9968934840746495],
    [0.0079681924961666, 0.9968934840746495]
]

gauss30 = np.swapaxes(gauss30, 0, 1)


def integral_r(a1, a2, a3, a4, r):
    a0 = 1.0 - a1 - a2 - a3 - a4
    rr = (1.0 - r ** 2) ** (1.0 / 4)
    aa4 = - (2.0 / 4) * a0 * (rr ** 4.0)
    aa5 = - (2.0 / 5) * a1 * (rr ** 5.0)
    aa6 = - (2.0 / 6) * a2 * (rr ** 6.0)
    aa7 = - (2.0 / 7) * a3 * (rr ** 7.0)
    aa8 = - (2.0 / 8) * a4 * (rr ** 8.0)
    return aa4 + aa5 + aa6 + aa7 + aa8


def num(r, a1, a2, a3, a4, p, z):
    arccos = (-p ** 2 + z ** 2 + r ** 2) / (2.0 * z * r)
    arccos = np.where(arccos > 1, 1, arccos)
    return (1.0 - a1 * (1.0 - (1.0 - r ** 2) ** (1.0 / 4)) - a2 * (1.0 - (1.0 - r ** 2) ** (1.0 / 2))
            - a3 * (1.0 - (1.0 - r ** 2) ** (3.0 / 4)) - a4 * (1.0 - (1.0 - r ** 2))) * r * np.arccos(arccos)


def integral_r_f(a1, a2, a3, a4, p, z, r1, r2):
    gauss = gauss30
    r1 = np.clip(r1, 0, 1)
    r2 = np.clip(r2, 0, 1)
    x1 = (r2 - r1) / 2
    x2 = (r2 + r1) / 2
    x1, l = np.meshgrid(x1, gauss[1])
    x2, w = np.meshgrid(x2, gauss[0])
    result = np.sum(w * num(x1 * l + x2, a1, a2, a3, a4, p, z), 0)
    return ((r2 - r1) / 2) * result


def integral_centred(a1, a2, a3, a4, p, ww1, ww2):
    w1 = np.minimum(ww1, ww2)
    w2 = np.maximum(ww1, ww2)
    final = (integral_r(a1, a2, a3, a4, p) - integral_r(a1, a2, a3, a4, 0.0)) * (w2 - w1)
    return final


def integral_plus_core(a1, a2, a3, a4, p, z, ww1, ww2):
    if len(z) == 0:
        return []
    rr1 = z * np.cos(ww1) + np.sqrt(np.maximum(p ** 2 - (z * np.sin(ww1)) ** 2, 0))
    rr1 = np.clip(rr1, 0, 1)
    rr2 = z * np.cos(ww2) + np.sqrt(np.maximum(p ** 2 - (z * np.sin(ww2)) ** 2, 0))
    rr2 = np.clip(rr2, 0, 1)
    w1 = np.minimum(ww1, ww2)
    r1 = np.minimum(rr1, rr2)
    w2 = np.maximum(ww1, ww2)
    r2 = np.maximum(rr1, rr2)
    parta = integral_r(a1, a2, a3, a4, 0.0) * (w1 - w2)
    partb = integral_r(a1, a2, a3, a4, r1) * w2
    partc = integral_r(a1, a2, a3, a4, r2) * (-w1)
    partd = integral_r_f(a1, a2, a3, a4, p, z, r1, r2)
    final = parta + partb + partc + partd
    return final


def integral_plus(a1, a2, a3, a4, p, z, ww1, ww2):
    split = np.where(ww1 * ww2 < 0)
    if len(split[0]) == 0:
        intplus = integral_plus_core(a1, a2, a3, a4, p, z, np.abs(ww1), np.abs(ww2))
        return intplus
    else:
        w1 = np.minimum(ww1, ww2)
        w2 = np.maximum(ww1, ww2)
        intplus = integral_plus_core(a1, a2, a3, a4, p, z, np.where(w1 * w2 < 0, 0, np.abs(w1)), np.abs(w2))
        intplus[split] = intplus[split] + integral_plus_core(a1, a2, a3, a4, p, z[split], 0, np.abs(w1[split]))
        return intplus    


def integral_minus_core(a1, a2, a3, a4, p, z, ww1, ww2):
    if len(z) == 0:
        return []
    rr1 = z * np.cos(ww1) - np.sqrt(np.maximum(p ** 2 - (z * np.sin(ww1)) ** 2, 0))
    rr1 = np.clip(rr1, 0, 1)
    rr2 = z * np.cos(ww2) - np.sqrt(np.maximum(p ** 2 - (z * np.sin(ww2)) ** 2, 0))
    rr2 = np.clip(rr2, 0, 1)
    w1 = np.minimum(ww1, ww2)
    r1 = np.minimum(rr1, rr2)
    w2 = np.maximum(ww1, ww2)
    r2 = np.maximum(rr1, rr2)
    parta = integral_r(a1, a2, a3, a4, 0.0) * (w1 - w2)
    partb = integral_r(a1, a2, a3, a4, r1) * (-w1)
    partc = integral_r(a1, a2, a3, a4, r2) * w2
    partd = integral_r_f(a1, a2, a3, a4, p, z, r1, r2)
    final = parta + partb + partc - partd
    return final


def integral_minus(a1, a2, a3, a4, p, z, ww1, ww2):
    split = np.where(ww1 * ww2 < 0)
    if len(split[0]) == 0:
        intmins = integral_minus_core(a1, a2, a3, a4, p, z, np.abs(ww1), np.abs(ww2))
        return intmins
    else:
        w1 = np.minimum(ww1, ww2)
        w2 = np.maximum(ww1, ww2)
        intmins = integral_minus_core(a1, a2, a3, a4, p, z, np.where(w1 * w2 < 0, 0, np.abs(w1)), np.abs(w2))
        intmins[split] = intmins[split] + integral_minus_core(a1, a2, a3, a4, p, z[split], 0, np.abs(w1[split]))
        return intmins    


def single_model(ldcoeffs, r_ratio, xyz, tt):
    if len(tt) == 0:
        return np.array([])
    a1, a2, a3, a4 = ldcoeffs
    p = r_ratio
    # projected distance
    fx, fy, fz = xyz
    z = np.sqrt(fy ** 2 + fz ** 2)
    # cases
    case0 = np.where((fx > 0) & (z == 0) & (p <= 1))
    case1 = np.where((fx > 0) & (z < p) & (z + p <= 1))
    casea = np.where((fx > 0) & (z < p) & (z + p > 1) & (p - z < 1))
    caseb = np.where((fx > 0) & (z < p) & (z + p > 1) & (p - z > 1))
    case2 = np.where((fx > 0) & (z == p) & (z + p <= 1))
    casec = np.where((fx > 0) & (z == p) & (z + p > 1))
    case3 = np.where((fx > 0) & (z > p) & (z + p < 1))
    case4 = np.where((fx > 0) & (z > p) & (z + p == 1))
    case5 = np.where((fx > 0) & (z > p) & (z + p > 1) & (z ** 2 - p ** 2 < 1))
    case6 = np.where((fx > 0) & (z > p) & (z + p > 1) & (z ** 2 - p ** 2 == 1))
    case7 = np.where((fx > 0) & (z > p) & (z + p > 1) & (z ** 2 - p ** 2 > 1) & (z < 1 + p))
    plus_case = np.concatenate((case1[0], case2[0], case3[0], case4[0], case5[0], casea[0], casec[0]))
    minus_case = np.concatenate((case3[0], case4[0], case5[0], case6[0], case7[0]))
    star_case = np.concatenate((case5[0], case6[0], case7[0], casea[0], casec[0]))
    # cross points
    th = np.arcsin(np.where(p / z > 1.0, 1.0, p / z))
    arccos = np.clip((1.0 - p ** 2 + z ** 2) / (2.0 * z), -1, 1)
    ph = np.arccos(arccos)
    # flux_upper
    plusflux = np.zeros(len(z))
    theta_1 = np.zeros(len(z))
    theta_1[case5] = ph[case5]
    theta_1[casea] = ph[casea]
    theta_1[casec] = ph[casec]
    theta_2 = np.full_like(th, th)
    theta_2[case1] = pi
    theta_2[case2] = pi / 2.0
    theta_2[casea] = pi
    theta_2[casec] = pi / 2.0
    plusflux[plus_case] = integral_plus(a1, a2, a3, a4, p, z[plus_case], theta_1[plus_case], theta_2[plus_case])
    if len(case0[0]) > 0:
        plusflux[case0] = integral_centred(a1, a2, a3, a4, p, 0.0, pi)
    if len(caseb[0]) > 0:
        plusflux[caseb] = integral_centred(a1, a2, a3, a4, 1, 0.0, pi)
    # flux_lower
    minsflux = np.zeros(len(z))
    theta_2 = np.full_like(th, th)
    theta_2[case7] = ph[case7]
    minsflux[minus_case] = integral_minus(a1, a2, a3, a4, p, z[minus_case], 0.0, theta_2[minus_case])
    # flux_star
    starflux = np.zeros(len(z))
    starflux[star_case] = integral_centred(a1, a2, a3, a4, 1, 0.0, ph[star_case])
    # flux_final
    finalflux = 2.0 * (plusflux + starflux - minsflux)
    # return
    total_flux = integral_centred(a1, a2, a3, a4, 1, 0.0, 2.0 * pi)
    return 1 - finalflux / total_flux


def transit(ldcoeffs, rprs, p, a, e, i, w, ww, t0, tt):
    xyz = position(p, a, e, i * pi / 180, w * pi / 180, ww * pi / 180, t0, tt)
    return single_model(ldcoeffs, rprs, xyz, tt)


def eclipse(fpfs, rprs, p, a, e, i, w, ww, t0, tt):
    xyz = position(p, -a / rprs, e, i * pi / 180, w * pi / 180, ww * pi / 180, t0, tt)
    return (1.0 + fpfs * single_model((0, 0, 0, 0), 1 / rprs, xyz, tt)) / (1.0 + fpfs)