from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UshortEnum


class SubCurveType(UshortEnum):
	Constant = 0
	Linear = 1
	Polynomial = 2
	Exponential = 3
	SCurve = 4
	Bezier = 5
