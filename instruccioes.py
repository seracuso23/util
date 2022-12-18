# -*- coding: utf-8 -*-
"""Instruccioes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NYu85Shk1OXEcpyNRTbDLrdVDFIOSkv4
"""

# Commented out IPython magic to ensure Python compatibility.
# %reset

# Commented out IPython magic to ensure Python compatibility.
# %whos

import pandas as pd
import re
import numpy as np

pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('display.float_format',None)

var='saldomora'
var2='Fuente'
categorias=['Comercial','Bancaria']
funciones=['avg','max','sum']
lags=[1,3,6,12]
lags=sorted(lags)
lags_s= ['_'+sub+'M' for sub in [str(x) for x in lags]]

lags_s

"""## Numerica Categorica"""

var_comun_b_df_list=list()
funcion_p=['min','max','avg']
df_l=list()
var_total_list_3=list()
for categoria_x in categorias:
  var_total_list_2=list()
  for funcion_x in funciones:
    #print(categoria_x,funcion_x)
    nombre_l=list()
    query_l=list()
    lag_l=list()
    for lag_x in list(range(max(lags)+1))[1:]:
      #print(lag_x)
      query=f"{funcion_x}(case when {var2}='{categoria_x}' then {var} else 0 end)"
      nombre=f"{funcion_x}_{var}_{categoria_x}_{lag_x}M"
      lag=lag_x
      #print(query,lag_x,nombre)
      nombre_l.append(nombre)
      query_l.append(query)
      lag_l.append(lag)

    var_comun_p_df=pd.DataFrame({
        'Nombre': nombre_l,
        'Query': query_l,
        'Lag': lag_l
      })
    var_comun_p_df['Tipo']='comun'
    var_comun_p_df['Funcion']='sql'
    var_comun_p_df['a_p']='p'

    var_comun_a_df=var_comun_p_df.copy()
    var_comun_a_df=var_comun_a_df[var_comun_a_df.Lag.isin(lags)]
    var_comun_a_df['a_p']='a'
    var_comun_p_df['Nombre']='p_'+var_comun_p_df['Nombre']
    ## Acumulados para las variables puntuales
    nombre_l_p=list()
    query_l_p=list()
    funcion_l_p=list()
    lag_l_p=list()
    for ff in funcion_p:
      for lags_a in lags:
        var_a_list_1=var_comun_p_df[(var_comun_p_df.Lag<=lags_a) & (var_comun_p_df.Nombre.str.contains(categoria_x)) & (var_comun_p_df.Nombre.str.contains(funcion_x))]['Nombre'].to_list()
        var_a_concat=",".join(var_a_list_1)
        query_a=f'{ff}({var_a_concat})'
        nombre_aa=re.sub('_*([^_*]*)$','',var_a_list_1[0])
        nombre_a=f'{ff}_{nombre_aa}_{lags_a}M'
        nombre_l_p.append(nombre_a)
        query_l_p.append(query_a)
        funcion_l_p.append(ff)
        lag_l_p.append(lags_a)
        var_comun_pa_dic={
        'Nombre': nombre_l_p,
        'Query': query_l_p,
        'Funcion':funcion_l_p,
        'Lag': lag_l_p
        }
    var_comun_pa_df=pd.DataFrame(var_comun_pa_dic)
    var_comun_pa_df['Tipo']='ratio'
    var_comun_pa_df['a_p']='p_a'

    var_comun1_df=pd.concat([var_comun_a_df,var_comun_p_df,var_comun_pa_df])

    ## Var Ratios
    nombre_lr=list()
    query_lr=list()
    tipo_lr=list()

    for a_p_x in ['a','p_a']:
      variable_x=var_comun1_df[(var_comun1_df.a_p==a_p_x)]['Nombre'].str.replace('_*([^_*]*)$','',regex=True).drop_duplicates().to_list()
      for var_x in variable_x:
        for lag_s_x in range(len(lags_s)):
          #print(lag_x,lag_s_x)
          nom_lag_x=lags_s[lag_s_x]
          nom_lag_x_n=nom_lag_x.replace('_','')
          numerador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_x]) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
          name_num=numerador.replace(nom_lag_x,'')
          for lag_s_y in range(len(lags_s))[lag_s_x+1:]:
            #print(nom_lag_x,nom_lag_y)
            nom_lag_y=lags_s[lag_s_y]
            nom_lag_y_n=nom_lag_y.replace('_','')
            #print(nom_lag_x,nom_lag_y)
            denominador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_y] ) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
            query_r=numerador+'/'+denominador
            nombre_r=f'{name_num}_T{nom_lag_x_n}{nom_lag_y_n}'
            nombre_lr.append(nombre_r)
            query_lr.append(query_r)
            if a_p_x=='p_a':
              tipo_lr.append('ratio2')
            else:
              tipo_lr.append('ratio')
    var_ratio={
        'Nombre': nombre_lr,
        'Query': query_lr,
        'Tipo': tipo_lr}
    var_ratio_df=pd.DataFrame(var_ratio)
    var_ratio_df['Funcion']='div' 
      ## Append para cada tipo de a_funcion
    var_total_df=pd.concat([var_comun1_df,var_ratio_df])
    var_total_list_2.append(var_total_df) # Tengo una lista para cada funcion y a
    ## Append para cada categoria
    var_total_df_2=pd.concat(var_total_list_2)
  var_total_list_3.append(var_total_df_2)
