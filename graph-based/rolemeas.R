###############################################################################
# Processes various measures related to community roles.
#
# References:
#	Guimerà & Amaral
#	  Functional cartography of complex metabolic networks 
#	  Nature, 2005, 433:895-900
#	  DOI: 10.1038/nature03288
# 	Dugué, Labatut, & Perez 
#	  A community role approach to assess social capitalists visibility in the Twitter network
#	  Social Network Analysis and Mining, 2015, 5:26
#	  DOI: 10.1007/s13278-015-0266-0
# 
# Version: 3
# Author: Vincent Labatut 2013-17
###############################################################################
library("igraph")

###############################################################################
# Processes the community role measures. 
#
# g: the graph to process.
# membership: integer vector representing the community id of each node in g.
#
# returns: a list of matrices whose cols and rows represent measures and nodes (resp.).
###############################################################################
community.role.measures <- function(g, membership) {	# process neighborhoods: each variable contains a list of integer vectors
	# each integer vector represents the neighborhood of a node (using the ids of its neighbors)
	neigh.all <- neighborhood(graph=g, order=1, nodes=V(g), mode="all")			# ignoring link directions
#	if(is.directed(g)) {
    	neigh.in <- neighborhood(graph=g, order=1, nodes=V(g), mode="in")		# incoming links only
		neigh.out <- neighborhood(graph=g, order=1, nodes=V(g), mode="out")		# outgoing links only
#	}
		
	# build new lists comparable to the previous ones, 
	# except each node id is replaced by the id of the community containing the node
	start.time <- Sys.time()
		com.all <- list()
		com.in <- list()
		com.out <- list()
		for(u in 1:vcount(g))								# for each one in the graph
		{	nall <- neigh.all[[u]][neigh.all[[u]]!=u]		# we remove the node of interest from its own neighborhood
			com.all[[u]] <- membership[nall]				# we retrieve the community ids of the remaining nodes
#			if(is.directed(g))
			{	nin <- neigh.in[[u]][neigh.in[[u]]!=u]		# same for the incoming neighborhood
				com.in[[u]] <- membership[nin]
				nout <- neigh.out[[u]][neigh.out[[u]]!=u]	# same for the outgoing one
				com.out[[u]] <- membership[nout]
			}
		}
	end.time <- Sys.time()
	preproc.duration <- difftime(end.time,start.time,units="s")
		
#	print(com.all);print(com.in);print(com.out) # debug	
	
	# process the undirected role measures
	result <- process.original.guimera.amaral(membership, com.all)
	tmp <- process.undirected.dulape(membership, com.all)
	result$Values <- cbind(result$Values, tmp$Values)
	result$Timing <- cbind(result$Timing, tmp$Timing+preproc.duration)
	
	# process the directed ones (provided the graph is directed)
#	if(is.directed(g))
	{	# Guimera & Amaral
		tmp <- process.directed.guimera.amaral(membership, com.in, com.out)
		result$Values <- cbind(result$Values, tmp$Values)
		result$Timing <- cbind(result$Timing, tmp$Timing+preproc.duration)
		# Dugue, Labatut & Perez
		tmp <- process.directed.dulape(membership, com.in, com.out)
		result$Values <- cbind(result$Values, tmp$Values)
		result$Timing <- cbind(result$Timing, tmp$Timing+preproc.duration)
	}
	
	return(result)
}



###############################################################################
# Computes the community z-score, i.e. the z-score of a given value for each
# node, but processed relatively to the node community (by opposition to the
# whole network. This method is used to process most of the community role
# measures.
#
# values: a numerical vector containing (for each node) the values to consider.
# membership: communities of the nodes.
#
# returns: the z-score for the specified values and community.
###############################################################################
process.community.zscore <- function(values, membership)
{	# init result vector
	result <- rep(NA,length(values))
	# get existing com ids
	coms <- sort(unique(membership))
	
	# for each community
	for(i in 1:length(coms))
	{	com <- coms[i]
		
		# identify the nodes belonging to this community
		idx <- which(membership==com)
		
		# process the z-score of the specified values, for this community
		result[idx] <- scale(values[idx])	
	}
	
	# specific handling of zero stdev case (thus generalizing the z-score)
	result[is.nan(result)] <- 0
	return(result)
}




