
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from sklearn.linear_model import Ridge
from sklearn.metrics import make_scorer


# In[2]:


# Enter the path for Viz_Data.csv, rid
viz_file_path = "./Prep_Data/Viz_Data.csv"
rid = 132539

# Read the data into dataframe
viz_df = pd.read_csv(viz_file_path)
rid_df = viz_df.groupby('rid').get_group(rid)

# Count the available number of temporal data for the given rid
# Note: We need atleast two values for a temporial attribute to visualize in lineplot
temp_attr_list = [ "Albumin", "ALP", "ALT", "AST", "Bilirubin", "BUN", "Cholesterol",
                "Creatinine", "DiasABP", "FiO2", "GCS", "Glucose", "HCO3", "HCT",
                "HR", "K", "Lactate", "Mg", "MAP", "MechVent", "Na", "NIDiasABP",
                "NIMAP", "NISysABP", "PaCO2", "PaO2", "pH", "Platelets", 
                "RespRate", "SaO2", "SysABP", "Temp", "TroponinI", "TroponinT",
                "Urine", "WBC"]
no_of_plots = 0
for attr, attr_df in rid_df.groupby('Attr_Name'):
  if (attr_df.shape[0] <= 1) or (attr not in temp_attr_list):
    continue
  no_of_plots += 1

# Plot line graph
fig, axs = plt.subplots(1, no_of_plots)
fig.set_size_inches(150, 5)
current_ax = 0
for attr, attr_df in rid_df.groupby('Attr_Name'):
  if (attr_df.shape[0] <= 1) or (attr not in temp_attr_list):
    continue
  axs[current_ax].plot(attr_df['time'], attr_df['Attr_Value'])
  axs[current_ax].set(xlabel='time', ylabel=attr)
  for tick in axs[current_ax].get_xticklabels():
        tick.set_rotation(90)
  current_ax += 1

print("Vizualization for", rid)


# In[3]:


# Enter the path for file summary_mean
mean_file_path = "./Prep_Data/summary_mean.csv"

mean_df = pd.read_csv(mean_file_path)

# Clean the Data
mean_df['Length_of_stay'].replace(-1, 2, inplace=True)
mean_df['Height'] = mean_df['Height'].apply(lambda x: np.NaN if x == -1.0 else x)
mean_df['Weight'] = mean_df['Weight'].apply(lambda x: np.NaN if x == -1.0 else x)
mean_df['Gender'] = mean_df['Gender'].apply(lambda x:np.NaN if x == -1 else x)

# Drop Record ID
mean_df = mean_df.drop(columns=["RecordID"])

print(mean_df.head(10))


# In[4]:


# Columns to be dropped
drop_cols = []

# Drop sparse features - Drop features if more than half of the patients doesn't have data
for items in mean_df.isna().sum().iteritems(): 
    if items[1] > 2000:
      drop_cols.append(items[0])

# Drop constant features and impute remaining features - Based on Exploratory Analysis
drop_cols.append('MechVent')

# Create new matrix and impute remaining features
r_mean_df = mean_df.drop(columns=drop_cols)

# Remove highly correlated features
X = r_mean_df.drop(columns=["Length_of_stay","In-hospital_death"])
plt.figure(figsize=(32,10))
sns.heatmap(data=X.corr(), cmap='seismic',annot=True, vmin=-1, vmax=1)
drop_cols.append("NIMAP") # NIMAP is highly correalted to NIDiasABP, NISysABP
r_mean_df.drop(columns=['NIMAP'])

print("Removed Columns:", drop_cols)
r_mean_df.head(3)


# In[5]:


# Enter the path for file summary_mode
mode_file_path = "./Prep_Data/summary_mode.csv"

mode_df = pd.read_csv(mode_file_path)

# Clean the Data
mode_df['Length_of_stay'].replace(-1, 2, inplace=True)
mode_df['Height'] = mode_df['Height'].apply(lambda x: np.NaN if x == -1.0 else x)
mode_df['Weight'] = mode_df['Weight'].apply(lambda x: np.NaN if x == -1.0 else x)
mode_df['Gender'] = mode_df['Gender'].apply(lambda x:np.NaN if x == -1 else x)

