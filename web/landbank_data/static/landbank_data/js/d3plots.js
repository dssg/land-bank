function d3hist(div, data, title, label, marker) {
  
  var margin = { top: 40, right: 20, bottom: 60, left: 40},
      width = 240 - margin.left - margin.right,
      height = 200 - margin.top - margin.bottom;
  
  data = data.sort(function(a,b) { if (a.x > b.x) return 1; if (a.x < b.x) return -1; return 0; });
  var xdeltas = [];
  for(var i=1; i<data.length; i++) { data[i].xdelta = data[i].x - data[i-1].x; };
    // creates 10% of distribution bins
  data[0].xdelta = data[1].xdelta;
  var xmin = d3.min(data, function(d) { return d.x; });
  var xmax = d3.max(data, function(d) { return d.x; });
  var ymax = d3.max(data, function(d) { return d.y; });
  var padding = data[0].xdelta * 0.1;

    //creates a domain buffer of 10% on each side of the min and max
    //creates scales and axes
    var xScale = d3.scale.linear()
      .domain([xmin-data[0].xdelta, xmax+data[data.length-1].xdelta])
      .range([0, width]);
  
  var yScale = d3.scale.linear()
      .domain([0, ymax])
      .range([height, 0])
  
  var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom")
      .ticks(5)
      .tickFormat(d3.format("3.0f"));

  if (data[0].xdelta < 1.0) {
    xAxis.tickFormat(d3.format("3.1f"));
  }
  if (data[0].xdelta < 0.1) {
    xAxis.tickFormat(d3.format("3.2f"));
  }
  
  var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left");
//  add the chart to the computed html
  var svg = d3.select(div).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .attr("id","chart");
 
// y axis text
  svg.append("g")
     .append("text")
     .attr("y", -10)
     .attr("x", width/2)
     .style("text-anchor","middle")
     .text(title);
// x axis text  
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("y",margin.bottom/2)
      .attr("x",width/2)
      .style("text-anchor", "middle")
      .text(label) ;
  // creates y axis
  svg.append("g")
      .attr("class", "axis")
      .attr("id", "yaxis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left)
      .attr("x", 0-(height/2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Count");
  
  if ((typeof marker !== 'undefined') && (marker != 99999)) {
    if (marker > xmax) { marker = xmax-0.01; };
    if (marker < xmin) { marker = xmin+0.01; };
    var line=svg.append("line")
      .attr({ 
        "x1": xScale(marker), "y1": yScale(0),
        "x2": xScale(marker), "y2": yScale(ymax),
        "stroke-width": 3, "stroke": "black"
      });
  };
    // manually creates y bar
  svg.selectAll(".bar")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return xScale(d.x - d.xdelta/2.0);} )
      .attr("width", function(d) { return xScale(d.x + d.xdelta/2.0-padding)-
                                          xScale(d.x - d.xdelta/2.0 + padding);} )
      .attr("y", function(d) { return yScale(d.y)} )
      .attr("height", function(d) { return height - yScale(d.y); })
      .attr("fill", "rgb(0, 0, 128)")
      .attr("opacity", 0.3);
};

function d3timeline(div, data, title, marker) {
  var margin = { top: 20, right: 20, bottom: 60, left: 60},
      width = 320 - margin.left - margin.right,
      height = 320 - margin.top - margin.bottom;

    // need to parse the date and dates from python must be passed as strings
  var parseDate = d3.time.format("%Y-%m-%d").parse;
  
  data.forEach(function(d) { d.x = parseDate(d.x); });

  data = data.sort(function(a,b) { if (a.x > b.x) return 1; if (a.x < b.x) return -1; return 0; });
  var xmin = d3.min(data, function(d) { return d.x; });
  var xmax = d3.max(data, function(d) { return d.x; });
  var ymin = d3.min(data, function(d) { return d.y; });
  var ymax = d3.max(data, function(d) { return d.y; });
  var ybot = d3.max([0,ymin-0.1*(ymax-ymin)]);
  var ytop = ymax+0.1*(ymax-ymin);

    // scales and axes
  var xScale = d3.time.scale()
      .domain(d3.extent(data, function(d) { return d.x; }))
      .range([0, width]);

  var yScale = d3.scale.linear()
      .domain([ybot, ytop])
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom");
  
  var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left");

    // computing the line that travels to each data point
  var line = d3.svg.line()
      .interpolate("linear")
      .x(function(d) { return xScale(d.x); })
      .y(function(d) { return yScale(d.y); });

    //append the chart
  var svg = d3.select(div).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
    //append the x axis
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("y",margin.bottom/2)
      .attr("x",width/2)
      .style("text-anchor", "middle")
      .text("Time") ;
  
    //append the y axis
  svg.append("g")
      .attr("class", "axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left)
      .attr("x", 0-(height/2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text(title);
  
  if (typeof marker !== 'undefined') {
    svg.append("line")
      .attr({ 
        "y1": yScale(marker), "x1": xScale(0),
        "y2": yScale(marker), "x2": xScale(xmax),
        "stroke-width": 3, "stroke": "black"
      });
  };

//append a timeseries class which contains the line
  var timeseries = svg.selectAll(".timeseries")
      .data(data)
      .enter().append("g")
      .attr("class","timeseries");
//append the actual path
  timeseries.append("path")
      .attr("class","line")
      .attr("d", line(data))
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("fill", "none");
};