###############################################################################
# Processes a generic version of Guimera & Amaral's Participation coefficient,
# for the specified nodes. Each node is described by an integer vector corresponding
# to the community ids of its neighbors. The parameter is therefore a list of such
# integer vectors.
#
# neigh.coms: community ids of the node neighbors, as a list of integer vectors (one
#			  for each node).
#
# returns: a numerical vector containing the participation coefficient obtained for
#		   each node.
###############################################################################
process.generic.participation.coeff <- function(neigh.coms)
{	# for each node
	result <- sapply(neigh.coms, function(coms)
	{	res <- 0
		
		# if no neighbor: the value is zero
		if(length(coms)>0)
		{	# compute community frequence among neighbors, and take the square of each resulting count
			numerator <- (table(coms))^2							
			
			# take the neighborhood size (squared again) and dupplicate to get a vector of same length
			denominator <- rep((length(coms))^2,length(numerator))
			
			# divide both vectors (term by term), sum the terms of the resulting vector, and take the complement to one
			res <- 1 - sum(numerator/denominator) 
		}
		
		return(res)
	})
	
	return(result)
}



###############################################################################
# Processes a generic version of the in/external degree, for the specified nodes. 
# Each node is described by an integer vector corresponding to the community ids 
# of its neighbors, and by its own community id.
#
# membership: community id of each node, as an integer vector.
# neigh.coms: community ids of the node neighbors, as a list of integer vectors (one
#			  for each node).
# internal: TRUE to process the internal degree, FALSE for the external one.
#
# returns: a numerical vector containing the in/external degree obtained for each node.
###############################################################################
process.generic.community.degree <- function(membership, neigh.coms, internal)
{	# process the internal degree of for each node u
	result <- sapply(1:length(membership), function(u)
	{	# get the community ids of the neighbors
		coms <- neigh.coms[[u]]
		
		# get the community id of the node of interest
		own.com <- membership[u]
		
		# internal degree: count the number of neighbors in the same community
		if(internal)
			res <- length(which(coms==own.com))
		# otherwise, external: count the neighbors in other communities
		else
			res <- length(which(coms!=own.com))
		
		return(res)
	})
	
	return(result)
}



###############################################################################
# Processes a generic version of the standard deviation of the node connectivity, 
# for the specified nodes. # Each node is described by an integer vector corresponding 
# to the community ids of its neighbors, and by its own community id. This function
# determines the distribution of communities among the neighbors of a given node, and
# computes its standard deviation to characterize the said node.
#
# membership: community id of each node, as an integer vector.
# neigh.coms: community ids of the node neighbors, as a list of integer vectors (one
#			  for each node).
#
# returns: a numerical vector containing the stdev connectivity obtained for each node.
###############################################################################
process.generic.stdev.connectivity <- function(membership, neigh.coms)
{	# process the standard deviation of the external connectivity for each node u
	result <- sapply(1:length(membership), function(u)
	{	res <- 0

		# get the community ids of the neighbors
		coms <- neigh.coms[[u]]
		
		# if no neighbor: the value is zero
		if(length(coms)>0)
		{	# get the community id of the node of interest
			own.com <- membership[u]
			
			# index of the nodes *not* belonging to the same community
			idx <- which(coms!=own.com)
			
			# get the community frequence among them
			t <- table(coms[idx])
			
			# compute the standard deviation for these values
			res <- sd(t)
			
			# if the stdev is not defined, we use zero
			if(is.na(res))
				res <- 0
		}
		
		return(res)
	})
	
	return(result)
}



