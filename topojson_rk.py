#!/usr/bin/python
#This script was written by Ralf Klammer, 22.10.2013
#Considerably inspired by Sean Gillies --> http://sgillies.net/blog/1159/topojson-with-python/

import json
import urllib

class Transformation:
	def __init__(self, transform):
		self.scale = transform['scale']
		self.translate = transform['translate']

	def convertPoint(self, point):
		return [point[0]*self.scale[0]+self.translate[0],point[1]*self.scale[1]+self.translate[1]]

	def convertArc(self, arc):
	 out_arc = []
	 previous=[0,0]
	 for point in arc:
	  previous[0]+=point[0];
	  previous[1]+=point[1];
	  out_arc.append(self.convertPoint(previous))	    
	 return out_arc

	def getArcGeometries(self, arcs):
		arcGeoms = []
		for arc in arcs:
			arcGeoms.append(self.convertArc(arc))
		return arcGeoms


class BuildGeometries:
	def __init__(self, arcGeometries):
		self.arcGeometries = arcGeometries

	def getArcID(self, arc):
		geomID = arc
		flip = False
		if(geomID<0):
			geomID = (geomID*(-1))-1
			flip = True
		return geomID, flip	

	def readLineString(self, lineArcs):
		lineGeom = []
		count = 0
		for arc in lineArcs:
			geomID, flip = self.getArcID(arc)
			geomCache = self.arcGeometries[geomID]#
			if(flip==True):		#the geometry needs to be reversed when the arcID was originally negative
				geomCache.reverse()	
			if(count==0):
				lineGeom=geomCache
			else:
				geomCache.pop(0)	#the 1st is identic with the last of the previous...not needed!!!
				for part in geomCache:
					lineGeom.append(part)
			#print geomCache[0], geomCache[len(geomCache)-1]
			#print 'line****', flip
			#print geomCache		
			count=count+1
		return lineGeom

	def readPolygon(self, polyArcs):
		polyGeom = []
		for polyPartArcs in polyArcs:
			polyGeom.append(self.readLineString(polyPartArcs))
		#print polyGeom
		return polyGeom


	def readMultiPolygon(self, arcs):
		multiPolyGeom = []
		for polyArcs in arcs:
			#print polyArcs
			multiPolyGeom.append(self.readPolygon(polyArcs))
		return multiPolyGeom

	def buildGeoSONGeometry(self, pureGeom):
		type = pureGeom['type']
		arcs = pureGeom['arcs']
		geometry = {}
		geometry['type']=type
		if(type=='LineString'):
			geometry['coordinates'] = self.readLineString(arcs)
		if(type=='Polygon'):
			geometry['coordinates'] = self.readPolygon(arcs)
		if(type=='MultiPolygon'):
			geometry['coordinates'] = self.readMultiPolygon(arcs)
		return geometry

	def buildFeature(self, pureGeom):
		feature = {}
		feature['type']='Feature'
		feature['properties']=pureGeom['properties']
		feature['geometry']=self.buildGeoSONGeometry(pureGeom)
		return feature

	def buildFeatures(self, pureGeoms):
		featColl = {}
		featColl['type']='FeatureCollection'
		featsCache = []
		for pureGeom in pureGeoms:
			featsCache.append(self.buildFeature(pureGeom))
		featColl['features']=featsCache
		return featColl

def saveGeoJSON(data, name):
	json_file=open(name,'w');
	json.dump(data, json_file);
	json_file.close();

def openJSON(fileURL):
	data = urllib.urlopen(fileURL).read();
	return json.loads(data)
