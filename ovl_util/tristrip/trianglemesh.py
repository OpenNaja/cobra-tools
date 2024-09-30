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

# modified from:

# http://techgame.net/projects/Runeblade/browser/trunk/RBRapier/RBRapier/Tools/Geometry/Analysis/TriangleMesh.py?rev=760

# original license:

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ License
##~
##- The RuneBlade Foundation library is intended to ease some
##- aspects of writing intricate Jabber, XML, and User Interface (wxPython, etc.)
##- applications, while providing the flexibility to modularly change the
##- architecture. Enjoy.
##~
##~ Copyright (C) 2002  TechGame Networks, LLC.
##~
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the
##~ LICENSE file included with this distribution.
##~
##~ TechGame Networks, LLC can be reached at:
##~ 3578 E. Hartsel Drive #211
##~ Colorado Springs, Colorado, USA, 80920
##~
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import operator # itemgetter

from weakref import WeakSet

class Edge:
	"""A directed edge which keeps track of its faces."""

	def __init__(self, ev0, ev1):
		"""Edge constructor."""
		
		if ev0 == ev1:
			raise ValueError("Degenerate edge.")

		self.verts = (ev0, ev1)
		"""Vertices of the edge."""

		self.faces = WeakSet()
		"""Weak set of faces that have this edge."""

	def __repr__(self):
		"""String representation."""
		return "Edge(%s, %s)" % self.verts

class Face:
	"""An oriented face which keeps track its adjacent faces."""

	def __init__(self, v0, v1, v2):
		"""Construct face from vertices."""
		if v0 == v1 or v1 == v2 or v2 == v0:
			raise ValueError("Degenerate face.")
		if v0 < v1 and v0 < v2:
			self.verts = (v0, v1, v2)
		if v1 < v0 and v1 < v2:
			self.verts = (v1, v2, v0)
		if v2 < v0 and v2 < v1:
			self.verts = (v2, v0, v1)
		# no index yet
		self.index = None

		self.adjacent_faces = (WeakSet(), WeakSet(), WeakSet())
		"""Weak sets of adjacent faces along edge opposite each vertex."""

	def __repr__(self):
		"""String representation."""
		return "Face(%s, %s, %s)" % self.verts

	def get_next_vertex(self, vi):
		"""Get next vertex of face."""
		return self.verts[(1, 2, 0)[self.verts.index(vi)]]

	def get_adjacent_faces(self, vi):
		"""Get adjacent faces associated with the edge opposite a vertex."""
		return self.adjacent_faces[self.verts.index(vi)]

class Mesh:
	"""A mesh of interconnected faces."""
	def __init__(self, faces=None, lock=True):
		"""Initialize a mesh, and optionally assign its faces and lock.
		"""
		self._faces = {}
		self._edges = {}
		if faces is not None:
			for v0, v1, v2 in faces:
				self.add_face(v0, v1, v2)
			if lock:
				self.lock()

	def __repr__(self):
		"""String representation."""
		try:
			self.faces
		except AttributeError:
			# unlocked
			if not self._faces:
				# special case
				return "Mesh()"
			return ("Mesh(faces=[%s], lock=False)"
					% ', '.join(repr(faceverts)
								for faceverts in sorted(self._faces)))
		else:
			# locked
			return ("Mesh(faces=[%s])"
					% ', '.join(repr(face.verts)
								for face in self.faces))

	def _add_edge(self, face, pv0, pv1):
		"""Create new edge for mesh for given face, or return existing
		edge. Lists of faces of the new/existing edge is also updated,
		as well as lists of adjacent faces. For internal use only,
		called on each edge of the face in add_face.
		"""
		# create edge if not found
		try:
			edge = self._edges[(pv0, pv1)]
		except KeyError:
			# create edge
			edge = Edge(pv0, pv1)
			self._edges[(pv0, pv1)] = edge

		# update edge's faces
		edge.faces.add(face)

		# find reverse edge in mesh
		try:
			otheredge = self._edges[(pv1, pv0)]
		except KeyError:
			pass
		else:
			# update adjacent faces
			pv2 = face.get_next_vertex(pv1)
			for otherface in otheredge.faces:
				otherpv2 = otherface.get_next_vertex(pv0)
				face.get_adjacent_faces(pv2).add(otherface)
				otherface.get_adjacent_faces(otherpv2).add(face)

	def add_face(self, v0, v1, v2):
		"""Create new face for mesh, or return existing face. List of
		adjacent faces is also updated.
		"""
		face = Face(v0, v1, v2)
		try:
			face = self._faces[face.verts]
		except KeyError:
			# create edges and update links between faces
			self._add_edge(face, v0, v1)
			self._add_edge(face, v1, v2)
			self._add_edge(face, v2, v0)
			# register face in mesh
			self._faces[face.verts] = face

		return face

	def lock(self):
		"""Lock the mesh. Frees memory by clearing the structures
		which are only used to update the face adjacency lists. Sets
		the faces attribute to the sorted list of all faces (sorting helps
		with ensuring that the strips in faces are close together).
		"""
		# store faces and set their index
		self.faces = []
		for i, (verts, face) in enumerate(sorted(iter(self._faces.items()),
										  key=operator.itemgetter(0))):
			face.index = i
			self.faces.append(face)
		# remove helper structures
		del self._faces
		del self._edges

	def discard_face(self, face):
		"""Remove the face from the mesh."""
		# note: don't delete, but set to None, to ensure that other
		# face indices remain valid
		self.faces[face.index] = None
		for adj_faces in face.adjacent_faces:
			for adj_face in adj_faces:
				for adj_adj_faces in adj_face.adjacent_faces:
					adj_adj_faces.discard(face)