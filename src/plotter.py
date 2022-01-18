import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input') # path to input file
	parser.add_argument('-t', '--type') # c - combined plot, t - two plots

	args = parser.parse_args()
	inputFile = args.input
	plot_type = args.type

	if inputFile == None:
		print('##################################')
		print('Must specify path to tsv file.')
		print('Run script again with -i argument.')
		print('##################################')
		quit()
	df = pd.read_csv(inputFile, delimiter="\t")

	# clean df
	df = df[['id', 'sentiment', 'category']]
	df = df[0:750]
	df = df[~(df['category'] == 'Remove')]

	return df, plot_type

def process(df, plot_type):

	counts = {}
	sentiments = ['Neutral', 'Negative', 'Positive']

	for cat in df['category'].unique():
		sentsDict = {}
		for sent in sentiments:
			sentsDict[sent] = len(df[np.logical_and(df['category'] == cat, df['sentiment'] == sent)])

		counts[cat] = sentsDict

	if plot_type == 'c': # combined plot
		df_counts_plotter = pd.DataFrame(counts)
		df_counts_plotter = df_counts_plotter.T

		return df_counts_plotter

	else:
		df_counts = pd.DataFrame()

		for key, val in counts.items():
			df_counts = df_counts.append([[key, 'Neutral', val['Neutral']]])
			df_counts = df_counts.append([[key, 'Negative', val['Negative']]])
			df_counts = df_counts.append([[ str(key), 'Positive', val['Positive']]])

		df_counts.columns = ['Category', 'Sentiment', 'Counts']

	return df_counts
def plot(df, plot_type):

	if plot_type == 'c':
		sns.set(rc = {'figure.figsize':(15,8)})
		df.plot(kind='bar', stacked=True, rot=0, title="Sentiment make-up by category", ax = plt.gca())
		plt.ylabel("Counts")
		plt.xlabel("Category")
		plt.legend(loc=1)
		plt.show()

	else:
		# first plot
		sns.set(rc = {'figure.figsize':(15,8)})
		plt.figure()
		ax1 = sns.barplot(x='Category', y='Counts', hue='Sentiment', data=df)
		ax1.set_title("Tweet sentiments by category")
		ax1.bar_label(ax1.containers[0])
		#plt.show()

		# second plot
		plt.figure()
		ax2 = sns.barplot(x='Category', y='Counts', data=df, ci=None, estimator=sum)
		ax2.set_title("Tweet count by category")
		ax2.bar_label(ax2.containers[0])
		plt.show()

def main():

	df_input, plot_type = parse()
	df = process(df_input, plot_type)
	plot(df, plot_type)


if __name__ == '__main__':
	main()