# Drop Record ID
mode_df = mode_df.drop(columns=["RecordID"])

mode_df.head(3)


# In[6]:


# Enter the path for file summary_stddev
s_mean_file_path = "./Prep_Data/combined_mean_std.csv"

s_mean_df = pd.read_csv(s_mean_file_path)

# Clean the Data
s_mean_df['Length_of_stay'].replace(-1, 2, inplace=True)
s_mean_df['Height'] = s_mean_df['Height'].apply(lambda x: np.NaN if x == -1.0 else x)
s_mean_df['Weight'] = s_mean_df['Weight'].apply(lambda x: np.NaN if x == -1.0 else x)
s_mean_df['Gender'] = s_mean_df['Gender'].apply(lambda x:np.NaN if x == -1 else x)

# Drop Record ID
s_mean_df = s_mean_df.drop(columns=["RecordID"])

s_mean_df.head(3)


# # 3. Model Building

# In[7]:


def classifier_one(df, matrix_name):

  X = df.drop(columns=["Length_of_stay","In-hospital_death"])
  y = df["In-hospital_death"]

  num_cols = [e for e in list(X.columns) if e not in ('Gender', 'ICUType')]

  # Preprocessor - Imputation and Scaling
  numeric_transformer = Pipeline(steps=[
      ('num_imputer', SimpleImputer(missing_values=np.NaN,strategy='mean')),
      ('scaler', StandardScaler())])
  non_numeric_transformer = Pipeline(steps=[
      ('non_num_imputer', SimpleImputer(missing_values=np.NaN,strategy='most_frequent'))])
  preprocessor = ColumnTransformer(
      transformers=[
          ('numeric', numeric_transformer, num_cols),
          ('non_numeric', non_numeric_transformer, ['Gender', 'ICUType'])])

  Model1 = Pipeline(steps=[('preprocessing', preprocessor),
                          ('pca',TruncatedSVD()),
                          ('xgb',XGBClassifier(gamma=1, learning_rate=0.1, max_depth=3, subsample=0.9))])

  scores = cross_val_score(Model1, X, y, cv = KFold(n_splits=4, shuffle=False), scoring="roc_auc")
  print(matrix_name+":", sum(scores)/len(scores))

classifier_one(mean_df, "Temporal_Mean_Matrix")
classifier_one(r_mean_df, "Reduced_Temporal_Mean_Matrix")
classifier_one(mode_df, "Temporal_Mode_Matrix")
classifier_one(s_mean_df, "Temporal_Mean_Std_Matrix")


# In[8]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def rmse(y, y_pred):
        return np.sqrt(np.mean((y_pred - y)**2))
rmse_scorer = make_scorer(rmse, greater_is_better=False)

def regressor_one(df, matrix_name):

  X = df.drop(columns=["Length_of_stay","In-hospital_death"])
  y = df["Length_of_stay"]

  num_cols = [e for e in list(X.columns) if e not in ('Gender', 'ICUType')]

  # Preprocessor - Imputation and Scaling
  numeric_transformer = Pipeline(steps=[
      ('num_imputer', SimpleImputer(missing_values=np.NaN,strategy='mean')),
      ('scaler', StandardScaler())])
  non_numeric_transformer = Pipeline(steps=[
      ('non_num_imputer', SimpleImputer(missing_values=np.NaN,strategy='most_frequent'))])
  preprocessor = ColumnTransformer(
      transformers=[
          ('numeric', numeric_transformer, num_cols),
          ('non_numeric', non_numeric_transformer, ['Gender', 'ICUType'])])

  Model1 = Pipeline(steps=[('preprocessing', preprocessor),
                           ('pca',TruncatedSVD()),
                           ('xgb', xgb.XGBRegressor(objective = 'reg:squarederror', n_estimators = 40, max_depth = 5))])

  scores = cross_val_score(Model1, X, y, cv = KFold(n_splits=4, shuffle=False), scoring=rmse_scorer)
  print(matrix_name+":", -1 * sum(scores)/len(scores))

