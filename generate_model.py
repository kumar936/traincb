import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Simulated data
data = pd.DataFrame({
    'Source': ['A', 'B', 'A', 'C', 'B'],
    'Destination': ['C', 'C', 'B', 'A', 'A'],
    'Time_Slot': ['07:00-09:00', '07:00-09:00', '09:00-11:00', '11:00-13:00', '13:00-15:00'],
    'Crowd_Level': ['High', 'Medium', 'Low', 'Medium', 'High']
})

X = data[['Source', 'Destination', 'Time_Slot']]
y = data['Crowd_Level']

X_encoded = pd.get_dummies(X)
model = RandomForestClassifier()
model.fit(X_encoded, y)

joblib.dump(model, 'model.pkl')
data.to_csv('train_data.csv', index=False)
print("Model trained and saved as model.pkl")
