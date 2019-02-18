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
import logging
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('-f1', help='Total annotation measurement files')
parser.add_argument('-f2', help='Total documents annotation measurement files')
parser.add_argument('-outputDir', help='Output Dir, could be the EFPIA partner name')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import plot_multiefpia_comparation
    parameters = plot_multiefpia_comparation.ReadParameters(args)
    
    total_annotation_measurement = parameters['total_annotation_measurement'].split(",")
    documents_annotation_measurement = parameters['documents_annotation_measurement'].split(",")
    if(len(total_annotation_measurement)!=len(documents_annotation_measurement)):
        logging.error("The numbers of total field and document files have to be the same.")
       
    #for path1,path2 in zip(total_annotation_measurement,documents_annotation_measurement):
    plot_multiefpia_comparation.plot_annotations_set_measurement(total_annotation_measurement,['Bayer','Sanofi','Servier'],['b','r','g'])
    #plot_multiefpia_comparation.plot_annotations_study_domain(documents_annotation_measurement)
       
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


    
def plot_annotations_set_measurement(annotation_measurement_paths,efpias,colors):
    
    list_to_plot = []
    for path1,efpia,c in zip(annotation_measurement_paths,efpias,colors):
        values=[]
        df = pandas.read_csv(path1, sep='\t', header=None)
        df = df[df.columns[[0,1,2]]]
        df_to_plot = df[(df[0]!='SENTENCES_TEXT') & (df[1]!='ORIGINAL MARKUPS') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
        df_grouped = df_to_plot[(df_to_plot[1]=='SEX') | (df_to_plot[1]=='MANIFESTATION_OF_FINDING') | (df_to_plot[1]=='STUDY_TESTCD') | (df_to_plot[1]=='STUDY_DOMAIN') | (df_to_plot[1]=='RISK_LEVEL')].groupby([1])[2].agg('sum').reset_index()
        df_default = df[(df[1]=='DEFAULT') & (df[0]!='SENTENCES_TEXT') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
        df_default = df_default.drop([1], axis=1)
        df_default.columns = [1, 2]
        frames = [df_grouped, df_default]
        df_to_plot = pandas.concat(frames)
        df_to_plot.columns=['key','value']
        
        #Get Specific fields for plot
        xdata=['Anatomy','Study Domain', 'Sex', 'Study Test', 'Specimen', 'Route of Administration', 'Species', 'Dose', 'Group', 'Manifestation of Finding', 'Mode of Action',  \
               'Treatment Related Term', 'Strain','No Treatment Related Term',  'Statical Significance', 'Risk Level' ]
        values.append(getFieldValue(df_to_plot, 'ANATOMY'))
        values.append(getFieldValue(df_to_plot, 'STUDY_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'SEX'))
        values.append(getFieldValue(df_to_plot, 'STUDY_TESTCD'))
        values.append(getFieldValue(df_to_plot, 'SPECIMEN'))
        values.append(getFieldValue(df_to_plot, 'ROUTE_OF_ADMINISTRATION'))
        values.append(getFieldValue(df_to_plot, 'SPECIES'))
        values.append(getFieldValue(df_to_plot, 'DOSE'))
        values.append(getFieldValue(df_to_plot, 'GROUP'))
        values.append(getFieldValue(df_to_plot, 'MANIFESTATION_OF_FINDING'))
        values.append(getFieldValue(df_to_plot, 'MODE_OF_ACTION'))
        values.append(getFieldValue(df_to_plot, 'TREATMENT_RELATED_EFFECT_DETECTED'))
        values.append(getFieldValue(df_to_plot, 'STRAIN'))
        values.append(getFieldValue(df_to_plot, 'NO_TREATMENT_RELATED_EFFECT_DETECTED'))
        values.append(getFieldValue(df_to_plot, 'STATICAL_SIGNIFICANCE'))
        values.append(getFieldValue(df_to_plot, 'RISK_LEVEL'))
        list_to_plot.append([values, efpia, c])

        
        
        '''df_to_plot['key'] = [  el.replace('_',' ').replace(' ','\n',2).capitalize() for el in df_to_plot['key']]
        total = df_to_plot['value'].sum()'''
    barWidth=0.2    
    in_ = 0    
    for row in list_to_plot:
        values = row[0]
        label  = row[1]
        color = row[2]
        if(in_==0):
            r1 = list(np.arange(len(values)))
            in_=1
        else:    
            r1 = [x + barWidth for x in r1]
        plt.bar(r1, values, color=color, width=barWidth, edgecolor='white', label=label)
    
    
    plt.xticks([r + barWidth for r in range(len(values))], xdata, rotation=90 )
    '''        
    xdata=df_to_plot[1]
    cliente1 = list(df_to_plot[2])
    cliente2 = list(df_to_plot[2])
    cliente3 = list(df_to_plot[2])
    
    
    
    r1 = np.arange(len(cliente1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    plt.bar(r1, cliente1, color='b', width=barWidth, edgecolor='white', label='Bayer')
    plt.bar(r2, cliente2, color='g', width=barWidth, edgecolor='white', label='Sanofi')
    plt.bar(r3, cliente3, color='r', width=barWidth, edgecolor='white', label='Servier')
    '''
    
    plt.legend()
    plt.xlabel("Field")
    plt.ylabel("# Terms Mentions")
    plt.title('Annotated Fields')
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(parameters['outputDir']+ 'all_set_annotations.png')
    plt.show()
    plt.gcf().clear()

def getFieldValue(df, fieldName):
    df_ = df[df['key']==fieldName]
    if(len(df_)!=0):
        v = df_.get_value(df_.index[0],'value')
    else:
        v = 0
    return v
    

def plot_annotations_study_domain(annotation_measurement_path):
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

    

    