var_total_df_4=pd.concat(var_total_list_3)
var_total_df_4['a_p']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['a_p'])
var_total_df_4['Lag']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['Lag'])

var_total_df_4.shape

len(var_total_list_3)

52*3

var_total_df_2.shape

len(var_total_list_3)

156*2

var_total_df_4.shape

len(var_total_list_3)

var_total_df_4.drop_duplicates().shape

"""## Numerica"""

var_comun_b_df_list=list()
funcion_p=['min','max','avg']
df_l=list()
var_total_list_3=list()

var_total_list_2=list()
for funcion_x in funciones:
  #print(categoria_x,funcion_x)
  nombre_l=list()
  query_l=list()
  lag_l=list()
  funcion_l=list()
  for lag_x in list(range(max(lags)+1))[1:]:
    #print(lag_x)
    query=f"{funcion_x}({var})"
    nombre=f"{funcion_x}_{var}_{lag_x}M"
    lag=lag_x
    #print(query,lag_x,nombre)
    nombre_l.append(nombre)
    query_l.append(query)
    lag_l.append(lag)
    funcion_l.append(funcion_x)

  var_comun_p_df=pd.DataFrame({
        'Nombre': nombre_l,
        'Query': query_l,
        'Lag': lag_l,
        'Funcion':funcion_l
      })
  var_comun_p_df['Tipo']='comun'
  var_comun_p_df['a_p']='p'

  var_comun_a_df=var_comun_p_df.copy()
  var_comun_a_df=var_comun_a_df[var_comun_a_df.Lag.isin(lags)]
  var_comun_a_df['a_p']='a'
  var_comun_p_df['Nombre']='p_'+var_comun_p_df['Nombre']

  ## Acumulados para las variables puntuales
  nombre_l_p=list()
  query_l_p=list()
  funcion_l_p=list()
  lag_l_p=list()
  for ff in funcion_p:
    for lags_a in lags:
      var_a_list_1=var_comun_p_df[(var_comun_p_df.Lag<=lags_a) & (var_comun_p_df.Nombre.str.contains(funcion_x))]['Nombre'].to_list()
      var_a_concat=",".join(var_a_list_1)
      query_a=f'{ff}({var_a_concat})'
      nombre_aa=re.sub('_*([^_*]*)$','',var_a_list_1[0])
      nombre_a=f'{ff}_a{nombre_aa}_{lags_a}M'
      nombre_l_p.append(nombre_a)
      query_l_p.append(query_a)
      funcion_l_p.append(ff)
      lag_l_p.append(lags_a)
      var_comun_pa_dic={
        'Nombre': nombre_l_p,
        'Query': query_l_p,
        'Funcion':funcion_l_p,
        'Lag': lag_l_p
      }
  var_comun_pa_df=pd.DataFrame(var_comun_pa_dic)
  var_comun_pa_df['Tipo']='ratio'
  var_comun_pa_df['a_p']='p_a'

  var_comun1_df=pd.concat([var_comun_a_df,var_comun_p_df,var_comun_pa_df])

  ## Var Ratios
  nombre_lr=list()
  query_lr=list()
  tipo_lr=list()

  for a_p_x in ['a','p_a']:
    variable_x=var_comun1_df[(var_comun1_df.a_p==a_p_x)]['Nombre'].str.replace('_*([^_*]*)$','',regex=True).drop_duplicates().to_list()
    for var_x in variable_x:
      for lag_s_x in range(len(lags_s)):
        #print(lag_x,lag_s_x)
        nom_lag_x=lags_s[lag_s_x]
        nom_lag_x_n=nom_lag_x.replace('_','')
        numerador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_x]) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
        name_num=numerador.replace(nom_lag_x,'')
        for lag_s_y in range(len(lags_s))[lag_s_x+1:]:
          #print(nom_lag_x,nom_lag_y)
          nom_lag_y=lags_s[lag_s_y]
          nom_lag_y_n=nom_lag_y.replace('_','')
          #print(nom_lag_x,nom_lag_y)
          denominador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_y] ) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
          query_r=numerador+'/'+denominador
          nombre_r=f'{name_num}_T{nom_lag_x_n}{nom_lag_y_n}'
          nombre_lr.append(nombre_r)
          query_lr.append(query_r)
          if a_p_x=='p_a':
            tipo_lr.append('ratio2')
          else:
            tipo_lr.append('ratio')
  var_ratio={
        'Nombre': nombre_lr,
        'Query': query_lr,
        'Tipo': tipo_lr}
  var_ratio_df=pd.DataFrame(var_ratio)
  var_ratio_df['Funcion']='div' 
      
  var_total_df=pd.concat([var_comun1_df,var_ratio_df])
  ## Append para cada tipo de a_funcion
  var_total_list_2.append(var_total_df) # Tengo una lista para cada funcion y a
  ## Append para cada categoria
  var_total_df_2=pd.concat(var_total_list_2)
