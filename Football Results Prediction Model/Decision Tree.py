# Code you have previously used to load data
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# Path of the file to read
file_path = 'Stats.csv'

#dataframe consisting of statistical data from 'Stats.csv'
data = pd.read_csv(file_path)

# convert result data to int
data.loc[data['Result'] == "W", 'Result'] = 1
data.loc[data['Result'] == "D", 'Result'] = 0
data.loc[data['Result'] == "L", 'Result'] = -1

# y represents what the model is predicting, i.e: Result, xG, GF, GA, etc.
y = data.Gls
# Create the feature space (which columns from the original data are used to create the model)
features = ["xG"]
X = data[features]

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Specify Model
model = DecisionTreeRegressor(random_state=1)
# Fit Model
model.fit(train_X, train_y)

# Make validation predictions and calculate mean absolute error
val_predictions = model.predict(val_X)
val_mae = mean_absolute_error(val_predictions, val_y)
print("Validation MAE when not specifying max_leaf_nodes: {:,.0f}".format(val_mae))

# Using best value for max_leaf_nodes after determining what best value is (trial and error)
model.fit(train_X, train_y)
val_predictions = model.predict(val_X)

#actual values
print(val_y)
#predicted values
print(val_predictions)
#mean average error betweena prediction and its associated actual value
val_mae = mean_absolute_error(val_predictions, val_y)
print("Validation MAE for best value of max_leaf_nodes: {:,.0f}".format(val_mae))
