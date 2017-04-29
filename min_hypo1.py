import numpy as np
import pandas as pd
from horse import Horse
from race import Race
import pdb
from sklearn.preprocessing import Imputer, StandardScaler, OneHotEncoder
from sklearn.cross_validation import train_test_split


#------------------------------------------------------------------------------
def main():
  df = pd.read_csv('results/singleHorse_2017-04-21.csv')
  

  # #data clean up
  # # H Odds columns: impute and scale
  # horse_odds_labels = ['h0_odds','h1_odds', 'h2_odds', 'h3_odds', 'h4_odds', 'h5_odds', 'h6_odds', 'h7_odds', 'h8_odds', 'h9_odds', 'h10_odds', 'h11_odds', 'h12_odds', 'h13_odds', 'h14_odds', 'h15_odds', 'h16_odds', 'h17_odds','h18_odds']
  # dataset = impute_def_col(dataset, horse_odds_labels)
  # dataset = scale_def_col(dataset, horse_odds_labels)

  # # H Weights columns: impute and scale
  # horse_weight_labels = ['h0_weight','h1_weight', 'h2_weight', 'h3_weight', 'h4_weight', 'h5_weight', 'h6_weight', 'h7_weight', 'h8_weight', 'h9_weight', 'h10_weight', 'h11_weight', 'h12_weight', 'h13_weight', 'h14_weight', 'h15_weight', 'h16_weight', 'h17_weight','h18_weight']
  # dataset = impute_def_col(dataset, horse_weight_labels)
  # dataset = scale_def_col(dataset, horse_weight_labels)

  # # H Claim value columns: impute and scale
  # horse_claim_value_labels = ['h0_claim_value','h1_claim_value', 'h2_claim_value', 'h3_claim_value', 'h4_claim_value', 'h5_claim_value', 'h6_claim_value', 'h7_claim_value', 'h8_claim_value', 'h9_claim_value', 'h10_claim_value', 'h11_claim_value', 'h12_claim_value', 'h13_claim_value', 'h14_claim_value', 'h15_claim_value', 'h16_claim_value', 'h17_claim_value','h18_claim_value']
  # dataset = impute_def_col(dataset, horse_claim_value_labels)
  # dataset = scale_def_col(dataset, horse_claim_value_labels)

  # # R Purse value columns: impute and scale
  # dataset = impute_def_col(dataset, ['purse'])
  # dataset = scale_def_col(dataset, ['purse'])

  # # R Purse value columns: impute and scale
  # dataset = impute_def_col(dataset, ['distance'])
  # dataset = scale_def_col(dataset, ['distance'])

  # # R Class Rating value columns: impute and scale
  # dataset = impute_def_col(dataset, ['class_rating'])
  # dataset = scale_def_col(dataset, ['class_rating'])

  # Data splitting
  x = df.iloc[:,:-1]
  y = df.iloc[:,-1]

  sc_hash = {}
  columns = list(x.columns)
  for col in columns:
    x,sc_hash = scale_col(x, col, sc_hash)

  pdb.set_trace()

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
  
  # SVC
  from sklearn.svm import SVC
  svc = SVC()
  svc.fit(x_train, y_train)
  y_pred_svm = svc.predict(x_test)

  # Validation
  from sklearn.metrics import confusion_matrix
  confusion_matrix(y_test, y_pred_svm)
  # predicted  0      1    Total:
  # real 0 [7590, 1240]     8830
  #      1 [2715, 2187]     4902 
  # Predict NOT wps accuracy: 85.95%
  # Predict wps accuracy:     44.61%

  # Removing race_number from data
  x_nrn = x.iloc[:,1:]
  x_nrn_train, x_nrn_test, y_nrn_train, y_nrn_test = train_test_split(x_nrn, y, test_size=0.2)
  svc_nrn.fit(x_nrn_train,y_nrn_train)
  y_pred_nrn = svc_nrn.predict(x_nrn_test)
  # predicted  0      1    Total:
  # real 0 [7609, 1221]     8830
  #      1 [2812, 2090]     4902
  # Predict NOT wps accuracy: 86.17%
  # Presict wps accuracy:     42.63%


#------------------------------------------------------------------------------
def impute_def_col(df, label):
  for la in label:
    imp = Imputer()
    col = np.array(df[la]).T
    try:
      df[la] = imp.fit_transform(col.reshape(-1,1))
    except:
      pdb.set_trace()
  return df

#------------------------------------------------------------------------------
def scale_col(df, label, sc_dict):
  sc = StandardScaler()
  col = np.array(df[label]).T
  try:
    sc.fit(col.reshape(-1,1))
    df[label] = sc.transform(col.reshape(-1,1))
    sc_dict[label] = sc
  except:
    pdb.set_trace()
  return df,sc_dict

#------------------------------------------------------------------------------
def ohe_col(df, label):
  for la in label:
    le  = LabelEncoder()
    ohe = OneHotEncoder()
    col = np.array(df[la]).T
    try:
      col_le = le.fit_transform(col.reshape(-1,1))
    except:
      pass
  return

#------------------------------------------------------------------------------
if __name__ == '__main__':
  main()