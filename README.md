TopoJSON-Arcs
=============

Python-Class to read and modify the arcs of a TopoJSON-file

Download the repository:

```sh
git clone https://github.com/milkbread/TopoJSON-Arcs.git
```

Exemplary Python-Code:

* Open a TopoJSON-file & get the arcs and objects

	```Python
	topology = topojson.openJSON('data/vg250_bld_krs_topo.json')
	arcs = topology['arcs']
	objects = topology['objects']
	```
* Get the corresponding geometries (LineStrings) of each arc

	```Python
	topoTrans = topojson.Transformation(topology['transform'])
	arcGeometries = topoTrans.getArcGeometries(arcs)
	```

* Build GeoJSON-geometries, using the original objects

	```Python
	topoGeomBuilder = topojson.BuildGeometries(arcGeometries)
	```

* Save GeoJSON-Features to Disk

	```Python
	geoJSON = topoGeomBuilder.buildFeatures(objects['vg250_bld']['geometries'])
	topojson.saveGeoJSON(geoJSON, 'result.geojson')
	```

Other Python-Approaches:

* complete library: https://github.com/calvinmetcalf/topojson.py
* examples: http://sgillies.net/blog/1159/topojson-with-python/

