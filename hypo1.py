import numpy as np
import pandas as pd
from horse import Horse
from race import Race
import pdb
from sklearn.preprocessing import Imputer, StandardScaler


#------------------------------------------------------------------------------
def main():
  dataset = pd.read_csv('results/ml_2017-04-17.csv')
  
  #data clean up

  # H Odds columns: impute and scale
  horse_odds_labels = ['h0_odds','h1_odds', 'h2_odds', 'h3_odds', 'h4_odds', 'h5_odds', 'h6_odds', 'h7_odds', 'h8_odds', 'h9_odds', 'h10_odds', 'h11_odds', 'h12_odds', 'h13_odds', 'h14_odds', 'h15_odds', 'h16_odds', 'h17_odds','h18_odds']
  dataset = impute_def_col(dataset, horse_odds_labels)
  dataset = scale_def_col(dataset, horse_odds_labels)

  # H Weights columns: impute and scale
  horse_weight_labels = ['h0_weight','h1_weight', 'h2_weight', 'h3_weight', 'h4_weight', 'h5_weight', 'h6_weight', 'h7_weight', 'h8_weight', 'h9_weight', 'h10_weight', 'h11_weight', 'h12_weight', 'h13_weight', 'h14_weight', 'h15_weight', 'h16_weight', 'h17_weight','h18_weight']
  dataset = impute_def_col(dataset, horse_weight_labels)
  dataset = scale_def_col(dataset, horse_weight_labels)

  # H Claim value columns: impute and scale
  horse_claim_value_labels = ['h0_claim_value','h1_claim_value', 'h2_claim_value', 'h3_claim_value', 'h4_claim_value', 'h5_claim_value', 'h6_claim_value', 'h7_claim_value', 'h8_claim_value', 'h9_claim_value', 'h10_claim_value', 'h11_claim_value', 'h12_claim_value', 'h13_claim_value', 'h14_claim_value', 'h15_claim_value', 'h16_claim_value', 'h17_claim_value','h18_claim_value']
  dataset = impute_def_col(dataset, horse_claim_value_labels)
  dataset = scale_def_col(dataset, horse_claim_value_labels)

  # R Purse value columns: impute and scale
  dataset = impute_def_col(dataset, ['purse'])
  dataset = scale_def_col(dataset, ['purse'])

  # R Purse value columns: impute and scale
  dataset = impute_def_col(dataset, ['distance'])
  dataset = scale_def_col(dataset, ['distance'])

  pdb.set_trace()
  # R Class Rating value columns: impute and scale
  dataset = impute_def_col(dataset, ['class_rating'])
  dataset = scale_def_col(dataset, ['class_rating'])
  
  pdb.set_trace()

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
def scale_def_col(df, label):
  for la in label:
    sc = StandardScaler()
    col = np.array(df[la]).T
    try:
      df[la] = sc.fit_transform(col.reshape(-1,1))
    except:
      pdb.set_trace()
  return df

#------------------------------------------------------------------------------
if __name__ == '__main__':
  main()