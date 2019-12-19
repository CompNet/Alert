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
res.node.file <- "/proc/self/fd/1"




# read the graph
g <- read.graph(graph.file, format="graphml")


compute_node_features <- function(g) {
    res <- list()
	
    g2 <- remove.edge.attribute(graph=g, name="weight")

    # unweighted alpha centrality
	start.time <- Sys.time()
		node.res <- as.matrix(alpha_centrality(graph=g, weights=NA, alpha=0.9))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- as.matrix(duration)
	colnames(node.res) <- "Alpha_Unweighted"
	colnames(node.time) <- "Alpha_Unweighted"
	
    # weighted alpha centrality
	start.time <- Sys.time()
		node.res <- cbind(node.res, alpha_centrality(graph=g, alpha=0.9))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	colnames(node.res)[ncol(node.res)] <- "Alpha_Weighted"
	colnames(node.time)[ncol(node.time)] <- "Alpha_Weighted"
	
    # articulation points (1 if AP, 0 otherwise)
	start.time <- Sys.time()
	art.points <- rep(0, gorder(g))
	ap.idx <- 
			articulation_points(graph=g)
	art.points[ap.idx] <- 1
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	node.res <- cbind(node.res, art.points)
	colnames(node.res)[ncol(node.res)] <- "Articulation_Point"
	colnames(node.time)[ncol(node.time)] <- "Articulation_Point"
	
    # unweighted Burt's constraint
	start.time <- Sys.time()
	node.res <- cbind(node.res, 
			constraint(graph=g2))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	colnames(node.res)[ncol(node.res)] <- "Burt_Cstrt_Unweighted"
	colnames(node.time)[ncol(node.time)] <- "Burt_Cstrt_Unweighted"
	
    # unweighted Burt's constraint
	start.time <- Sys.time()
	node.res <- cbind(node.res, 
			constraint(graph=g))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	colnames(node.res)[ncol(node.res)] <- "Burt_Cstrt_Weighted"
	colnames(node.time)[ncol(node.time)] <- "Burt_Cstrt_Weighted"
	
    # Bonacich power measure
	start.time <- Sys.time()
	node.res <- cbind(node.res, 
			power_centrality(graph=g, exponent=0.9))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	colnames(node.res)[ncol(node.res)] <- "Bonacich_Power"
	colnames(node.time)[ncol(node.time)] <- "Bonacich_Power"
	
    # Subgraph centrality
	start.time <- Sys.time()
	node.res <- cbind(node.res, 
			subgraph_centrality(graph=g))
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	node.time <- cbind(node.time, duration)
	colnames(node.res)[ncol(node.res)] <- "Subgraph_Ctr"
	colnames(node.time)[ncol(node.time)] <- "Subgraph_Ctr"
	
    # community role measures
	start.time <- Sys.time()
		membership <- infomap.community(graph=g, modularity=FALSE)$membership
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	com.role.tmp <- community.role.measures(g, membership)
	com.role.vals <- com.role.tmp$Values
	com.role.times <- com.role.tmp$Timing + duration
	node.res <- cbind(node.res, com.role.vals)
	node.time <- cbind(node.time, com.role.times)
	colnames(node.res)[(ncol(node.res)-ncol(com.role.vals)+1):ncol(node.res)] <- colnames(com.role.vals)
	colnames(node.time)[(ncol(node.time)-ncol(com.role.times)+1):ncol(node.time)] <- colnames(com.role.times)
	

	res$Timing <- node.time
	return(res)
}

node_res <- compute_node_features(g)



write.table(x=node_res$Timing, file=res.node.file, row.names=FALSE, col.names=TRUE)
