# Get Set Hedge
![](https://img.shields.io/badge/python-3.7-red)
![](https://img.shields.io/badge/Streamlit-0.67.1-blue)
![](https://img.shields.io/badge/numpy-1.19.2-blue)
![](https://img.shields.io/badge/pandas-1.1.2-blue)
![](https://img.shields.io/badge/statsmodels-0.12.0-blue)
![](https://img.shields.io/badge/license-MIT-green)

## About

Given the rise of assets under passive management and particularly because of rise of ETFs, stock prices might be driven based on the ETF performance of ETF’s that the stock is part of, in addition to the underlying business fundamentals.

**Get Set Hedge is a framework which a discretionary investor might want to use in case he likes a certain stock but does not like certain factors it is exposed to.**

The way we do this is by pre-creating multiple academic factors and allowing the investor to request for building a custom factor(at some price of course).

Get Set Hedge perform historical factor validation analysis and produce robust hedges the investor needs to do. In order to execute those hedges in market an investor can use relevant ETFs.

## Installation

```bash
git clone https://github.com/adityavyasbme/GetSetHedge #Clone this repo
cd GetSetHedge #Go into the folder
pip install -r requirements.txt #Install the required files
pip install yfinance #Confirm install of yfinance library
```

## Usage

```bash
streamlit run stream.py #Run the app
```

## Pipeline

![](https://github.com/adityavyasbme/GetSetHedge/blob/master/data/images/Pipeline.jpeg?raw=true)

## Key Features
- Streamlit Web application at your hand
- You can add your own Index to track at backend
- Get Risk Exposure of a certain stock to the corresponding factors ETF, currently constructing, Beta Against Beta strategy and Momentum factors
- Exploratory Data Analysis, currently uses Altair graphs
- Create your own custom indicators, e.g. SMA
- Custom Visualization
- Support for Factor Construction
- Containerization support

## Documentation
Check out more details on: [GSH's Documentation](https://adityavyasbme.github.io/GetSetHedge/)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

Please make sure to update tests as appropriate

## Credits


- Big round of thanks to [Insight](https://insightfellows.com) community for helping me create this framework
- I would also like to thank [Streamlit](https://www.streamlit.io) community for helping me create this Web Application
- The codebase of this web application is inspired from [Mark Skov Madsen](https://www.linkedin.com/in/marcskovmadsen)'s [Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit)

## License
[MIT](https://github.com/adityavyasbme/GetSetHedge/blob/master/LICENSE)
