var row = sets.length;
//console.log(row)
var col = 0;
var array = []
//Temp Array
var array2 = []

//Count for Colums
for(var i=0;i<row;i++){
	
	if(sets[i].sets.length == 1) {
		col++;}
	}
//Create Rows and Columns
for (var i=0;i<row;i++){
var body = d3.select("body")
		.append("div")
			.attr("class", "row"+i)
	for (var j = 0;j<col+2;j++){
	var div = d3.select(".row"+i)
		.append("svg")
				.attr("class", "col"+j)
				.attr("height", 30)
				.attr("width", 30)}
}


//Create Empty Circles
for (var i=0;i<row;i++){
	for (var j=0;j<col;j++){
			var div = d3.select(".row"+i).select(".col"+j)
				.append("circle")
					.attr("class", "circle"+j)
					.attr("cx",15)
					.attr("cy",15)
					.attr("r",12)
					.attr("stroke","black")
					.attr("stroke-width",3)
					.attr("fill","white")}
		}           
//Fill the circles
for (var i=0;i<row;i++){
	for (var j=0;j<col;j++){
			var circle = d3.select(".row"+i).select(".col"+sets[i].sets[j]).select(".circle"+sets[i].sets[j])
				.attr("fill","black")
            if (typeof sets[i].sets[j] != "undefined"){
            array2.push(sets[i].sets[j])}
            
                }
            if (array2.length != 1){
            array.push(array2.concat(i))}
            array2 = []
         
		}

//Adding Text(Size)   
for (var i=0;i<row;i++){
    console.log()
    var div = d3.select(".row"+i).select(".col"+(col))
        .append("text")
            .attr("x",15)
            .attr("y",20)
            .text(sets[i].size)
            .attr("font-size","15px")
}
//Graphs
for (var i=0;i<row;i++){
    console.log()
    var div = d3.select(".row"+i).select(".col"+(col+1))
        .attr("width", "auto")
        .append("line")
            .attr("stroke-width","10")
            .attr("stroke","black")
            .attr("x1",0)
            .attr("x2",sets[i].size*5)
            .attr("y1",10)
            .attr("y2",10)
//array[i][array[i].length-1]
}


//lines
    

for (var i=0;i<array.length;i++){
    for (var j=array[i][0];j<array[i][array[i].length-2]+1;j++){
        console.log(array[i][array[i].length-2])
        var div = d3.select(".row"+array[i][array[i].length-1]).select(".col"+j)
            .append("line")
                .attr("stroke-width","3")
                .attr("stroke","black")
                .attr("x1",0)
                .attr("x2",30)
                .attr("y1",15)
                .attr("y2",15)
    }
}

