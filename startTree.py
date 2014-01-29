#!/usr/bin/evn python

import sys
import AccuracyCalc as AC

def main():
	"""Initiate program"""
	prune = False
	if len(sys.argv) == 3:
		prune = (not not sys.argv[2])
	a = AC.AccCalculator(sys.argv[1], prune)
	a.analyze()

if __name__ == '__main__':
	main()
