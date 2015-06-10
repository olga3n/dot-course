#!/usr/bin/env python3

import interface_pb2
import binascii

pref = """
<!DOCTYPE html>
	<meta charset="utf-8">

	<body style="padding-top:60px">
		<script src="lib/d3-cloud/lib/d3/d3.js"></script>
		<script src="lib/d3-cloud/d3.layout.cloud.js"></script>

		<style>
			text:hover { opacity: .3; cursor: pointer;}
		</style>

		<script>

			var words = [

"""

suf = """

			]

			d3.layout.cloud().size([800, 600])
					.words(words)
					.padding(5)
					.rotate(function(d) { return d.rotation? d.rotation: 0; })
					.font("Impact")
					.fontSize(function(d) { return d.size? d.size: 20; })
					.on("end", draw)
					.start();
			function draw(words) {
				d3.select("body").append("svg")
						.attr("width", 800)
						.attr("height", 600)
						.attr("style", "display: block; margin-left: auto; margin-right: auto;") 
					.append("g")
						.attr("transform", "translate(400, 300)")
					.selectAll("text")
						.data(words)
					.enter().append("a")
						.attr("xlink:href", function(d){ return d.url; })
					.append("text")
						.style("font-size", function(d) { return d.size + "px"; })
						.style("font-family", "Impact")
						.style("fill", function(d) { return "#" + d.color;})
						.attr("text-anchor", "middle")
						.attr("transform", function(d) {
							return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
						})
						.text(function(d) {return d.text;})
						.append("title")
					.text(function(d){ return d.url; })		
			}
		</script>
	</body>
</html>
"""

def wrap(items):

	tags = []

	for i in items.tag:
		tags.append( (\
			"{ \"text\" : \"%s\", \"url\" : \"%s\", \"size\" : \"%s\", \"rotation\" : \"%s\", \"color\" : \"%s\" }" % \
			( i.text, i.url, i.font_size or "50", i.rotation, (i.font_color  or b"000000").decode("utf-8") )\
			) )

	data = ",\n".join(tags)

	return (pref + data + suf )