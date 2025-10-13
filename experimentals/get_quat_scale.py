import contextlib
import math
import struct

import numpy as np

from source.formats.manis import get_quat_scale_fac


def f_as_i(f):
    return np.int32(struct.unpack('<i', struct.pack('<f', f))[0])


def i_as_f(f):
    return np.float32(struct.unpack('<f', struct.pack('<i', f))[0])


@contextlib.contextmanager
def as_int(f):
    i = f_as_i(f)
    yield i
    return i_as_f(i)


def get_quat_scale_fac_asm(norm_half_abs):
    # pointless, as norm is already squared
    # norm_half_abs = abs(norm_half_abs)
    # logging.info(f"half_norm {norm_half_abs}")
    # fVar3 = norm_half_abs * 0.6366197 + 8388608.0
    # masked_8388609 = f_as_i(8388609.0) & f_as_i(fVar3)
    # matches_8388609 = -int(i_as_f(masked_8388609) == 8388609.0)
    # logging.info(f"matches_8388609 {matches_8388609}")
    # fVar4 = fVar3 - 8388608.0
    # logging.info(f"fVar4 {fVar4}")
    # uVar7 = 0 & -(i_as_f(f_as_i(fVar3) & f_as_i(8388610.0)) == 8388610.0)
    # fVar4 = ((norm_half_abs - fVar4 * 1.570313) - fVar4 * 0.0004837513 - fVar4 * 7.54979e-08)# ^ (0 & uVar8)
    # fVar4_squared = fVar4 * fVar4
    # fVar5 = (((0.000024433157 * fVar4_squared + -0.001388732) * fVar4_squared + 0.04166665) * fVar4_squared - 0.5) * fVar4_squared + 1.0
    # fVar4 = ((fVar4_squared * -0.000195153 + 0.008332161) * fVar4_squared + -0.1666666) * fVar4_squared * fVar4 + fVar4
    # scale = (f_as_i(fVar5) & matches_8388609 | f_as_i(fVar4) & ~matches_8388609) ^ uVar7
    # res = np.array(1.0, dtype=np.float32) & np.array(-1, dtype=np.int32)
    # print(res)
    # fVar6 = abs(norm_half_abs)
    # fVar3 = fVar6 * 0.6366197 + 8388608.0
    # uVar4 = f_as_i(8388609.0) & f_as_i(fVar3)
    # uVar8 = -int(i_as_f(uVar4) == 8388609.0)
    # fVar4 = fVar3 - 8388608.0
    # uVar6 = 0.0
    # uVar7 = (uint)uVar6 & -(uint)((float)((uint)fVar3 & f_as_i(8388610.0)) == 8388610.0)
    # uVar9 = 0.000024433157
    # xmm0 = np.float32(1.0)
    # # xmm0 = 2.0
    # print(xmm0, type(xmm0))
    # raise AttributeError

    xmm2 = np.float32(8388608.0)  # 00 00 00 4B
    xmm0 = np.float32(8388609.0)  # 01 00 00 4B
    xmm1 = np.float32(8388610.0)  # 02 00 00 4B
    # store new norm at ptr (used to have old norm)
    xmm3 = xmm1  # copy 8388610f to xmm3
    # store 1.0 vec4f at ptr (not sure what it does)
    xmm7 = xmm0  # copy 8388609f
    # store 0 0 0 0 0 16383 6.10389e-005 16383 at ptr (not sure why)
    xmm8 = np.float32(norm_half_abs)  # move halfnorm to xmm8 from ptr
    xmm6 = xmm8  # copy halfnorm from xmm8 to xmm6
    xmm6 = np.abs(xmm6)  # take abs of xmm6 (copy of halfnorm)
    xmm4 = xmm6  # copy abs halfnorm to xmm4
    xmm4 *= np.float32(0.6366197)  # halfnorm
    xmm4 += xmm2  # halfnorm + 8388608f
    xmm3 = i_as_f(f_as_i(xmm3) & f_as_i(xmm4))  # mask xmm3 (...10f) with xmm4 (halfnorm+...8f)
    xmm7 = i_as_f(f_as_i(xmm7) & f_as_i(xmm4))  # mask xmm7 (...9f) with xmm4 (halfnorm+...8f)
    xmm3 = xmm3 == xmm1  # compare equality of masked and ..10f -> xmm3 = 0
    xmm7 = xmm7 == xmm0  # compare equality of masked and ..9f -> xmm7 = -1 or 0
    # xmm3 = i_as_f(-1 if xmm3 else 0)
    # xmm7 = i_as_f(-1 if xmm7 else 0)
    # xmm3 = 2147483647 if xmm3 else 0
    # xmm7 = 2147483647 if xmm7 else 0
    # print(bin(xmm3))
    # print(bin(xmm7))
    xmm4 -= xmm2  # halfnorm - (..8f)  = 1 or 0
    xmm2 = xmm7
    xmm0 = xmm4
    xmm1 = xmm4
    xmm0 *= np.float32(1.570313)
    xmm4 *= np.float32(7.54979e-08)
    xmm1 *= np.float32(0.0004837513)
    xmm6 -= xmm0  # halfnorm -xmm0
    xmm6 -= xmm1  # halfnorm -= xmm1
    xmm1 = np.float32(-0.0)  # copy -0.0 to xmm1
    xmm0 = xmm1
    xmm5 = xmm1
    xmm5 = xmm5 if xmm3 else 0.0
    xmm0 = xmm0 if xmm7 else 0.0
    # xmm5 = i_as_f(f_as_i(xmm5) & xmm3)
    # xmm0 = i_as_f(f_as_i(xmm0) & xmm7)
    xmm3 = np.float32(-0.000195153)  # copy to xmm3
    xmm8 = i_as_f(f_as_i(xmm8) & f_as_i(xmm1))
    xmm1 = xmm7
    xmm6 = i_as_f(f_as_i(xmm6) ^ f_as_i(xmm5))
    xmm6 -= xmm4
    xmm4 = np.float32(2.44332e-005)  # copy from ptr
    xmm6 = i_as_f(f_as_i(xmm6) ^ f_as_i(xmm0))
    xmm0 = xmm6
    xmm0 *= xmm6
    xmm4 *= xmm0
    xmm3 *= xmm0
    xmm4 += np.float32(-0.001388732)
    xmm3 += np.float32(0.008332161)
    xmm4 *= xmm0
    xmm3 *= xmm0
    xmm4 += np.float32(0.04166665)
    xmm3 += np.float32(-0.1666666)
    xmm4 *= xmm0
    xmm4 -= np.float32(0.5)
    xmm4 *= xmm0
    xmm0 *= xmm6
    xmm4 += np.float32(1.0)
    xmm3 *= xmm0

    # changed # xmm1 = i_as_f(~f_as_i(xmm1) & f_as_i(xmm4))  # slight change here
    xmm1 = 0.0 if xmm1 else xmm4
    xmm0 = xmm4
    xmm3 += xmm6
    # changed  # i_as_f(f_as_i(xmm0) & f_as_i(xmm7))
    xmm0 = xmm0 if xmm7 else 0.0
    # get new norm again
    # xmm2 = i_as_f(~f_as_i(xmm2) & f_as_i(xmm3))
    xmm2 = 0.0 if xmm2 else xmm3
    # changed  #  i_as_f(f_as_i(xmm3) & f_as_i(xmm7))
    xmm3 = xmm3 if xmm7 else 0.0
    # get 1.0 float again
    xmm1 = i_as_f(f_as_i(xmm1) | f_as_i(xmm3))
    xmm0 = i_as_f(f_as_i(xmm0) | f_as_i(xmm2))
    xmm1 = i_as_f(f_as_i(xmm1) ^ f_as_i(xmm5))  # xmm1[0] is q
    xmm0 = i_as_f(f_as_i(xmm0) ^ f_as_i(xmm8))  # xmm0 is scale_fac
    return xmm1, xmm0


def test_get_scale_fac():
    inp = np.arange(0, 4 * math.pi, math.pi*0.0001)
    # inp = np.arange(3.92, 3.93, math.pi*0.00001)
    q_data = np.zeros(len(inp))
    s_data = np.zeros(len(inp))
    q2_data = np.zeros(len(inp))
    s2_data = np.zeros(len(inp))
    for i, x in enumerate(inp):
        q_data[i], s_data[i] = get_quat_scale_fac_asm(x)
        q2_data[i], s2_data[i] = get_quat_scale_fac(x)
    assert np.allclose(q_data, q2_data, rtol=1e-03, atol=1e-05, equal_nan=False)
    assert np.allclose(s_data, s2_data, rtol=1e-03, atol=1e-05, equal_nan=False)
    import matplotlib.pyplot as plt
    plt.plot(inp, q_data, label="Q")
    plt.plot(inp, s_data, label="S")
    plt.plot(inp, q2_data, label="Q2", linestyle='-.')
    plt.plot(inp, s2_data, label="S2", linestyle='-.')
    plt.xlabel('Input')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
