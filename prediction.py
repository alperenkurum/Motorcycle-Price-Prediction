import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm
import matplotlib.pyplot as plt
import time
import seaborn as sns

# Load the data skip one line
df = pd.read_csv('motors.csv', skiprows=1)


# Split the data into features (X) and target (y)
X = df.iloc[:, 1:]
y = df.iloc[:, 0]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
start_time = time.time()
model = LinearRegression()
model.fit(X_train, y_train)
end_time = time.time()

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Training time: {end_time - start_time} seconds")
print(f"R-squared score: {r2}")
print(f"Mean Squared Error: {mse}")

# Time series analysis
X = sm.add_constant(X)  # adding a constant
model = sm.OLS(y, X).fit()
print_model = model.summary()
print(print_model)
print(y_pred)
df_plot = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

# Create a scatter plot for actual and predicted prices with a regression line
sns.lmplot(x='Actual', y='Predicted', data=df_plot)

# Display the plot
plt.show()

plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Prices')

# Create a scatter plot for predicted prices
plt.scatter(range(len(y_pred)), y_pred, color='red', label='Predicted Prices')

plt.xlabel('Index')
plt.ylabel('Prices')
plt.title('Actual Prices vs Predicted Prices')
plt.legend()

# Display the plot
plt.show()