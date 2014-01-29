import math
import operator
"""import chi"""

class Leaf:
	def __init__(self, class_label):
		"""represents class label"""
		self.class_label = class_label

	def choose(self, example = None):
		"""returns the class label"""
		return self.class_label

	def numNodes(self):
		"""number of nodes in Leaf equals 1"""
		return 1

	def visualize(self, d):
		"""visualize leaf"""
		return "%s\n" % (self.class_label)

	def leaf(self):
		"""states this is a leaf"""
		return True

class branch:
		def __init__(self, attribute):
			"""a decision node"""
			self.attribute = attribute
			self.children = {}

		def add_child(self, val, node):
			"""adds a child node for specified attribute value"""
			self.children[val] = node

		def choose(self, example):
			"""chooses a label based on the example's attribute"""
			return self.select_child(example).choose(example)

		def select_child(self, example):
			"""returns child based on attribute of node"""
			return self.children[example[self.attribute]]

		def numNodes(self):
			num = 1
			for k, val in self.children.items():
				num += val.numNodes()
			return num

		def visualize(self, d = 1):
			"""visualize tree"""
			s = "%i\n" % (self.attribute)
			for k,v in self.children.items():
				s = "%s%s%s: %s" % (s, " " * d, k, v.visualize(d+1))
			return s

		def all_leaves(self):
			"""returns true if all children are leaves"""
			for child in self.children.values():
				if not child.leaf():
					return False

			return True

		def leaf(self):
			"""Not a leaf"""
			return False

class treeBuilder:
	def __init__(self):
		"""figure this out"""
		"""self.chi = chi.Chi() """
		self.stop = False
		self.bestContinuous = False
		self.numSplits = 0

	def create(self, examples, atts, prune=False):
		"""create the full decision tree"""
		"""attributes = atts.keys()
		for j in attributes[:]:
			csplits = self.split_on_class(examples,j)
			mode0 = self.attr_mode(csplits,0)
			mode1 = self.attr_mode(csplits,1)
			mode2 = self.attr_mode(csplits,2)
			for a in atts:
				if a == "?":
					print "? found"""
		return self.DTL(examples, atts.keys(), examples, atts, prune)

	def DTL(self, examples, attributes, parents, attr_vals, prune):
		if len(examples) == 0:
			""" return default? define default?"""
			l = Leaf(self.mode(parents))
			return l
		elif self.sameClassification(examples):
			l = Leaf(examples[0][-1])
			return l
		elif len(attributes) == 0:
			l = Leaf(self.mode(examples))
			return l
		else:
			best = self.choose_attribute(attributes, examples)
			if self.stop == False:
				attribute_subset = attributes[:]
				for ex in examples:
					if '?' in ex:
						examples.remove(ex)
						#a = self.mode(attribute_subset)
				attribute_subset.remove(best)
				d_tree = branch(best)
				if self.bestContinuous:
					splits = self.continuous_split(examples, best)
				else:
					splits = self.split(examples, best)
				self.numSplits+=1
				values = attr_vals[best][:]
				for key, example_subset in splits.items():
					d_tree.add_child(key, self.DTL(example_subset, attribute_subset, examples, attr_vals, prune))
					if key in values:
						values.remove(key)
				for value in values:
					d_tree.add_child(value, Leaf(self.mode(examples)))
				if prune and d_tree.all_children_leaves():
					"""prune"""
			
			return d_tree
	
	def split(self, examples, best):
		"""splits examples from each other based on its value for best attribute"""
		splits = {}
		for example in examples:
			key = example[best]
			if splits.get(key):
				splits.get(key).append(example)
			else:
				splits[key] = [example]
		return splits

	def continuous_split(self, examples, best):
		ex_sort = sorted(examples, key=lambda ex: ex[best])
		print "best: " + repr(best)
		print "examples"
		print ex_sort
		count = len(ex_sort)-2
		j = 0
		cont_entropy = 0
		best_entropy = 2
		best_split_set = {}
		for j in range(0,count):
			splits = {}
			ex_index = 0	
			for ex in ex_sort:
				#print "ex index: " + repr(ex_index)
				key1 = j
				key2 = j+1
				#print "key1: " + repr(key1)
				#print "key2: " + repr(key2)

				if ex_index == 0:
					splits[key1] = [ex]
				elif ex_index <= key1:
					splits.get(key1).append(ex)
				elif ex_index == key2:
					splits[key2] = [ex]
				#	print "key2 initialized"
				#	print splits[key2]
				else:
					splits.get(key2).append(ex)
				#	print "key 2 appended"
				#	print splits[key2]

				ex_index += 1
			print "key 1 = " + repr(key1) + "; key2 = " + repr(key2)
			print "split 1: " + repr(splits[key1])
			print "split 2: " + repr(splits[key2])
			for k, val in splits.items():
				en = self.entropy_all(val)
				cont_entropy += en*len(val)/float(len(ex_sort))

			if cont_entropy < best_entropy:
				best_entropy = cont_entropy
				best_split_set = splits
		return jk

	def mode(self, examples):
		"""returns the mode class label for examples"""
		"""edit variable names"""
		majority = examples[0][1]
		counts = {majority: 0}
		for row in examples:
			label = row[-1]
			if counts.get(label):
				counts[label]+=1
				if counts[label] > counts[majority]:
					majority = label
			else:
				counts[label]=0
		return majority



	def sameClassification(self, examples):
		"""returns true if all examples have the same classification"""
		classification = None
		for row in examples:
			if not classification:
				classification = row[-1]
			elif classification != row[-1]:
				return False
		return True 

	def choose_attribute(self, attributes, examples):
		"""calculates entropy change and decides next best attribute"""
		best = attributes[0]
		best_change = self.entropy_change(examples,0)
		for a in attributes[1:]:
			change = self.entropy_change(examples, a)
			if change > best_change:
				best = a
				best_change = change
		if best_change == 0:
			self.stop = True
		self.lastChange = best_change

		if best >2 and best <8:
			"""this is a nominal attribute"""
			self.bestContinuous = False
		else:
			self.bestContinuous = True

		return best

	def entropy_change(self,examples, attribute):
		return self.entropy_all(examples) - self.entropy_part(examples,attribute)

	def entropy_all(self, examples):
		"""return entropy of unpartitioned example set"""
		all_counts = {}
		for example in examples:
			if all_counts.get(example[-1]):
				all_counts[example[-1]]+=1
			else:
				all_counts[example[-1]] = 1
		return self.entropy(all_counts,len(examples))

	def entropy_part(self, examples, attribute):
		"""return entropy of examples partitioned based on attribute"""
		splits = self.split(examples,attribute)
		entropy_part = 0
		for k, val in splits.items():
			en = self.entropy_all(val)
			entropy_part += en*len(val)/float(len(examples))
		return entropy_part

	def entropy(self, all_counts, num_ex):
		"""return entropy calculation"""
		entropy = 0
		for label, count in all_counts.items():
			h = 0
			p = count/float(num_ex)
			if p != 0:
				h = p*math.log(p,2)
			entropy += h
		return h*-1
	
	
