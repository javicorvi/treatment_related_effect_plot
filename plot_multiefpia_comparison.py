'''
Created on Jan 16, 2019

To run the file 
python plot_multiefpia_comparison.py -f1 bayer/total_annotation_measurement.dat,sanofi/total_annotation_measurement.dat,servier/total_annotation_measurement.dat -f2 bayer/documents_annotation_measurement.dat,sanofi/documents_annotation_measurement.dat,servier/documents_annotation_measurement.dat -outputDir multoefpia

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
    import plot_multiefpia_comparison
    parameters = plot_multiefpia_comparison.ReadParameters(args)
    
    
    parameters['total_annotation_measurement'] = "bayer/total_annotation_measurement.dat,servier/total_annotation_measurement.dat"
    efpias=['Bayer','Servier']
    #['Bayer','Sanofi','Servier']
    #['b','r','g']
    colors = ['b','g']
    
    total_annotation_measurement = parameters['total_annotation_measurement'].split(",")
    documents_annotation_measurement = parameters['documents_annotation_measurement'].split(",")
    if(len(total_annotation_measurement)!=len(documents_annotation_measurement)):
        logging.error("The numbers of total field and document files have to be the same.")
       
    #for path1,path2 in zip(total_annotation_measurement,documents_annotation_measurement):
    plot_multiefpia_comparison.plot_annotations_set_measurement(total_annotation_measurement, parameters['outputDir']+ 'all_set_annotations_percentage.png',efpias,colors,True)
    plot_multiefpia_comparison.plot_annotations_set_measurement(total_annotation_measurement,parameters['outputDir']+ 'all_set_annotations_quantity.png',efpias,colors,False)
    plot_multiefpia_comparison.plot_annotations_study_domain(total_annotation_measurement,parameters['outputDir']+ 'study_domain_percentage.png',efpias,colors,True)
    plot_multiefpia_comparison.plot_annotations_study_domain(total_annotation_measurement,parameters['outputDir']+ 'study_domain_quantity.png',efpias,colors,False)   
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


    
def plot_annotations_set_measurement(annotation_measurement_paths, output,efpias,colors, percentage=True):
    list_to_plot = []
    for path1,efpia,c in zip(annotation_measurement_paths,efpias,colors):
        values=[]
        df = pandas.read_csv(path1, sep='\t', header=None)
        df = df[df.columns[[0,1,2]]]
        df_to_plot = df[(df[0]!='SENTENCES_TEXT') & (df[1]!='ORIGINAL MARKUPS') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
        df_grouped = df_to_plot[(df_to_plot[1]=='SEX') | (df_to_plot[1]=='MANIFESTATION_FINDING') | (df_to_plot[1]=='STUDY_TESTCD') | (df_to_plot[1]=='STUDY_DOMAIN') | (df_to_plot[1]=='RISK_LEVEL')].groupby([1])[2].agg('sum').reset_index()
        df_default = df[(df[1]=='DEFAULT') & (df[0]!='SENTENCES_TEXT') & (df[0]!='TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE') & (df[0]!='NO_TREATMENT_RELATED_EFFECT_DETECTED_SENTENCE')]
        df_default = df_default.drop([1], axis=1)
        df_default.columns = [1, 2]
        frames = [df_grouped, df_default]
        df_to_plot = pandas.concat(frames)
        df_to_plot.columns=['key','value']
        if(percentage==True):
            tokens_df = df[(df[0]=='TOKENS_QUANTITY')]
            tokens = float(tokens_df.get_value(tokens_df.index[0],2))
            df_to_plot['value'] = df_to_plot['value']/tokens
        #Get Specific fields for plot
        xdata=['Anatomy','Study Domain', 'Sex', 'Study Test', 'Specimen', 'Route of \nAdministration', 'Species', 'Dose', 'Group', 'Manifestation of \nFinding', 'Mode of \nAction',  \
               'Treatment \nRelated Term', 'Strain','No Treatment \nRelated Term',  'Statical \nSignificance', 'Risk Level' ]
        values.append(getFieldValue(df_to_plot, 'ANATOMY'))
        values.append(getFieldValue(df_to_plot, 'STUDY_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'SEX'))
        values.append(getFieldValue(df_to_plot, 'STUDY_TESTCD'))
        values.append(getFieldValue(df_to_plot, 'SPECIMEN'))
        values.append(getFieldValue(df_to_plot, 'ROUTE_OF_ADMINISTRATION'))
        values.append(getFieldValue(df_to_plot, 'SPECIES'))
        values.append(getFieldValue(df_to_plot, 'DOSE'))
        values.append(getFieldValue(df_to_plot, 'GROUP'))
        values.append(getFieldValue(df_to_plot, 'MANIFESTATION_FINDING'))
        values.append(getFieldValue(df_to_plot, 'MODE_OF_ACTION'))
        values.append(getFieldValue(df_to_plot, 'TREATMENT_RELATED_EFFECT_DETECTED'))
        values.append(getFieldValue(df_to_plot, 'STRAIN'))
        values.append(getFieldValue(df_to_plot, 'NO_TREATMENT_RELATED_EFFECT_DETECTED'))
        values.append(getFieldValue(df_to_plot, 'STATICAL_SIGNIFICANCE'))
        values.append(getFieldValue(df_to_plot, 'RISK_LEVEL'))
        list_to_plot.append([values, efpia, c])
    
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
    plt.legend()
    plt.xlabel("Field")
    if(percentage==True):
        plt.ylabel("Annotations % over tokens")
        plt.title('%  of term mentions annotated')
    else:
        plt.ylabel("# Terms Mentions")
        plt.title('# of term mentions annotated')
    
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(output)
    plt.show()
    plt.gcf().clear()

def getFieldValue(df, fieldName):
    df_ = df[df['key']==fieldName]
    if(len(df_)!=0):
        v = df_.get_value(df_.index[0],'value')
    else:
        v = 0
    return v
    

def plot_annotations_study_domain(annotation_measurement_paths, output, efpias,colors, percentage=True):
    list_to_plot = []
    xdata=['Clinical','Microscopic', 'Death \nDiagnosis', 'Food and Water \nConsumption', 'Fetal Pathology', 'Body Weight', 'Body Weight \nGain', 'Organ \nMeasurement', 'Cardiovascular', 'Behavioral','Macroscopic', 'ECG',  \
               'Respiratory', 'Pharmacokinetics','Laboratory']
    for path1,efpia,c in zip(annotation_measurement_paths,efpias,colors):
        values=[]
        df = pandas.read_csv(path1, sep='\t', header=None)
        df = df[df.columns[[0,1,2]]]
        df_to_plot = df[(df[1]=='STUDY_DOMAIN')]
        df_to_plot.columns=['key','source','value']
        tokens = df_to_plot['value'].sum()
        if(percentage==True):
            df_to_plot['value'] = df_to_plot['value']/tokens
        values.append(getFieldValue(df_to_plot, 'CLINICAL_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'MICROSCOPIC_FINDINGS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'DEATH_DIAGNOSIS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'FOOD_WATER_CONSUMPTION_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'FETAL_PATOLOGY_FINDINGS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'BODY_WEIGHT_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'BODY_WEIGHT_GAIN_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'ORGAN_MEASUREMENT_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'CARDIOVASCULAR_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'BEHAVIORAL_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'MACROSCOPIC_FINDINGS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'ECG_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'RESPIRATORY_FINDINGS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'PHARMACOKINETICS_PARAMETERS_DOMAIN'))
        values.append(getFieldValue(df_to_plot, 'LABORATORY_FINDINGS_DOMAIN'))
        list_to_plot.append([values, efpia, c])    
    
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
    plt.legend()
    plt.xlabel("Study Domain")
    plt.xticks(rotation=90)
    if(percentage==True):
        plt.ylabel("Annotations % over tokens")
        plt.title('%  of term mentions annotated')
    else:
        plt.ylabel("# Terms Mentions")
        plt.title('# of term mentions annotated')
    
    
    plt.gcf().subplots_adjust(bottom=0.40)
    plt.gcf().set_size_inches(16.5, 6.0)
    plt.savefig(output)
    plt.show()
    plt.gcf().clear()

    

    
