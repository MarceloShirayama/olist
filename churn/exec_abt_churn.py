import os
import pandas as pd
from olistlib.db import utils
from sklearn import tree, metrics

# diretórios do projeto
DATA_CHURN = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(DATA_CHURN)
DATA_DIR = os.path.join(BASE_DIR, 'upload_data', 'data')

query_path = './churn/query_abt_churn.sql'

query = utils.import_query(query_path)

datas = [
    '2017-02-01',
    '2017-03-01',
    '2017-04-01',
    '2017-05-01',
    '2017-06-01',
    '2017-07-01',
    '2017-08-01',
    '2017-09-01'
]

dfs = []

conn = utils.connect_db(db_dir=DATA_DIR)

for data in datas:
    query_formatada = query.format(date=data)
    df_tmp = pd.read_sql_query(query_formatada, conn)
    dfs.append(df_tmp)

abt = pd.concat(dfs, axis=0, ignore_index=True)

avg_churn = abt['flag_churn'].mean()

target = 'flag_churn'

features = abt.columns[3:-2]
features.remove(['seller_id', 'dt_ult_vda'])

clf = tree.DecisionTreeClassifier(max_depth=10)

clf.fit(abt[features], abt[target])

y_pred = clf.predict(abt[features])
y_prob = clf.predict_proba(abt[features])

acc = metrics.accuracy_score(abt[target], y_pred)
auc = metrics.roc_auc_score(abt[target], y_prob[:,1])

features_importance = pd.Series(clf.feature_importances_, index=features)
features_importance.sort_values(inplace=True)
