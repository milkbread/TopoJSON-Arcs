#!/usr/bin/python
#This script was written by Ralf Klammer, 22.10.2013
################################
#It demonstrates how to get more control of TopoJSON-geometries by 
#manipulating the single arc-geometries and use them directly to build the GeoJSON-features

import json
import topojson_rk as topojson

#topology = topojson.openTopoJSON('https://gist.github.com/milkbread/5957651/raw/81e3b548ab7873f3f80829e918ac5bd0da083a72/vg250_bld_krs_topo.json')
topology = topojson.openJSON('data/vg250_bld_krs_topo.json')
arcs = topology['arcs']
objects = topology['objects']

topoTrans = topojson.Transformation(topology['transform'])
arcGeometries = topoTrans.getArcGeometries(arcs)

topoGeomBuilder = topojson.BuildGeometries(arcGeometries)

geoJSON = topoGeomBuilder.buildFeatures(objects['vg250_bld']['geometries'])
topojson.saveGeoJSON(geoJSON, 'result.geojson')

