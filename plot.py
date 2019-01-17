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
    #plot.plot_annotations_set_measurement()
    #plot.plot_annotations_individual_measurement()
    #plot.plot_annotations_study_domain()
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
    plt.title('Annotated Fields')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.savefig('/home/jcorvi/Documents/all_individual_annotations.png')
    plt.show()
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
    ax.annotate(str(total) + ' terms mentions in total', xy=(0.8,0.8),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x()+.1, i.get_height()-1, str(i.get_height()), fontsize=8, color='black')
    
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.savefig('/home/jcorvi/Documents/all_set_annotations.png')
    plt.show()
    plt.gcf().clear()

def plot_annotations_study_domain():
    annotation_measurement_path = '/home/jcorvi/Documents/total_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df_to_plot = df[(df[1]=='STUDY_DOMAIN')]
    df_to_plot[3] = [el.replace('_DOMAIN','') for el in df_to_plot[0]]
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=3, y=2 , legend=False)
    ax.annotate(str(total) + ' study domain terms mentions in total', xy=(0.78,0.85),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x()+.1, i.get_height()-1, str(i.get_height()), fontsize=8, color='black')
    plt.title('Annotated Study Domains')
    plt.xlabel("Study Domain")
    plt.xticks(rotation=90)
    plt.ylabel("# Terms Mentions")
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.savefig('/home/jcorvi/Documents/study_domain.png')
    plt.show()
    plt.gcf().clear()
    
def plot_annotations_by_year():
    annotation_measurement_path = '/home/jcorvi/Documents/documents_annotation_measurement.dat'
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    
    sentences = df[(df[1]=='SENTENCES_QUANTITY')]
    tokens = df[(df[1]=='TOKENS_QUANTITY')]
    print tokens
    df_to_plot = df[(df[2]!='ORIGINAL MARKUPS') & (df[2]!='GENERAL_DOCUMENT') ]
    
    df_to_plot = df_to_plot[(df_to_plot[2]=='SEX') | (df_to_plot[2]=='MANIFESTATION_OF_FINDING') | (df_to_plot[2]=='STUDY_DOMAIN') | (df_to_plot[2]=='RISK_LEVEL')]
    df_to_plot[4] = [el[el.rfind('_')+1:] for el in df_to_plot[0]]
    df_sum = df_to_plot.groupby([4])[3].agg('sum').reset_index()
    df_to_plot = df_to_plot.drop([1,2,3], axis=1)
    df_count = df_to_plot.groupby([0,4]).count().reset_index().groupby(4).count().reset_index()
    df_to_plot = pandas.concat([df_count, df_sum[3]], axis=1, sort=False)
     
    df_to_plot['Result'] = df_to_plot[3]/df_to_plot[0]
    df_to_plot.columns = ['year','#reports','#annotations','average']
    print df_to_plot
    
    
    df_default = df[(df[1]=='DEFAULT')]
    df_default = df_default.drop([1], axis=1)
    df_default.columns = [1, 2]
    frames = [df_grouped, df_default]
    df_to_plot = pandas.concat(frames)
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=1, y=2, legend=False)
    ax.annotate(str(total) + ' terms mentions in total', xy=(0.8,0.8),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x()+.1, i.get_height()-1, str(i.get_height()), fontsize=8, color='black')
    
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.savefig('/home/jcorvi/Documents/all_set_annotations.png')
    plt.show()
    plt.gcf().clear()    
    
