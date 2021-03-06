
# coding: utf-8

import os
import json
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import sys
from tabulate import tabulate

def format_dict(job0):
    tmp = job0['config']
    tmp['acc'] = job0['acc'][-1]
    tmp['val_acc'] = job0['val_acc'][-1]
    tmp['Top2'] = job0['val_Top2'][-1]
    tmp['val_Top2'] = job0['val_Top2'][-1]
    tmp['Top3'] = job0['Top3'][-1]
    tmp['val_Top3'] = job0['val_Top3'][-1]
    return tmp



def get_summary(root,print_summary=False,return_dframe=False):
    job_list = []
    started=0
    not_started=0
    accs={}
    dataframe={}
    cols = []
    for job in os.listdir(os.path.join(root,'jobs')):
        if 'job' in job:
            try:
                filename = os.listdir(os.path.join(root,'jobs',job,'logs'))[0]
                f = open(os.path.join(root,'jobs',job,'logs',filename),"r")
                job0 = json.loads(f.read())
                f.close()
                conf = job0['config']
                job0 = format_dict(job0)
                dataframe[job]=job0
                started+=1
                cols.append(job)
                os.system('tree '+root+'/jobs/'+job)
                print("\n#====================Model Summary===================#")
                print(job,conf)
                print("\n#== Best Accuracy: %f #==val_Top2: %f ==#\n\n"%(job0['val_acc'],job0['val_Top2']))
            except:
                not_started+=1
    print('Number of jobs started:%d'%(started))
    print('Number of jobs pending:%d'%(not_started))

    dataframe = pd.DataFrame(dataframe).T
    if print_summary:
        try: print(dataframe)
        except: print("couldn't load a dataframe")
    if return_dframe: return dataframe
    else: pass


def visualize(dframe,field,target):
    dframe[target] = pd.to_numeric(dframe[target])
    print('#======================================================#')
    print('\n'+str(field)+' vs '+str(target)+'\n')
    if type(dframe[field][0])!= str:
        dframe[field] = pd.to_numeric(dframe[field])
        print(dframe[[field,target]].T)
        #dframe.plot.scatter(x=field,y=target,logx=True)
        #plt.scatter(x=dframe[field],y=dframe[target],logx=True)
    else:
        print(dframe.groupby(field).mean()[target])
    pass

if __name__=="__main__":

    try:
        root = sys.argv[1]
    except:
        root = input("Enter project's root folder:")

    print('\n#==========================Project tree:====================================#\n')
  

    dframe = get_summary(root,return_dframe=True)
    print('#=========================================================#')
    '''
    hyperpar = str(input('\n\nEnter hyperpar name to compare with val_Top2,val_acc (or hit enter to compare all):')) or ['learning_rate','reg_rate','architecture','optimizers','num_layers','dense_layer_sizes','dropout']
    '''

    '''
    for h in hyperpar:
        print(h)
        visualize(dframe,h,'val_Top2')
        visualize(dframe,h,'val_acc')
    '''

    sorted_dframe = dframe[['val_acc','val_Top2','learning_rate','reg_rate']].sort_values('val_acc',ascending=False)
    print(tabulate(sorted_dframe,headers='keys',tablefmt='psql'))

    delete = input('delete least performing jobs? (y/n)')
    if delete=='y':
        k = int(input('how many from the best jobs to keep?'))
        jobs2keep = sorted_dframe.index[:k]
        print('keep: {}'.format(jobs2keep))
        jobs2delete = sorted_dframe.index[k:]
        for job in jobs2delete:
            if 'job' in job:
                print('--deleting folder {}'.format(job))
                os.system('rm -rf '+root+'/jobs/'+job)

    
    dframe = get_summary(root,return_dframe=True)
    
    sorted_dframe = dframe[['val_acc','val_Top2','learning_rate','reg_rate']].sort_values('val_acc',ascending=False)
    print(tabulate(sorted_dframe,headers='keys',tablefmt='psql'))


