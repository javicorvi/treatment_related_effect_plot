'''
Created on Jan 16, 2019

To run the file 
python plot.py -f1 servier/total_annotation_measurement.dat -f2 servier/documents_annotation_measurement.dat -outputDir servier

@author: jcorvi
'''
import pandas 
import sys
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
import logging
from matplotlib.pyplot import legend
from numpy.core.defchararray import capitalize

parser=argparse.ArgumentParser()
parser.add_argument('-f1', help='Total annotation measurement files')
parser.add_argument('-f2', help='Total documents annotation measurement files')
parser.add_argument('-outputDir', help='Output Dir, could be the EFPIA partner name')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import plot
    parameters = plot.ReadParameters(args)
    plot.plot_annotations_set_measurement()
    plot.plot_annotations_by_source()
    plot.plot_annotations_study_domain()
    plot.plot_annotations_by_year()
    
def ReadParameters(args):
    """Read the parameters of the module, see --help"""
    missing_parameter=False
    if(args.f1!=None):
        parameters['total_annotation_measurement']=args.f1
    else:
        missing_parameter=True
        logging.error("Please set the Total annotation measurement file, for more information --help ")
    if(args.f2!=None):
        parameters['documents_annotation_measurement']=args.f2
    else:
        missing_parameter=True
        logging.error("Please set the Total documents annotation measurement file, for more information --help ")
    if(args.outputDir!=None):
        parameters['outputDir']=args.outputDir + '/'
        if not os.path.exists(parameters['outputDir']):
            os.makedirs(parameters['outputDir'])
    else:
        missing_parameter=True
        logging.error("Please set the Output directory for the plots, for more information --help ")
        
    if(missing_parameter):
        logging.error("Please set the correct parameters before continue --help ")
        sys.exit(1)
        
    return parameters    

