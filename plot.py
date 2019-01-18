'''
Created on Jan 16, 2019

@author: jcorvi
'''
import pandas 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import legend

if __name__ == '__main__':
    import plot
    plot.plot_annotations_set_measurement()
    #plot.plot_annotations_individual_measurement()
    plot.plot_annotations_study_domain()
    plot.plot_annotations_by_year()
def plot_annotations_individual_measurement():
    annotation_measurement_path = '/home/jcorvi/Documents/total_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df_to_plot = df[(df[1]!='ORIGINAL MARKUPS')]
    #df = df[1]=='STUDY_DOMAIN'
    #df = pandas.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    ax = df_to_plot.plot.bar(x=0, y=2, legend=False)
    for i in ax.patches:
        ax.text(i.get_x()+.1, i.get_height()-1, str(i.get_height()), fontsize=8, color='black')
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields, 46 Bayer study reports')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(18.5, 10.5)
    plt.savefig('/home/jcorvi/Documents/all_individual_annotations.png')
    #plt.show()
    plt.gcf().clear()
    
def plot_annotations_set_measurement():
    annotation_measurement_path = '/home/jcorvi/Documents/total_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df_to_plot = df[(df[1]!='ORIGINAL MARKUPS')]
    df_grouped = df_to_plot[(df_to_plot[1]=='SEX') | (df_to_plot[1]=='MANIFESTATION_OF_FINDING') | (df_to_plot[1]=='STUDY_DOMAIN') | (df_to_plot[1]=='RISK_LEVEL')].groupby([1])[2].agg('sum').reset_index()
    df_default = df[(df[1]=='DEFAULT')]
    df_default = df_default.drop([1], axis=1)
    df_default.columns = [1, 2]
    frames = [df_grouped, df_default]
    df_to_plot = pandas.concat(frames)
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=1, y=2, legend=False)
    ax.annotate(str(total) + ' terms mentions in total', xy=(0.8,0.9),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height()-1, str(i.get_height()), fontsize=10, color='black',ha='center')
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields, 46 Bayer study reports')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 8.5)
    plt.savefig('/home/jcorvi/Documents/all_set_annotations.png')
    #plt.show()
    plt.gcf().clear()

def plot_annotations_study_domain():
    annotation_measurement_path = '/home/jcorvi/Documents/total_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df_to_plot = df[(df[1]=='STUDY_DOMAIN')]
    df_to_plot[3] = [el.replace('_DOMAIN','') for el in df_to_plot[0]]
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=3, y=2 , legend=False)
    ax.annotate(str(total) + ' study domain terms mentions in total', xy=(0.70,0.90),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height()-1, str(i.get_height()), fontsize=10, color='black',ha='center')
    plt.title('Annotated Study Domains, 46 Bayer study reports')
    plt.xlabel("Study Domain")
    plt.xticks(rotation=90)
    plt.ylabel("# Terms Mentions")
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(15.5, 8.5)
    plt.savefig('/home/jcorvi/Documents/study_domain.png')
    #plt.show()
    plt.gcf().clear()
    
def plot_annotations_by_year():
    annotation_measurement_path = '/home/jcorvi/Documents/documents_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    
    #sentences = df[(df[1]=='SENTENCES_QUANTITY')]
    tokens = df[(df[1]=='TOKENS_QUANTITY')]
    tokens[4] = [el[el.rfind('_')+1:] for el in tokens[0]]
    tokens_year = tokens.groupby([4])[3].agg('sum').reset_index()
    tokens_year.columns = ['year','tokens'] 
    print tokens_year
    df_to_plot = df[(df[2]!='ORIGINAL MARKUPS') & (df[2]!='GENERAL_DOCUMENT') ]
    
    df_to_plot = df_to_plot[(df_to_plot[2]=='SEX') | (df_to_plot[2]=='MANIFESTATION_OF_FINDING') | (df_to_plot[2]=='STUDY_DOMAIN') | (df_to_plot[2]=='RISK_LEVEL')]
    df_to_plot[4] = [el[el.rfind('_')+1:] for el in df_to_plot[0]]
    df_sum = df_to_plot.groupby([4])[3].agg('sum').reset_index()
    df_sum.columns = ['year','annotations'] 
    print df_sum
    
    df_to_plot = pandas.concat([tokens_year, df_sum['annotations']], axis=1, sort=False)
    df_to_plot['result'] = df_to_plot['tokens']/(df_to_plot['annotations']*100)
    print df_to_plot
    
    ax = df_to_plot.plot.bar(x='year', y='result', legend=False)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height(),  str(round(i.get_height(),2)), fontsize=10, color='black',ha='center')
    
    plt.xlabel("Years")
    plt.ylabel("Annotations % over tokens")
    plt.title('Annotated Fields, Annotations % over tokens by year')
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.gcf().set_size_inches(15.5, 8.5)
    plt.savefig('/home/jcorvi/Documents/annotations_by_year.png')
    #plt.show()
    plt.gcf().clear()    
    
