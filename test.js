const dataset = [1,2,3,4,5]

D3.select("body").selectAll("p")
.data(dataset)
.enter()
.append("p");