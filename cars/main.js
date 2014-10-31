(function() {
var groups = [
{key: "US", values:[]},
{key: "EU", values:[]},
{key: "JP", values:[]}]
var indices = {"US": 0, "Europe":1, "Japan":2}
var x = d3.csv("cars.csv", function(d) {
  // console.log(d)
  var datapoint = {
      x: +d.MPG,
      y: +d.horsepower,
      size: +d.weigth,
      shape: "circle"
    }
  groups[indices[d.origin]].values.push(datapoint)
  // return {
    // year: new Date(+d.Year, 0, 1), // convert "Year" column to Date
    // make: d.make,
    // model: d.model,
    // length: +d.Length // convert "Length" column to number
  // };
}, function(error, rows) {
  console.log(rows);
});


nv.addGraph(function() {
  var chart = nv.models.scatterChart()
                .transitionDuration(350)
                .color(d3.scale.category10().range());

  //Configure how the tooltip looks.
  chart.tooltipContent(function(key) {
      return '<h3>' + key + '</h3>';
  });

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
})();
