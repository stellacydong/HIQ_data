#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## for data
import pandas as pd
import numpy as np
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for statistical tests
# import scipy
# import statsmodels.formula.api as smf
import statsmodels.api as sm


# In[ ]:


# import the data from json file named under "b_data.json"

import json
with open("b_data.json", "r") as read_file:
    data = json.load(read_file)


# In[ ]:


# re-arrange the raw data into the table which is easier to be used later 

df = pd.DataFrame()
for i in range(0,20):
    for j in range(0,10): 
        temp = pd.DataFrame.from_dict(pd.DataFrame.from_dict(data, orient='index')[i][j], orient='index').T
        df = pd.concat([df, temp], axis=0).reset_index(drop=True)


# In[ ]:


# make the numerical data type into float so that they can be used in statsmodels
df = df.astype({'surgeries_last_month': 'float', 
                'surgeries_this_month': 'float',
                'age_in_yrs': 'float',
                'service_id': 'float', 
                'hospital_id': 'float'})


# In[ ]:


# fit a simple linear model (OLS - for "ordinary least squares" method) with 
# surgeries_this_month as the response and  
# surgeries_last_month + service_id + age_in_yrs + c(last_name) + hospital_id as the predictor:
lm = sm.OLS.from_formula('surgeries_this_month ~ surgeries_last_month + service_id + age_in_yrs + C(last_name) + hospital_id', df)
result = lm.fit()
print(result.summary())


# In[ ]:


# fit a simple linear model (OLS - for "ordinary least squares" method) with 
# surgeries_this_month as the response and  
# surgeries_last_month + hospital_id as the predictor:
lm = sm.OLS.from_formula('surgeries_this_month ~ surgeries_last_month', df)
result = lm.fit()
print(result.summary())


# In[ ]:


sns.regplot('surgeries_last_month','surgeries_this_month',df, line_kws = {"color":"r"}, ci=None)


# In[ ]:


# plot the residuals against the fitted values 
fitted_values = pd.Series(result.fittedvalues, name="Fitted Values")
residuals = pd.Series(result.resid, name="Residuals")
sns.regplot(fitted_values, residuals, fit_reg=False)


# In[ ]:


# normalized residuals
s_residuals = pd.Series(result.resid_pearson, name="S. Residuals")
sns.regplot(fitted_values, s_residuals,  fit_reg=False)


# In[ ]:


# look for points with high leverage:
from statsmodels.stats.outliers_influence import OLSInfluence
leverage = pd.Series(OLSInfluence(result).influence, name = "Leverage")
sns.regplot(leverage, s_residuals,  fit_reg=False)


# In[ ]:


corrMatrix = df.corr()
g=sns.heatmap(df[['surgeries_last_month','service_id','age_in_yrs','surgeries_this_month']].corr(),annot=True,cmap="Blues")
plt.show()


# In[ ]:




