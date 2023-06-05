from database import db
import math
import numpy

class calculations:
	
	# calculates if the beta shows high or low volatility
	def beta_Volatility(self, beta):
		if 0 <= beta < 1:
			return 'Low Volatility'
		elif beta > 1:
			return 'High Volatility'
		elif beta == 1:
			return 'Same Volatility'
		elif beta < 0:
			return 'No Correlation'

	# calculates the ratio of the current price to the all time high and low and determines 
	def yearly_high_low_BullBear(self, high, low, current):
		current_to_high = (current / high)*100
		current_to_low = (current / low)*100
		if current_to_high >= 95:
			return 'Bearish'
		if current_to_low <= 1.05:
			return 'Bullish'
		else:
			return 'In between'

	# calculates whether peg ratio suggests stock is bearish or bullish
	def peg_ratio_BullBear(self, ratio):
		if ratio <= 1:
			return 'Bullish/Undervalued'
		elif ratio > 1:
			return 'Bearish/Overvalued'

	# calculates whether stock has dividends or not
	def dividend_yield_Volatility(self, dividend):
		if dividend == 0:
			return 'High Volatility'
		elif dividend > 0:
			return 'Low volatility'
	
	# determines the variation of the stock's prices and determines if it has high or low volatility
	def volatility_variation(self, prices):
		mean = numpy.mean(prices)
		stdev = numpy.std(prices)

		print(mean)
		print(stdev)
		variation = stdev / mean
		print(variation)

		if variation <= 1:
			return 'Low Volatility'
		if variation > 1:
			return 'High Volatility'


calc = calculations()