###############################################################################
# Processes a generic version of the number of neighboring communities, for the 
# specified nodes. Each node is described by an integer vector corresponding to 
# the community ids of its neighbors, and by its own community id. This function
# determines the number of communities among the neighbors of each node.
#
# membership: community id of each node, as an integer vector.
# neigh.coms: community ids of the node neighbors, as a list of integer vectors (one
#			  for each node).
#
# returns: a numerical vector containing the number of distinct communities among
# 		   the neighbors of each node.
###############################################################################
process.generic.nbr.neigh.com <- function(membership, neigh.coms)
{	# process the number of neighboring communities for each node u
	result <- sapply(1:length(membership), function(u)
	{	res <- 0
		
		# get the community ids of the neighbors
		coms <- neigh.coms[[u]]
		
		# if no neighbor: the value is zero
		if(length(coms)>0)
		{	# get the community id of the node of interest
			own.com <- membership[u]
			
			# index of the nodes *not* belonging to the same community
			idx <- which(coms!=own.com)
			
			# count the number of distinct communities among them
			res <- length(unique(coms[idx]))
		}
		
		return(res)
	})
}



###############################################################################
# Processes the original community role measures of Guimera & Amaral, designed 
# for undirected unweighted graphs.
# 
# membership: integer vector containing the community id of each node.
# com.all: list of integer vectors, each one containing the community ids of the
#		   neighbors of a given node.
#
# returns: a matrix containing as many rows as nodes, and 2 columns (one for each
#          G&A measure P & z).
###############################################################################
process.original.guimera.amaral <- function(membership, com.all)
{	names <- c("P", "z")															# names of the table columns
	vals <- matrix(nrow=length(membership),ncol=length(names))						# init result table
	times <- matrix(nrow=1,ncol=length(names))						# init time table
	colnames(vals) <- names															# setup column names
	colnames(times) <- names														
	
	# undirected participation coefficient P
	start.time <- Sys.time()
		vals[,"P"] <- process.generic.participation.coeff(com.all)					# the result go to the column "P" in the table
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"P"] <- duration
	
	# undirected z within-module degree
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.all, internal=TRUE)	# process the (undirected) internal degree
		vals[,"z"] <- process.community.zscore(values=k.int, membership)				# z is simply the z-score of the internal degree
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"z"] <- duration
	
	result <- list()
	result$Values <- vals
	result$Timing <- times
	return(result)
}



###############################################################################
# Processes the generalized version of the community role measures of Guimera & Amaral, 
# designed for directed unweighted graphs.
# 
# membership: integer vector containing the community id of each node.
# com.in: list of integer vectors, each one containing the community ids of the
#		  incoming neighbors of a given node.
# com.out: list of integer vectors, each one containing the community ids of the
#		   outgoing neighbors of a given node.
#
# returns: a matrix containing as many rows as nodes, and 4 columns (one for each
#          G&A measure P & z, in their outgoing and incoming versions).
###############################################################################
process.directed.guimera.amaral <- function(membership, com.in, com.out)
{	names <- c("P_in", "P_out", "z_in", "z_out")
	vals <- matrix(nrow=length(membership),ncol=length(names))						# init result table
	times <- matrix(nrow=1,ncol=length(names))						# init time table
	colnames(vals) <- names															# setup column names
	colnames(times) <- names														
	
	# incoming participation coefficient P_in
	start.time <- Sys.time()
		vals[,"P_in"] <- process.generic.participation.coeff(com.in)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"P_in"] <- duration
	# outgoing participation coefficient P_out
	start.time <- Sys.time()
		vals[,"P_out"] <- process.generic.participation.coeff(com.out)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"P_out"] <- duration
	
	# incoming within-module degree z_in
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.in, internal=TRUE)
		vals[,"z_in"] <- process.community.zscore(values=k.int, membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"z_in"] <- duration
	# outgoing within-module degree z_out
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.out, internal=TRUE)
		vals[,"z_out"] <- process.community.zscore(values=k.int, membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"z_out"] <- duration
	
	result <- list()
	result$Values <- vals
	result$Timing <- times
	return(result)
}