var_total_list_3.append(var_total_df_2)
var_total_df_4=pd.concat(var_total_list_3)
var_total_df_4['a_p']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['a_p'])
var_total_df_4['Lag']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['Lag'])

var_total_df_4.shape

"""## Variable conteo"""

var_comun_b_df_list=list()
funcion_p=['min','max','avg']
df_l=list()
var_total_list_3=list()

var_total_list_2=list()

#print(categoria_x,funcion_x)
nombre_l=list()
query_l=list()
lag_l=list()
funcion_l=list()
for lag_x in list(range(max(lags)+1))[1:]:
  #print(lag_x)
  query=f"COUNT( DISTINCT {var})"
  nombre=f"N_{var}_{lag_x}M"
  lag=lag_x
  #print(query,lag_x,nombre)
  nombre_l.append(nombre)
  query_l.append(query)
  lag_l.append(lag)
  funcion_l.append(funcion_x)

var_comun_p_df=pd.DataFrame({
        'Nombre': nombre_l,
        'Query': query_l,
        'Lag': lag_l,
        'Funcion':funcion_l
      })
var_comun_p_df['Tipo']='comun'
var_comun_p_df['a_p']='p'

var_comun_a_df=var_comun_p_df.copy()
var_comun_a_df=var_comun_a_df[var_comun_a_df.Lag.isin(lags)]
var_comun_a_df['a_p']='a'

var_comun1_df=pd.concat([var_comun_a_df])

## Var Ratios
nombre_lr=list()
query_lr=list()
tipo_lr=list()

for a_p_x in ['a']:
  variable_x=var_comun1_df[(var_comun1_df.a_p==a_p_x)]['Nombre'].str.replace('_*([^_*]*)$','',regex=True).drop_duplicates().to_list()
  for var_x in variable_x:
    for lag_s_x in range(len(lags_s)):
      #print(lag_x,lag_s_x)
      nom_lag_x=lags_s[lag_s_x]
      nom_lag_x_n=nom_lag_x.replace('_','')
      numerador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_x]) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
      name_num=numerador.replace(nom_lag_x,'')
      for lag_s_y in range(len(lags_s))[lag_s_x+1:]:
        #print(nom_lag_x,nom_lag_y)
        nom_lag_y=lags_s[lag_s_y]
        nom_lag_y_n=nom_lag_y.replace('_','')
        #print(nom_lag_x,nom_lag_y)
        denominador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_y] ) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
        query_r=numerador+'/'+denominador
        nombre_r=f'{name_num}_T{nom_lag_x_n}{nom_lag_y_n}'
        nombre_lr.append(nombre_r)
        query_lr.append(query_r)
        if a_p_x=='p_a':
          tipo_lr.append('ratio2')
        else:
          tipo_lr.append('ratio')
var_ratio={
        'Nombre': nombre_lr,
        'Query': query_lr,
        'Tipo': tipo_lr}
var_ratio_df=pd.DataFrame(var_ratio)
var_ratio_df['Funcion']='div' 
      
