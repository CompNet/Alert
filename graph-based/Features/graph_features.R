#!/usr/bin/env Rscript

###################################################################
# Processes the missing topological measures
#
# R igraph documentation: http://igraph.org/r/doc/
# 
# How to call an R script from the command line:
# R --vanilla < /my/path/myscript.R > terminal.output.txt
###################################################################
suppressMessages(library("igraph"))
source("rolemeas.R")

# sudo apt install libxml2-dev to correct
# foreign-graphml.c:1211 : GraphML support is disabled, Unimplemented function call
# then reinstall with
# $ R
# > install.packages("igraph")

args = commandArgs(TRUE)

graph.file <- args[1]
# name of the result files
res.graph.file <- "/proc/self/fd/1"




# read the graph
g <- read.graph(graph.file, format="graphml")



compute_graph_features <- function(g) {
	res <- list()
	
	# number of articulation points
	start.time <- Sys.time()
		ap.idx <- articulation_points(graph=g)
		graph.res <- as.matrix(length(ap.idx))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	graph.time <- as.matrix(duration)
	colnames(graph.res) <- "Articulation_Point_Nbr"
	colnames(graph.time) <- "Articulation_Point_Nbr"
	
	# reciprocity
	start.time <- Sys.time()
		graph.res <- cbind(graph.res, reciprocity(graph=g, ))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	graph.time <- cbind(graph.time, duration)
	colnames(graph.res)[ncol(graph.res)] <- "Reciprocity"
	colnames(graph.time)[ncol(graph.res)] <- "Reciprocity"
	
	res$Values <- graph.res
	res$Timing <- graph.time
	return(res)
}

graph_res <- compute_graph_features(g)


write.table(x=graph_res$Timing, file=res.graph.file, row.names=FALSE, col.names=TRUE)
