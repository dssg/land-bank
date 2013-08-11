function d3hist(div, data, title, marker) {
  
  var margin = { top: 20, right: 20, bottom: 60, left: 60},
      width = 320 - margin.left - margin.right,
      height = 320 - margin.top - margin.bottom;
  
  data = data.sort(function(a,b) { if (a.x > b.x) return 1; if (a.x < b.x) return -1; return 0; });
  var xdelta=data[1].x - data[0].x;
  var xmax = d3.max(data, function(d) { return d.x; });
  var ymax = d3.max(data, function(d) { return d.y; });
  var padding = xdelta * 0.1;
  var bar_width = xdelta - padding;
  
  
  var xScale = d3.scale.linear()
      .domain([0, xmax+xdelta/2.0])
      .range([0, width]);
  
  var yScale = d3.scale.linear()
      .domain([0, ymax])
      .range([height, 0]);
  
  var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom")
      .ticks(10)
      .tickFormat(d3.format("3.2f"));
  
  var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left");
  
  var svg = d3.select(div).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("y",margin.bottom/2)
      .attr("x",width/2)
      .style("text-anchor", "middle")
      .text(title) ;
  
  svg.append("g")
      .attr("class", "axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left)
      .attr("x", 0-(height/2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Count");
  
  if (typeof marker !== 'undefined') {
    svg.append("line")
      .attr({ 
        "x1": xScale(marker), "y1": yScale(0),
        "x2": xScale(marker), "y2": yScale(ymax),
        "stroke-width": 3, "stroke": "black"
      });
  };
  
  svg.selectAll(".bar")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return xScale(d.x - xdelta/2.0 + padding/2.0)} )
      .attr("width", xScale(bar_width))
      .attr("y", function(d) { return yScale(d.y)} )
      .attr("height", function(d) { return height - yScale(d.y); })
      .attr("fill", function(d) {
          return "rgb(0, 0, "+ Math.round((255*d.y)/
                                          d3.max(
          $.map(data,function(d){ return d.y; })))  + ")";
      })
      .attr("opacity", "0.4");
  
};

function d3timeline(div, data, title, marker) {
  var margin = { top: 20, right: 20, bottom: 60, left: 60},
      width = 320 - margin.left - margin.right,
      height = 320 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m-%d").parse;
  
  data.forEach(function(d) { d.x = parseDate(d.x); });

  data = data.sort(function(a,b) { if (a.x > b.x) return 1; if (a.x < b.x) return -1; return 0; });
  var xmin = d3.min(data, function(d) { return d.x; });
  var xmax = d3.max(data, function(d) { return d.x; });
  var ymin = d3.min(data, function(d) { return d.y; });
  var ymax = d3.max(data, function(d) { return d.y; });
  var ybot = d3.max([0,ymin-0.1*(ymax-ymin)]);
  var ytop = ymax+0.1*(ymax-ymin);

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

  var line = d3.svg.line()
      .interpolate("linear")
      .x(function(d) { return xScale(d.x); })
      .y(function(d) { return yScale(d.y); });

  var svg = d3.select(div).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("y",margin.bottom/2)
      .attr("x",width/2)
      .style("text-anchor", "middle")
      .text("Time") ;
  
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
  
  /*if (typeof marker !== 'undefined') {
    svg.append("line")
      .attr({ 
        "y1": yScale(marker), "x1": xScale(0),
        "y2": yScale(marker), "x2": xScale(xmax),
        "stroke-width": 3, "stroke": "black"
      });
  };*/


  var timeseries = svg.selectAll(".timeseries")
      .data(data)
      .enter().append("g")
      .attr("class","timeseries");

  timeseries.append("path")
      .attr("class","line")
      .attr("d", line(data))
      .attr("stroke", "blue")
      .attr("stroke-width", 3)
      .attr("fill", "none");
};
