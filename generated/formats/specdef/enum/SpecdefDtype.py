from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class SpecdefDtype(UintEnum):
	Boolean = 0
	Int8 = 1
	Int16 = 2
	Int32 = 3
	Int64 = 4
	UInt8 = 5
	UInt16 = 6
	UInt32 = 7
	UInt64 = 8
	Float = 9
	String = 10
	Vector2 = 11
	Vector3 = 12
	Array = 13
	ChildItem = 14
	ReferenceToObject = 15
