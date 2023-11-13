from generated.formats.ovl_base import OvlContext
from generated.formats.physmat.compounds.PhysmatRoot import PhysmatRoot

# PZ ms2
pz_classification_name = ['Animal', 'Animal_Bone', 'Animal_Box', 'Bedding', 'Building', 'Climbable', 'Coaster_Car', 'Enrichment_Object', 'Facility', 'Kinetic_Object', 'NoCollision', 'Prop', 'Scenery', 'Scenery_NoNavSource', 'Structure', 'Track', 'TreeBase', 'TreeBranch', 'TreeFoliage', 'TreeTrunk', 'UIElement']
pz_surface_name = ['Animal', 'Brick', 'Cloth', 'Concrete', 'Default', 'Default_Legacy_DO_NOT_USE', 'Dirt', 'Foliage', 'Glass', 'Grass', 'Ice', 'Leaves', 'Litter', 'Metal', 'Mud', 'Plastic', 'Poo', 'Rubber', 'Snow', 'Stone', 'Tree', 'Wood']

# JWE2 ms2
jwe2_classification_name = ['AIVehicle', 'AIVehicleObstacle', 'AviaryTourGate', 'Building', 'BuildingNoCameraObstacle', 'CameraObstacle', 'CarBody', 'CarObstacle', 'Debris', 'Default', 'Dinosaur', 'DinosaurNoFence', 'DinosaurNoVehicle', 'Drone', 'Foliage', 'Gate', 'GuestRagdoll', 'HatcheryGate', 'LagoonFloor', 'PaleoFoodPoint', 'Perch', 'PerchQuetz', 'Prop', 'PropNoCameraObstacle', 'TourGate', 'Vehicle']
jwe2_surface_name = ['BuildingBrick', 'BuildingConcrete', 'BuildingMetal', 'BuildingWood', 'CarBody', 'Debris', 'Default', 'DinosaurLimb', 'Drone', 'Gyrosphere', 'LagoonFloor', 'PaleoFoodPoint', 'PropMetal', 'PropPlastic', 'PropWooden', 'SceneryTree']

files = (
	("C:/Users/arnfi/Desktop/pz.physmat", pz_classification_name, pz_surface_name),
	("C:/Users/arnfi/Desktop/jwe2.physmat", jwe2_classification_name, jwe2_surface_name),
	("C:/Users/arnfi/Desktop/wh.physmat", (), ()))
for fp, classification, surface in files:
	with open(fp, "rb") as f:
		mat = PhysmatRoot.from_stream(f, OvlContext())
		print(mat)
		for s in ("all_surfaces", "surface_res", "classnames"):
			print("\n\n")
			print(s)
			names = []
			for ind, offset in enumerate(getattr(mat, f"{s}_names")):
				lut = None
				if s in ("surface_res", "classnames"):
					lut = getattr(mat, f"{s}_indices")[ind]
				else:
					lut = f'{bin(getattr(mat, f"all_surfaces_flags")[ind])[2:]:>64s}'
				name = mat.names.get_str_at(offset)
				print(f'{ind:>3d}', lut, name)
				names.append(name)
			print(sorted(names))
		print()
		print(classification)
		print(surface)
