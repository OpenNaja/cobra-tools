"""A wrapper for TriangleStripifier and some utility functions, for
stripification of sets of triangles, stitching and unstitching strips,
and triangulation of strips."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2012, Python File Format Interface
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#	* Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
#
#	* Redistributions in binary form must reproduce the above
#	  copyright notice, this list of conditions and the following
#	  disclaimer in the documentation and/or other materials provided
#	  with the distribution.
#
#	* Neither the name of the Python File Format Interface
#	  project nor the names of its contributors may be used to endorse
#	  or promote products derived from this software without specific
#	  prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****


from .trianglestripifier import TriangleStripifier
from .trianglemesh import Mesh

def triangulate(strips):
	"""A generator for iterating over the faces in a set of
	strips. Degenerate triangles in strips are discarded."""

	triangles = []

	for strip in strips:
		if len(strip) < 3: continue # skip empty strips
		i = strip.__iter__()
		j = False
		t1, t2 = next(i), next(i)
		for k in range(2, len(strip)):
			j = not j
			t0, t1, t2 = t1, t2, next(i)
			if t0 == t1 or t1 == t2 or t2 == t0: continue
			triangles.append((t0, t1, t2) if j else (t0, t2, t1))

	return triangles

def _generate_faces_from_triangles(triangles):
	i = triangles.__iter__()
	while True:
		yield (next(i), next(i), next(i))

def _sort_triangle_indices(triangles):
	"""Sorts indices of each triangle so lowest index always comes first.
	Also removes degenerate triangles."""
	for t0, t1, t2 in triangles:
		# skip degenerate triangles
		if t0 == t1 or t1 == t2 or t2 == t0:
			continue
		# sort indices
		if t0 < t1 and t0 < t2:
			yield (t0, t1, t2)
		elif t1 < t0 and t1 < t2:
			yield (t1, t2, t0)
		elif t2 < t0 and t2 < t1:
			yield (t2, t0, t1)
		else:
			# should *never* happen
			raise RuntimeError(
				"Unexpected error while sorting triangle indices.")

def _check_strips(triangles, strips):
	"""Checks that triangles and strips describe the same geometry.
	"""
	# triangulate
	strips_triangles = set(_sort_triangle_indices(triangulate(strips)))
	triangles = set(_sort_triangle_indices(triangles))
	# compare
	if strips_triangles != triangles:
		raise ValueError(
			"triangles and strips do not match\n"
			"triangles = %s\n"
			"strips = %s\n"
			"triangles - strips = %s\n"
			"strips - triangles = %s\n"
			% (triangles, strips,
			   triangles - strips_triangles,
			   strips_triangles - triangles))

def stripify(triangles, stitchstrips = False):
	"""Converts triangles into a list of strips."""

	strips = []
	# build a mesh from triangles
	mesh = Mesh()
	for face in triangles:
		try:
			mesh.add_face(*face)
		except ValueError:
			# degenerate face
			pass
	mesh.lock()

	# calculate the strip
	stripifier = TriangleStripifier(mesh)
	strips = stripifier.find_all_strips()

	# stitch the strips if needed
	if stitchstrips:
		return [stitch_strips(strips)]
	else:
		return strips

class OrientedStrip:
	"""An oriented strip, with stitching support."""

	def __init__(self, strip):
		"""Construct oriented strip from regular strip (i.e. a list)."""

		if isinstance(strip, (list, tuple)):
			# construct from strip
			self.vertices = list(strip)
			self.reversed = False
			self.compactify()
		elif isinstance(strip, OrientedStrip):
			# copy constructor
			self.vertices = strip.vertices[:]
			self.reversed = strip.reversed
		else:
			raise TypeError(
				"expected list or OrientedStrip, but got %s"
				% strip.__class__.__name__)

	def compactify(self):
		"""Remove degenerate faces from front and back."""
		# remove from front
		if len(self.vertices) < 3:
			raise ValueError(
				"strip must have at least one non-degenerate face")
		while self.vertices[0] == self.vertices[1]:
			del self.vertices[0]
			self.reversed = not self.reversed
			if len(self.vertices) < 3:
				raise ValueError(
					"strip must have at least one non-degenerate face")
		# remove from back
		while self.vertices[-1] == self.vertices[-2]:
			del self.vertices[-1]
			if len(self.vertices) < 3:
				raise ValueError(
					"strip must have at least one non-degenerate face")

	def reverse(self):
		"""Reverse vertices."""
		self.vertices.reverse()
		if len(self.vertices) & 1:
			self.reversed = not self.reversed

	def __len__(self):
		if self.reversed:
			return len(self.vertices) + 1
		else:
			return len(self.vertices)

	def __iter__(self):
		if self.reversed:
			yield self.vertices[0]
		for vert in self.vertices:
			yield vert

	def __str__(self):
		"""String representation."""
		return str(list(self))

	def __repr__(self):
		return "OrientedStrip(%s)" % str(list(self))

	def get_num_stitches(self, other):
		"""Get number of stitches required to glue the vertices of self to
		other.
		"""
		# do last vertex of self and first vertex of other match?
		has_common_vertex = (self.vertices[-1] == other.vertices[0])

		# do windings match?
		if len(self.vertices) & 1:
			has_winding_match = (self.reversed != other.reversed)
		else:
			has_winding_match = (self.reversed == other.reversed)

		# append stitches
		if has_common_vertex:
			if has_winding_match:
				return 0
			else:
				return 1
		else:
			if has_winding_match:
				return 2
			else:
				return 3

	def __add__(self, other):
		"""Combine two strips, using minimal number of stitches."""
		# make copy of self
		result = OrientedStrip(self)

		# get number of stitches required
		num_stitches = self.get_num_stitches(other)
		if num_stitches >= 4 or num_stitches < 0:
			# should *never* happen
			raise RuntimeError("Unexpected error during stitching.")

		# append stitches
		if num_stitches >= 1:
			result.vertices.append(self.vertices[-1]) # first stitch
		if num_stitches >= 2:
			result.vertices.append(other.vertices[0]) # second stitch
		if num_stitches >= 3:
			result.vertices.append(other.vertices[0]) # third stitch

		# append other vertices
		result.vertices.extend(other.vertices)

		return result

def stitch_strips(strips):
	"""Stitch strips keeping stitch size minimal."""

	class ExperimentSelector:
		"""Helper class to select best experiment."""
		def __init__(self):
			self.best_ostrip1 = None
			self.best_ostrip2 = None
			self.best_num_stitches = None
			self.best_ostrip_index = None

		def update(self, ostrip_index, ostrip1, ostrip2):
			num_stitches = ostrip1.get_num_stitches(ostrip2)
			if ((self.best_num_stitches is None)
				or (num_stitches < self.best_num_stitches)):
				self.best_ostrip1 = ostrip1
				self.best_ostrip2 = ostrip2
				self.best_ostrip_index = ostrip_index
				self.best_num_stitches = num_stitches

	# get all strips and their orientation, and their reverse
	ostrips = [(OrientedStrip(strip), OrientedStrip(strip))
			   for strip in strips if len(strip) >= 3]
	for ostrip, reversed_ostrip in ostrips:
		reversed_ostrip.reverse()
	# start with one of the strips
	if not ostrips:
		# no strips!
		return []
	result = ostrips.pop()[0]
	# go on as long as there are strips left to process
	while ostrips:
		selector = ExperimentSelector()

		for ostrip_index, (ostrip, reversed_ostrip) in enumerate(ostrips):
			# try various ways of stitching strips
			selector.update(ostrip_index, result, ostrip)
			selector.update(ostrip_index, ostrip, result)
			selector.update(ostrip_index, result, reversed_ostrip)
			selector.update(ostrip_index, reversed_ostrip, result)
			# break early if global optimum is already reached
			if selector.best_num_stitches == 0:
				break
		# get best result, perform the actual stitching, and remove
		# strip from ostrips
		result = selector.best_ostrip1 + selector.best_ostrip2
		ostrips.pop(selector.best_ostrip_index)
	# get strip
	strip = list(result)
	# check if we can remove first vertex by reversing strip
	if strip[0] == strip[1] and (len(strip) & 1 == 0):
		strip = strip[1:]
		strip.reverse()
	# return resulting strip
	return strip

def unstitch_strip(strip):
	"""Revert stitched strip back to a set of strips without stitches."""
	strips = []
	currentstrip = []
	i = 0
	while i < len(strip)-1:
		winding = i & 1
		currentstrip.append(strip[i])
		if strip[i] == strip[i+1]:
			# stitch detected, add current strip to list of strips
			strips.append(currentstrip)
			# and start a new one, taking into account winding
			if winding == 1:
				currentstrip = []
			else:
				currentstrip = [strip[i+1]]
		i += 1
	# add last part
	currentstrip.extend(strip[i:])
	strips.append(currentstrip)
	# sanitize strips
	for strip in strips:
		while len(strip) >= 3 and strip[0] == strip[1] == strip[2]:
			strip.pop(0)
			strip.pop(0)
	return [strip for strip in strips if len(strip) > 3 or (len(strip) == 3 and strip[0] != strip[1])]