var_total_df=pd.concat([var_comun1_df,var_ratio_df])
## Append para cada tipo de a_funcion
var_total_list_2.append(var_total_df) # Tengo una lista para cada funcion y a
## Append para cada categoria
var_total_df_2=pd.concat(var_total_list_2)
var_total_df_2['a_p']=np.where(var_total_df_2['Tipo']!='comun',np.nan,var_total_df_2['a_p'])
var_total_df_2['Lag']=np.where(var_total_df_2['Tipo']!='comun',np.nan,var_total_df_2['Lag'])

var_total_df_2.shape

var_total_df_2

var_total_df_2[var_total_df_2.Tipo=='comun']

"""## Conteo Categorico"""

var_comun_b_df_list=list()
funcion_p=['min','max','avg']
df_l=list()
var_total_list_3=list()
for categoria_x in categorias:
  var_total_list_2=list()
  for funcion_x in ['COUNT']:
    #print(categoria_x,funcion_x)
    nombre_l=list()
    query_l=list()
    lag_l=list()
    for lag_x in list(range(max(lags)+1))[1:]:
      #print(lag_x)
      query=f"{funcion_x}(DISTINCT (case when {var2}='{categoria_x}' then {var} else 0 end))"
      nombre=f"N_{var}_{categoria_x}_{lag_x}M"
      lag=lag_x
      #print(query,lag_x,nombre)
      nombre_l.append(nombre)
      query_l.append(query)
      lag_l.append(lag)

    var_comun_p_df=pd.DataFrame({
        'Nombre': nombre_l,
        'Query': query_l,
        'Lag': lag_l
      })
    var_comun_p_df['Tipo']='comun'
    var_comun_p_df['Funcion']='sql'
    var_comun_p_df['a_p']='p'

    var_comun_a_df=var_comun_p_df.copy()
    var_comun_a_df=var_comun_a_df[var_comun_a_df.Lag.isin(lags)]
    var_comun_a_df['a_p']='a'
    var_comun1_df=var_comun_a_df
    ## Var Ratios
    nombre_lr=list()
    query_lr=list()
    tipo_lr=list()

    for a_p_x in ['a']:
      variable_x=var_comun1_df[(var_comun1_df.a_p==a_p_x)]['Nombre'].str.replace('_*([^_*]*)$','',regex=True).drop_duplicates().to_list()
      for var_x in variable_x:
        for lag_s_x in range(len(lags_s)):
          #print(lag_x,lag_s_x)
          nom_lag_x=lags_s[lag_s_x]
          nom_lag_x_n=nom_lag_x.replace('_','')
          numerador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_x]) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
          name_num=numerador.replace(nom_lag_x,'')
          for lag_s_y in range(len(lags_s))[lag_s_x+1:]:
            #print(nom_lag_x,nom_lag_y)
            nom_lag_y=lags_s[lag_s_y]
            nom_lag_y_n=nom_lag_y.replace('_','')
            #print(nom_lag_x,nom_lag_y)
            denominador=var_comun1_df[(var_comun1_df.Lag==lags[lag_s_y] ) & (var_comun1_df.a_p==a_p_x) & (var_comun1_df.Nombre.str.contains(var_x))]['Nombre'].values[0]
            query_r=numerador+'/'+denominador
            nombre_r=f'{name_num}_T{nom_lag_x_n}{nom_lag_y_n}'
            nombre_lr.append(nombre_r)
            query_lr.append(query_r)
            if a_p_x=='p_a':
              tipo_lr.append('ratio2')
            else:
              tipo_lr.append('ratio')
    var_ratio={
        'Nombre': nombre_lr,
        'Query': query_lr,
        'Tipo': tipo_lr}
    var_ratio_df=pd.DataFrame(var_ratio)
    var_ratio_df['Funcion']='div' 
      ## Append para cada tipo de a_funcion
    var_total_df=pd.concat([var_comun1_df,var_ratio_df])
    var_total_list_2.append(var_total_df) # Tengo una lista para cada funcion y a
    ## Append para cada categoria
    var_total_df_2=pd.concat(var_total_list_2)
  var_total_list_3.append(var_total_df_2)
var_total_df_4=pd.concat(var_total_list_3)
var_total_df_4['a_p']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['a_p'])
var_total_df_4['Lag']=np.where(var_total_df_4['Tipo']!='comun',np.nan,var_total_df_4['Lag'])

var_total_df_4.shape

var_comun1_df.drop_duplicates().shape