def plot_annotations_by_source():
    annotation_measurement_path = parameters['total_annotation_measurement']
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df_to_plot = df[(df[0]!='SENTENCES_TEXT') & (df[1]!='ORIGINAL MARKUPS') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
    df_grouped = df_to_plot[(df_to_plot[1]=='SEX') | (df_to_plot[1]=='MANIFESTATION_OF_FINDING') | (df_to_plot[1]=='STUDY_TESTCD') | (df_to_plot[1]=='STUDY_DOMAIN') | (df_to_plot[1]=='RISK_LEVEL')].groupby([1]).agg('sum').reset_index()
    df_default = df[(df[1]=='DEFAULT') & (df[0]!='SENTENCES_TEXT') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
    df_default = df_default.drop([1], axis=1)
    df_default.columns = [1, 2, 3 ,4, 5 ]
    frames = [df_grouped, df_default]
    df_to_plot = pandas.concat(frames)
    df_to_plot = df_to_plot.sort_values(by=[2],ascending=[0])
    df_to_plot[1] = [  el.replace('_',' ').replace(' ','\n',2).capitalize() for el in df_to_plot[1]]
    xdata=df_to_plot[1]
    #total = list(df_to_plot[2])
    cdisc = list(df_to_plot[3])
    etox = list(df_to_plot[4])
    manual = list(df_to_plot[5])
    
    barWidth=0.2
    
    r1 = np.arange(len(cdisc))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    plt.bar(r1, cdisc, color='b', width=barWidth, edgecolor='white', label='CDISC')
    plt.bar(r2, etox, color='g', width=barWidth, edgecolor='white', label='ETOX')
    plt.bar(r3, manual, color='r', width=barWidth, edgecolor='white', label='MANUAL')
    
    plt.xticks([r + barWidth for r in range(len(cdisc))], xdata,rotation=90 )
    
    plt.xlabel("Field")
    plt.legend()
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields by source')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(parameters['outputDir']+'annotations_by_source.png')
    #plt.show()
    plt.gcf().clear()
    
def plot_annotations_set_measurement():
    annotation_measurement_path = parameters['total_annotation_measurement']
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None, )
    df = df[df.columns[[0,1,2]]]
    df_to_plot = df[(df[0]!='SENTENCES_TEXT') & (df[1]!='ORIGINAL MARKUPS') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
    df_grouped = df_to_plot[(df_to_plot[1]=='SEX') | (df_to_plot[1]=='MANIFESTATION_OF_FINDING') | (df_to_plot[1]=='STUDY_TESTCD') | (df_to_plot[1]=='STUDY_DOMAIN') | (df_to_plot[1]=='RISK_LEVEL')].groupby([1])[2].agg('sum').reset_index()
    df_default = df[(df[1]=='DEFAULT') & (df[0]!='SENTENCES_TEXT') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
    df_default = df_default.drop([1], axis=1)
    df_default.columns = [1, 2]
    frames = [df_grouped, df_default]
    df_to_plot = pandas.concat(frames)
    df_to_plot = df_to_plot.sort_values(by=[2],ascending=[0])
    df_to_plot[1] = [  el.replace('_',' ').replace(' ','\n',2).capitalize() for el in df_to_plot[1]]
    
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=1, y=2, legend=False)
    ax.annotate(str(total) + ' terms mentions in total', xy=(0.8,0.9),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height()-1, str(i.get_height()), fontsize=10, color='black',ha='center')
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(parameters['outputDir']+ 'all_set_annotations.png')
    #plt.show()
    plt.gcf().clear()

def plot_annotations_study_domain():
    annotation_measurement_path = parameters['total_annotation_measurement']
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    df = df[df.columns[[0,1,2]]]
    df_to_plot = df[(df[1]=='STUDY_DOMAIN')]
    df_to_plot[3] = [el.replace('_DOMAIN','').replace('_','\n').capitalize() for el in df_to_plot[0]]
    df_to_plot = df_to_plot.sort_values(by=[2],ascending=[0])
    total = df_to_plot[2].sum()
    ax = df_to_plot.plot.bar(x=3, y=2 , legend=False)
    ax.annotate(str(total) + ' study domain terms mentions in total', xy=(0.70,0.90),xycoords='axes fraction', fontsize=10)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height()-1, str(i.get_height()), fontsize=10, color='black',ha='center')
    plt.title('Annotated Study Domains')
    plt.xlabel("Study Domain")
    plt.xticks(rotation=90)
    plt.ylabel("# Terms Mentions")
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(parameters['outputDir']+'study_domain.png')
    #plt.show()
    plt.gcf().clear()

    
def plot_annotations_by_year():
    annotation_measurement_path = parameters['documents_annotation_measurement']
    df = pandas.read_csv(annotation_measurement_path, sep='\t', header=None)
    tokens = df[(df[1]=='TOKENS_QUANTITY')]
    tokens[4] = [el[el.rfind('_')+1:] for el in tokens[0]]
    tokens_year = tokens.groupby([4])[3].agg('sum').reset_index()
    tokens_year[2] = tokens.groupby([4])[2].agg('count').reset_index()[2]
    print tokens_year
    tokens_year.columns = ['year','tokens','reports'] 
    df_to_plot = df[(df[2]!='ORIGINAL MARKUPS') & (df[2]!='GENERAL_DOCUMENT') ]
    df_to_plot = df_to_plot[(df_to_plot[2]=='SEX') | (df_to_plot[2]=='MANIFESTATION_OF_FINDING') | (df_to_plot[2]=='STUDY_TESTCD') | (df_to_plot[2]=='STUDY_DOMAIN') | (df_to_plot[2]=='RISK_LEVEL')]
    df_to_plot[4] = [el[el.rfind('_')+1:] for el in df_to_plot[0]]
    df_sum = df_to_plot.groupby([4])[3].agg('sum').reset_index()
    df_sum.columns = ['year','annotations'] 
    print df_sum
    df_to_plot = pandas.concat([tokens_year, df_sum['annotations']], axis=1, sort=False)
    df_to_plot['result'] = df_to_plot['tokens']/(df_to_plot['annotations']*100)
    print df_to_plot
    ax = df_to_plot.plot.bar(x='year', y='result', legend=False)
    index=0
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2., i.get_height(),  str(round(i.get_height(),2)), fontsize=10, color='black',ha='center')
        ax.text(i.get_x() + i.get_width()/2., 0.05,  df_to_plot.iloc[index]['reports'], fontsize=10, color='white',ha='center')
        index=index+1
    plt.xlabel("Years")
    plt.ylabel("Annotations % over tokens")
    plt.title('Annotated Fields, Annotations % over tokens by year')
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(parameters['outputDir']+'annotations_by_year.png')
    #plt.show()
    plt.gcf().clear()    
    
