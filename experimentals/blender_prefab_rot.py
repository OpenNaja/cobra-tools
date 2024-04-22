import numpy as np
import math

stra = """		RF_Spiders_Arboreal_Web_Base_Resting_Point_[N] = {
			Components = {
				ExhibitRestingPoint = {
					ValidPosePrefabs = {
						'GoldenOrbWeaverSpiders_Pose_01'
					}
				},
				Transform = {
					Rotation = vec3_const([R]),
					Position = vec3_const([P]),
					Scale = 1.0,
				}
			}
		},
"""


output = []
num = 9
extent_x = 180
# num = 5
# extent_x = 90
x_angles = np.linspace(-extent_x, extent_x, num)
x_pos = np.linspace(0, 1, num)
for r_x, p_x in zip(x_angles, x_pos):
	p = (-1.575462, p_x, 1.931068)
	r = (math.radians(r_x), 0, 0)
	prefab = stra.replace("[N]", str(len(output))).replace(
		"[R]", f"{r[0]:.2f}, {r[1]:.2f}, {r[2]:.2f}").replace(
		"[P]", f"{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}")
	output.append(prefab)

x_angles = np.linspace(-extent_x, extent_x, num)
x_pos = np.linspace(0, 1, num)
for r_x, p_x in zip(x_angles, x_pos):
	p = (-1.3, p_x, 1.931068)
	r = (0, math.radians(r_x), 0)
	prefab = stra.replace("[N]", str(len(output))).replace(
		"[R]", f"{r[0]:.2f}, {r[1]:.2f}, {r[2]:.2f}").replace(
		"[P]", f"{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}")
	output.append(prefab)

for r_x, p_x in zip(x_angles, x_pos):
	p = (-1.1, p_x, 1.931068)
	r = (0, 0, math.radians(r_x))
	prefab = stra.replace("[N]", str(len(output))).replace(
		"[R]", f"{r[0]:.2f}, {r[1]:.2f}, {r[2]:.2f}").replace(
		"[P]", f"{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}")
	output.append(prefab)

for r_x, p_x in zip(x_angles, x_pos):
	p = (-0.9, p_x, 1.931068)
	# r = (math.radians(45), 0, math.radians(r_x))
	r = (math.radians(45), math.radians(r_x), math.radians(45))
	prefab = stra.replace("[N]", str(len(output))).replace(
		"[R]", f"{r[0]:.2f}, {r[1]:.2f}, {r[2]:.2f}").replace(
		"[P]", f"{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}")
	output.append(prefab)


res = "".join(output)
print(res)

