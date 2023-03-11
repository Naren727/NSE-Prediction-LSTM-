# NSE-Prediction-LSTM
A repo for NSE screener and prediction project using apis for real time data

## What is the application meant for? :
I built this application to help rookie traders and people new to the stock market make effective trades that will help get them more
interested in the subject.For people who have no clue as to how the next trading session is going to be like, this project will provide and idea which can be imporved upon.

## What the user needs to do? :
The user simply selects his/her stock that is listed on the National Stock Exchange(nse) that is a part of the Nifty 50 Stocks

## What Otput does the user get :
The user gets a LSTM based prediction on what the next close price will be :
  - if the market is currently open then the model predicts what the current trading session will end on
  - if the market is closed then the model predicts the price for the next trading session.

## What is LSTM :
Long Short Term Memory (LSTM) is a special kind of RNN that is capable of learning long-term dependencies or trends
If you want a more vivid and complete understanding of the model then refer this article : https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21

## Caution :
During Actual Trading session various reasons may lead to discrepancies.For example a company may crash overnight which will not be predicted by the application.
So when using to trade in the markets I advise caution and ask you to use it at your own risk

## Test Case Outputs :
Feature Selection : 
![Screenshot (452)](https://user-images.githubusercontent.com/81982063/224481368-6b2e8c8b-9752-4e54-8e8c-a34af8dc2801.png)

Model Performance for INFY(as of 10/3/23):
![Screenshot (454)](https://user-images.githubusercontent.com/81982063/224481492-bdb139d5-207d-4cf4-b283-6a27f56f6744.png)

![Screenshot (455)](https://user-images.githubusercontent.com/81982063/224481479-b2192f30-0811-427f-b2c7-18dc92f8e9cf.png)

