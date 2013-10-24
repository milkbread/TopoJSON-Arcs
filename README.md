TopoJSON-Arcs
=============

Python-Class to read and modify the arcs of a TopoJSON-file

Download the repository:

```sh
git clone https://github.com/milkbread/TopoJSON-Arcs.git
```

[Exemplary Python-Code](run_example.py):

* Import the Python-classes

	```Python
	import topojson_rk as topojson
	```

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

Automatic Execution using [makeGeoJSON.py](makeGeoJSON.py):

* Dummy

	```sh
	python makeGeoJSON.py -i <inputfile> -o <outputfile> -f <TopoJSON-Feature>
	```

* Example

	```sh
	python makeGeoJSON.py -i data/vg250_bld_krs_topo.json -o result.geojson -f 'vg250_bld'
	```

*What is a 'TopoJSON-Feature???'*

When you look into the [specification](https://github.com/topojson/topojson-specification/blob/master/README.md), you'll notice, that a TopoJSON-file can contain one or more different original GeoJSON-files.
That is why you have to specify, which one you want to use. Normally, this 'name' corresponds with the original filename.
In the example we want to re-build the GeoJSON-File of the Feature 'vg250_bld' because the original GeoJSON-file was called 'vg250_bld.json'!

Other Python-Approaches:

* complete library: https://github.com/calvinmetcalf/topojson.py
* examples: http://sgillies.net/blog/1159/topojson-with-python/