import xgboost as xgb

regressor_one(mean_df, "Temporal_Mean_Matrix")
regressor_one(r_mean_df, "Reduced_Temporal_Mean_Matrix")
regressor_one(mode_df, "Temporal_Mode_Matrix")
regressor_one(s_mean_df, "Temporal_Mean_Std_Matrix")


# In[9]:


# Improved Mortality Classifier
def classifier_two(df, model_name):

  X = df.drop(columns=["Length_of_stay","In-hospital_death"])
  y = df["In-hospital_death"]

  num_cols = [e for e in list(X.columns) if e not in ('Gender', 'ICUType')]

  # Preprocessor - Imputation and Scaling
  numeric_transformer = Pipeline(steps=[
      ('num_imputer', SimpleImputer(missing_values=np.NaN,strategy='mean')),
      ('scaler', StandardScaler())])
  non_numeric_transformer = Pipeline(steps=[
      ('non_num_imputer', SimpleImputer(missing_values=np.NaN,strategy='most_frequent'))])
  preprocessor = ColumnTransformer(
      transformers=[
          ('numeric', numeric_transformer, num_cols),
          ('non_numeric', non_numeric_transformer, ['Gender', 'ICUType'])])

  Model1 = Pipeline(steps=[('preprocessing', preprocessor),
                          ('xgb',XGBClassifier(gamma=1, learning_rate=0.1, max_depth=3, subsample=0.9))])

  scores = cross_val_score(Model1, X, y, cv = KFold(n_splits=4, shuffle=False), scoring="roc_auc")
  print(model_name+":", sum(scores)/len(scores))

# Improved LoS Regressor
def regressor_two(df, model_name):

  X = df.drop(columns=["Length_of_stay","In-hospital_death"])
  y = df["Length_of_stay"]

  num_cols = [e for e in list(X.columns) if e not in ('Gender', 'ICUType')]

  # Preprocessor - Imputation and Scaling
  numeric_transformer = Pipeline(steps=[
      ('num_imputer', SimpleImputer(missing_values=np.NaN,strategy='mean')),
      ('scaler', StandardScaler())])
  non_numeric_transformer = Pipeline(steps=[
      ('non_num_imputer', SimpleImputer(missing_values=np.NaN,strategy='most_frequent'))])
  preprocessor = ColumnTransformer(
      transformers=[
          ('numeric', numeric_transformer, num_cols),
          ('non_numeric', non_numeric_transformer, ['Gender', 'ICUType'])])

  Model1 = Pipeline(steps=[('preprocessing', preprocessor),
                           ('xgb', xgb.XGBRegressor(objective = 'reg:squarederror', n_estimators = 40, max_depth = 5))])

  scores = cross_val_score(Model1, X, y, cv = KFold(n_splits=4, shuffle=False), scoring=rmse_scorer)
  print(model_name+":", -1 * sum(scores)/len(scores))

classifier_two(mean_df, "Classifier Model 2")
regressor_two(mode_df, "Regressor Model 2")


# # 4. Deployment Workflow

# ## 4.1. Workflow
# 
# ![alt text](https://i.ibb.co/tMMD130/Intelligent-system-prj-wrkflow.jpg)
# 
# **Step 1:** Get Mean Summary, Mode Summary - Refer to Section 2.1, 2.3.
# 
# **Step 2:** Clean Data - Replace '-1' missing values to 'np.NaN' for both Mean Summary, Mode Summary - Refer to Section 2.1, 2.3. Do Preprocessor following that for both summary - Refer to Section 3.3. Preprocessor includes Imputation, Scaling.
# 
# **Step 3:** Use mean summary as input for best classifier and use mode summary as input for best regressor - Refer Section 3.3.
# 
# Image Src. Local Path: ./Images/workflow.jpeg
# 

# In[11]:





# In[ ]:





# In[ ]:




