(function() {

var lightness = d3.scale.ordinal().range([0,  0.125,  0.25 ,  0.375,  0.5]).domain([3,4,5,6,8]),
    saturation = d3.scale.linear().range([0.5,1]).domain([70,83]),
    hue = {'US':50, 'Europe' : 200, 'Japan' : 100};

var groups = [
  {key: "US", color:d3.hsl(hue['US'],1,.5), values:[]},
  {key: "EU", color:d3.hsl(hue['Europe'],1,.5), values:[]},
  {key: "JP", color:d3.hsl(hue['Japan'],1,.5), values:[]}];
var indices = {"US": 0, "Europe":1, "Japan":2};

var cylinders =
{
  3: "triangle-up",
  4: "square",
  5: "diamond",
  6: "cross",
  8: "circle"}


d3.csv("cars.csv", function(d) {
  var datapoint = {
      x: +d.MPG,
      y: +d.horsepower,
      size: +d.weigth,
      shape: cylinders[+d.cylinders],
      color: d3.hsl(hue[d.origin],saturation(+d.year), 0.5),
      data: d
    };
  groups[indices[d.origin]].values.push(datapoint);

}, function(error, rows) {
    nv.addGraph(function() {
        var chart = nv.models.scatterChart()
                    .transitionDuration(100)
                    .color(d3.scale.category10().range());

        //Configure how the tooltip looks.
        chart.tooltipContent(function(key,x,y,datapoint) {
        string = '';
        for (var property in datapoint.point.data) {
            if (datapoint.point.data.hasOwnProperty(property)) {
                string += property + ' : ' + datapoint.point.data[property] + '<br />';
            }
        }
          return '<h3>' + string + '</h3>';
        });
        chart.scatter.onlyCircles(false);


        //Axis settings
        chart.xAxis.tickFormat(d3.format('.02f'));
        chart.yAxis.tickFormat(d3.format('.02f'));

        //We want to show shapes other than circles.

        d3.select('#chart svg')
          .datum(groups)
          .call(chart);

        nv.utils.windowResize(chart.update);
        return chart;
    });
});



})();