###############################################################################
# Processes the generalization of the role measures proposed by Dugé, Labatut &
# Perez, for undirected unweighted networks.  
#
# membership: integer vector containing the community id of each node.
# com.all: list of integer vectors, each one containing the community ids of the
#		   neighbors of a given node.
#
# returns: a matrix containing as many rows as nodes, and 4 columns (one for each
#          measure: internal and external intensities, heterogeneity and diversity).
###############################################################################
process.undirected.dulape <- function(membership, com.all) 
{	names <- c("I_int", "I_ext", "H", "D")
	vals <- matrix(nrow=length(membership),ncol=length(names))
	times <- matrix(nrow=1,ncol=length(names))
	colnames(vals) <- names
	colnames(times) <- names
	
	# internal intensity I_int
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.all, internal=TRUE)
		vals[,"I_int"] <- process.community.zscore(values=k.int,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_int"] <- duration
	
	# external intensity I_ext
	start.time <- Sys.time()
		k.ext <- process.generic.community.degree(membership, com.all, internal=FALSE)
		vals[,"I_ext"] <- process.community.zscore(values=k.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_ext"] <- duration
	
	# heterogeneity H
	start.time <- Sys.time()
		sd.ext <- process.generic.stdev.connectivity(membership, com.all)
		vals[,"H"] <- process.community.zscore(values=sd.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"H"] <- duration
	
	# diversity D
	start.time <- Sys.time()
		n.ext <- process.generic.nbr.neigh.com(membership, com.all)
		vals[,"D"] <- process.community.zscore(values=n.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"D"] <- duration
	
	result <- list()
	result$Values <- vals
	result$Timing <- times
	return(result)
}



###############################################################################
# Processes the generalization of the role measures proposed by Dugé, Labatut &
# Perez, for directed unweighted networks.  
#
# membership: integer vector containing the community id of each node.
# com.in: list of integer vectors, each one containing the community ids of the
#		  incoming neighbors of a given node.
# com.out: list of integer vectors, each one containing the community ids of the
#		   outgoing neighbors of a given node.
#
# returns: a matrix containing as many rows as nodes, and 8 columns (one for each
#          measure in its outgoing and incoming versions).
###############################################################################
process.directed.dulape <- function(membership, com.in, com.out) 
{	names <- c("I_int^in", "I_int^out", "I_ext^in", "I_ext^out", "H_in", "H_out", "D_in", "D_out")
	vals <- matrix(nrow=length(membership),ncol=length(names))						# init result table
	times <- matrix(nrow=1,ncol=length(names))						# init time table
	colnames(vals) <- names															# setup column names
	colnames(times) <- names														
	
	# incoming internal intensity I_int^in
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.in, internal=TRUE)
		vals[,"I_int^in"] <- process.community.zscore(values=k.int,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_int^in"] <- duration
	
	# outgoing internal intensity I_int-out
	start.time <- Sys.time()
		k.int <- process.generic.community.degree(membership, com.out, internal=TRUE)
		vals[,"I_int^out"] <- process.community.zscore(values=k.int,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_int^out"] <- duration
	
	# incoming external intensity I_ext^in
	start.time <- Sys.time()
		k.ext <- process.generic.community.degree(membership, com.in, internal=FALSE)
		vals[,"I_ext^in"] <- process.community.zscore(values=k.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_ext^in"] <- duration
	
	# outgoing external intensity I_ext^out
	start.time <- Sys.time()
		k.ext <- process.generic.community.degree(membership, com.out, internal=FALSE)
		vals[,"I_ext^out"] <- process.community.zscore(values=k.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"I_ext^out"] <- duration
	
	# incoming heterogeneity H_in
	start.time <- Sys.time()
		sd.ext <- process.generic.stdev.connectivity(membership, com.in)
		vals[,"H_in"] <- process.community.zscore(values=sd.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"H_in"] <- duration
	
	# outgoing heterogeneity H_out
	start.time <- Sys.time()
		sd.ext <- process.generic.stdev.connectivity(membership, com.out)
		vals[,"H_out"] <- process.community.zscore(values=sd.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"H_out"] <- duration
	
	# incoming diversity D_in
	start.time <- Sys.time()
		n.ext <- process.generic.nbr.neigh.com(membership, com.in)
		vals[,"D_in"] <- process.community.zscore(values=n.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"D_in"] <- duration
	
	# outgoing diversity D_out
	start.time <- Sys.time()
		n.ext <- process.generic.nbr.neigh.com(membership, com.out)
		vals[,"D_out"] <- process.community.zscore(values=n.ext,membership)
	end.time <- Sys.time()
	duration <- difftime(end.time,start.time,units="s")
	times[,"D_out"] <- duration
	
	result <- list()
	result$Values <- vals
	result$Timing <- times
	return(result)
}
