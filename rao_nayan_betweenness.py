import sys
import string
import re
import json
import itertools
import collections
import glob
import os
import itertools
from decimal import *

bfset = set()
#document = str(sys.argv[1])


def bfs(graph, start):
	visited, queue = set(), [start]
	while queue:
		vertex = queue.pop(0)
		if vertex not in visited:
			visited.add(vertex)
			queue.extend(graph[vertex])
	#print visited
	#print " "

def generate_edges(graph):
	edges1 = []
	for node in graph:
		for neighbour in graph[node]:
				edges.append((node, neighbour))

def predictMovieRating(movie, similarity, MovieUser):
	rated_movies = MovieUser[USER].keys()
	rated_movie_pairs =[]
	for rated_movie in rated_movies:
		rated_movie_pairs.append(tuple(sorted([movie, rated_movie])))
	relevant_similarity =[]
	for wij in rated_movie_pairs:
		relevant_similarity.append((wij, similarity[wij]))
	relevant_similarity = sorted(relevant_similarity,key=lambda x: x[0])
	relevant_similarity = sorted(relevant_similarity, key=lambda x: x[1], reverse=True)
	if len(relevant_similarity)>N:
		relevant_similarity = relevant_similarity[0:N]
	neighbourhood_movie=[]
	for wij in relevant_similarity:
		neighbourhood_movie.append(wij[0][(wij[0].index(movie)-1)%2])	
	numerator_fraction =0
	for n_movie,win in zip(neighbourhood_movie, relevant_similarity):
		numerator_fraction+= (MovieUser[USER][n_movie] * similarity[win[0]])
	denominator_fraction=0
	for win in relevant_similarity:
		denominator_fraction+= abs(similarity[win[0]])
	if denominator_fraction==0:
		return 0
	else:
		return numerator_fraction/denominator_fraction

def iterative_bfs(graph, start):
	'''iterative breadth first search from start'''
	bfs_tree = {start: {"parents":[], "children":[], "level":0}}
	q = [start]
	while q:
		current = q.pop(0)
		for v in graph[current]:
			if not v in bfs_tree:
				bfs_tree[v]={"parents":[current], "children":[], "level": bfs_tree[current]["level"] + 1}
				bfs_tree[current]["children"].append(v)
				q.append(v)
			else:
				if bfs_tree[v]["level"] > bfs_tree[current]["level"]:
					bfs_tree[current]["children"].append(v)
					bfs_tree[v]["parents"].append(current)
	#for node in bfs_tree:
	#	level = max(bfs_tree[node]["level"])
	level = max([bfs_tree[node]["level"] for node in bfs_tree])
	node_values = {node:1.0 for node in graph}
	temp_betweenness = {}
	while level != 0:
		for node in [node for node in bfs_tree if bfs_tree[node]["level"]==level]:
			for parent in bfs_tree[node]["parents"]:
				value = node_values[node] / len(bfs_tree[node]["parents"])
				node_values[parent] = node_values[parent]+value
				temp_betweenness[tuple(sorted([node, parent]))] = value
		level=level-1
	return temp_betweenness

def recursive_dfs(graph, start, path=[]):
  '''recursive depth first search from start'''
  path=path+[start]
  for node in graph[start]:
    if not node in path:
      path=recursive_dfs(graph, node, path)
  return path

def iterative_dfs(graph, start, path=[]):
  '''iterative depth first search from start'''
  q=[start]
  while q:
    v=q.pop(0)
    if v not in path:
      path=path+[v]
      q=graph[v]+q
  return path

document = str(sys.argv[1])
edges = []
afinnfile = open(document)
for line in afinnfile:
	line = line.strip()
	linelist = line.split(" ")
	edges.append(sorted([int(x) for x in linelist]))
	

betweenness ={}
for edge in edges:
	betweenness.update({tuple(edge):0}) 

graph = {}
for nodes in edges:
	if nodes[0] not in graph:
		graph[int(nodes[0])] = []
	if nodes[1] not in graph:
		graph[int(nodes[1])] = []
	graph[int(nodes[0])].append(int(nodes[1]))
	graph[int(nodes[1])].append(int(nodes[0]))

for node in graph:
	temp_betweenness = iterative_bfs(graph, node)
	for edge in temp_betweenness:
		betweenness[edge] += temp_betweenness[edge]

for edge in betweenness: # divid by 2 to get correct answer
	betweenness[edge] = betweenness[edge]/2.0
#print betweenness
for edge in sorted(betweenness):
	print [edge[0],edge[1]],betweenness[edge]
#for edge in edges:
#	print "{0} {1}".format(edge, betweenness[tuple(sorted(edge))])





