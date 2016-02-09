    var width = 750, height = 400;

    

    var path = d3.geo.path();

    
    var colorlist =[];
    for (var key in window.colorbrewer) {
      if (window.colorbrewer.hasOwnProperty(key)){
      colorlist.push(key);
      }
    }
    console.log(colorlist);
    var svg = d3.select("#map").append("svg")
            .attr("width", width)
            .attr("height", height);
    var projection = d3.geo.albersUsa().translate([width/2.2, height/2.4]).scale([750]);
    var path = d3.geo.path().projection(projection);

    //$("#swap").click(updatemap);
    updatemap(0);
    
    

    d3.selectAll(".m")
                .on("click", function() {
                    var lan_id = this.getAttribute("value");
                    updatemap(lan_id);
                  });


    function updatemap(lan_id){
       console.log("click");
       queue()
      .defer(d3.json, "us_state.json")
      .defer(d3.csv, "us_city.csv")
      .await(function(error,us,city){ready(us,city,lan_id)});
    }
    

   // d3.json("https://raw.githubusercontent.com/alignedleft/d3-book/master/chapter_12/us-states.json",ready);

    function ready(us,city,lan_id) {
        console.log(lan_id);
		    //console.log(us);
       
        var host = $(location).attr('host');
        var protocol = $(location).attr('protocol');
        //lan=encodeURIComponent(lan)
        //console.log(lan)
       //console.log(protocol+'//'+host+'/'+lan)
        $.get(protocol+'//'+host+'/language/'+lan_id,function(data_in_us){  
       var cscale;

       if (parseInt(lan_id)==0){
        cscale = colorbrewer.Blues[9];
       }
       else{
      cscale = colorbrewer[colorlist[lan_id]][9];
      }
       
       var colors = d3.scale.quantile()
                    .domain([d3.min(data_in_us.state_count.slice(0,data_in_us.state_count.length-2)),
                            d3.max(data_in_us.state_count.slice(0,data_in_us.state_count.length-2))])
                    .range(cscale);
       console.log(colors);

        console.log(typeof(us.features));
        svg.selectAll("path").remove();
        svg.selectAll("circle").remove();
        svg.selectAll("path")
                .data(us.features)
                .enter()
                .append("path")
                .attr("class","state")
                .attr("d", path)
                .style("fill", function(d){
                  console.log(d.seq)
                  console.log(data_in_us)
                  return colors(data_in_us.state_count[d.seq]);
                })
                .append("svg:title")
                .text(function(d){ return d.properties.name+"\n"+data_in_us.state_count[d.seq]});

      //d3.csv("us_city.csv", function(data) { 
         //console.log(data);
         svg.selectAll("circle")
           .data(city)
           .enter()
           .append("circle")
           .attr("cx", function(d) {
                   return projection([d.longitude, d.latitude])[0];
           })
           .attr("cy", function(d) {
                   //console.log(d.latitude);
                   return projection([d.longitude, d.latitude])[1];
           })
           .attr("r", 3)
           .style("fill", "red")
           .style("opacity", 1)
           .append("svg:title")
           .text(function(d){return d.Place+"\n"+data_in_us.city_count[d.Rank-1]});

           d3.select('#legend')
                        .selectAll('ul')
                        .remove();
                    console.log(colors.range())
                    // build the map legend
                    var legend = d3.select('#legend')
                        .append('ul')
                        .attr('class', 'list-inline');
    
                    var keys = legend.selectAll('li.key')
                        .data(colors.range());
    
                    var legend_items = ["Low", "", "", "", "", "", "", "", "High"];
    
                    keys.enter().append('li')
                        .attr('class', 'key')
                        .style('border-top-color', String)
                        .text(function (d, i) {
                            return legend_items[i];
                        });
             });


            }
        