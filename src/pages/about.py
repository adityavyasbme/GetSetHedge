import streamlit as st


def question(que):
    st.markdown(f"<h3>{que}</h3>", unsafe_allow_html=True)


def answer(ans):
    st.markdown(f"<p> {ans} </p>", unsafe_allow_html=True),


def add_source(link, title):
    st.markdown(f"<a href='{link}'>{title}</a>", unsafe_allow_html=True)

# pylint: disable=line-too-long


def write():
    """Front End of the Documentation Page
    """
    
    with st.spinner("Loading Documentation ..."):
        st.write(
            "# DOCUMENTATION/FAQs")
        question("What is hedging?")
        answer("<i> Hedging is a risk management strategy employed to offset losses in investments by taking an opposite position in a related asset.</i>")
        answer("The best way to understand hedging is to think of it as a form of insurance. When people decide to hedge, they are insuring themselves against a negative event's impact on their finances. This doesn't prevent all negative events from happening. However, if a negative event does happen and you're properly hedged, the impact of the event is reduced.")
        answer("In practice, hedging occurs almost everywhere. For example, if you buy homeowner's insurance, you are hedging yourself against fires, break-ins, or other unforeseen disasters.")
        add_source(
            "https://www.investopedia.com/trading/hedging-beginners-guide/", "Show more")
        st.write("----")
        question("What is ETF?")
        answer("<i>An exchange traded fund (ETF) is a basket of securities that trade on an exchange, just like a stock.</i>")
        answer("ETF share prices fluctuate all day as the ETF is bought and sold; this is different from <b>mutual funds</b> that only trade once a day after the market closes.")
        answer("ETFs can contain all types of investments including stocks, commodities, or bonds; some offer U.S. only holdings, while others are international.")
        answer("ETFs offer low expense ratios and fewer broker commissions than buying the stocks individually.")
        add_source("https://www.investopedia.com/terms/e/etf.asp", "Show more")
        st.write("----")

        question("What is Factor Construction?")
        st.markdown("""
        <p>Factor construction is a method to synthetically create a portfolio based on given factor. The way to do this generally is to sort the security universe into 10 deciles ordered by some variable representing factor and then we go long for first decile and short on last decile.</p>
<p><b>Intuition</b>: We can express our bet on factor via synthetically creating a portfolio expressing the theme. &nbsp;</p>
        """, unsafe_allow_html=True)
        st.write("----")

        question("What is BAB?")
        st.markdown("""
        <p>BAB refers to Betting against beta strategy.</p>
<p>In simple terms, Long low beta securities and short high beta securities in a way that net position is dollar neutral.&nbsp;</p>
<p>Intuition: Leverage constrained investors like pension funds, buy high beta securities to replicate effect of leverage. This drives up their price and convergence to intrinsic value forces rational expected returns to fall.&nbsp;</p>
<p><br></p>
        """, unsafe_allow_html=True)
        st.write("----")

        question("What is Momentum?")
        st.markdown("""
        <p>Momentum is a factor where we go long the winners and short the losers.&nbsp;</p>
<p>Intuition: Price Inertia</p>
        """, unsafe_allow_html=True)
        st.write("----")

        question("How to add an index to the framework?")
        answer("To add a Index in this Framework, Add a csv file in data/index_csv")
        answer("<b>IMPORTANT</b>: The CSV file should have a SYMBOL Feature. Refer <i>'data/index_csv/SP500.csv'</i> to see the formatting. Also, Here's an example of code that downloads SP500 index from Wikipedia")
        st.markdown(
            """
<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">pandas</span> <span style="color: #008800; font-weight: bold">as</span> <span style="color: #0e84b5; font-weight: bold">pd</span>
<span style="color: #008800; font-weight: bold">try</span>:
    table <span style="color: #333333">=</span> pd<span style="color: #333333">.</span>read_html(
        <span style="background-color: #fff0f0">&#39;https://en.wikipedia.org/wiki/List_of_S%26P_500_companies&#39;</span>)
    df <span style="color: #333333">=</span> table[<span style="color: #0000DD; font-weight: bold">0</span>]
    df<span style="color: #333333">.</span>to_csv(<span style="background-color: #fff0f0">&#39;data/index_csv/SP500.csv&#39;</span>)
<span style="color: #008800; font-weight: bold">except</span>:
    <span style="color: #008800; font-weight: bold">print</span>(<span style="background-color: #fff0f0">&quot;Error in downloading SP500 index&quot;</span>)
</pre></div>
            """,
            unsafe_allow_html=True)
        st.write("----")

        question("What do you mean by Tracker and Tracker Config?")
        st.markdown("""
        <p>Tracker represent a config file that framework uses to download the data. If Tracker is not set then the Visualization/Hedging Pages won&apos;t work.</p>
<p>Available Tracker: This displays available config files with &apos;name&apos; representing name of Index, &apos;tickers&apos; represent number of tickers found in that index, &apos;current children&apos; represents the number of stock data downloaded.&nbsp;</p>
<p>Set Tracker: This will fetch all available trackers and point framework to the selected tracker.</p>
        """, unsafe_allow_html=True)
        st.write("----")

        question("How to add a feature to the data lake?")
        answer("To add a feature(s) to all the data, you can create a custom indicator.")
        answer(
            "Here's a sample code of an indicator stored in '<i>src/features/indicators</i>'")
        st.markdown("""
        <div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">from</span> <span style="color: #0e84b5; font-weight: bold">src.features.features</span> <span style="color: #008800; font-weight: bold">import</span> Feature
<span style="color: #008800; font-weight: bold">class</span> <span style="color: #BB0066; font-weight: bold">Custom_indicator</span>(Feature):
    <span style="color: #008800; font-weight: bold">def</span> <span style="color: #0066BB; font-weight: bold">__init__</span>(<span style="color: #007020">self</span>, name, parent, requires<span style="color: #333333">=</span>[<span style="background-color: #fff0f0">&quot;Open&quot;</span>, <span style="background-color: #fff0f0">&quot;Close&quot;</span>]):
        <span style="color: #007020">self</span><span style="color: #333333">.</span>name <span style="color: #333333">=</span> name
        <span style="color: #007020">self</span><span style="color: #333333">.</span>requires <span style="color: #333333">=</span> requires
        <span style="color: #007020">self</span><span style="color: #333333">.</span>parent <span style="color: #333333">=</span> parent
        <span style="color: #007020">self</span><span style="color: #333333">.</span>register()
    <span style="color: #008800; font-weight: bold">def</span> <span style="color: #0066BB; font-weight: bold">indicator</span>(<span style="color: #007020">self</span>, data):
        ans <span style="color: #333333">=</span> data
        ans <span style="color: #333333">=</span> ans<span style="color: #333333">.</span>rename(columns<span style="color: #333333">=</span>{<span style="background-color: #fff0f0">&quot;Open&quot;</span>: <span style="background-color: #fff0f0">&quot;Feature1&quot;</span>, <span style="background-color: #fff0f0">&quot;Close&quot;</span>: <span style="background-color: #fff0f0">&quot;Feature3&quot;</span>})
        <span style="color: #008800; font-weight: bold">return</span> ans
</pre></div>
<br>
<p>Class Description:</p>
<p>The class inherits Feature class, so that the framework can read, &amp; register the custom indicator. The requires parameter can be used to fetch previous features for example in this case, I&apos;m pulling the Open and Close of stock and performing simple renaming on that DataFrame.&nbsp;</p>
<p>Usage:</p>
<p>The custom indicator is accessed through &apos;<em>src/pages/data</em>&apos; file where it dumps the indicator into pickle file stored at &apos;<em>data/features/__name__</em>&apos; with a reference of the parent object and then we can use apply feature function to add those indicator.&nbsp;</p>
<div style='color: rgb(212, 212, 212); background-color: rgb(30, 30, 30); font-family: Menlo, Monaco, "Courier New", monospace; font-size: 12px; line-height: 18px; white-space: pre;'>c = Custom_indicator(<span style="color: rgb(156, 220, 254);">name</span>=<span style="color: rgb(206, 145, 120);">&quot;Custom&quot;</span>, <span style="color: rgb(156, 220, 254);">parent</span>=gov.population[loc[<span style="color: rgb(181, 206, 168);">0</span>]])</div>
<p>&nbsp;</p>
        """, unsafe_allow_html=True)
        st.write("----")

        question("How to use Viz?")
        st.markdown("""
        <p>Visualization Page has multiple functions to play with:</p>
<ol>
	<li><strong>Check Dataset</strong>: Pulls up a particular stock and display the data</li>
	<li><strong>Plot Multiple Tickers into one graph</strong>: The name defines itself. At the backend, it pulls up selected stock, chooses the target variable, and use Altair library for plotting.</li>
	<li><strong>Add Features</strong>: Used to add custom indicators to the data lake. Custom Indicator could be anything, for example, Simple Moving Average.</li>
	<li><strong>Remove Features</strong>: Used to delete features from the data</li>
</ol>
        """, unsafe_allow_html=True)
        st.write("----")

        question("How to create factor?")
        st.markdown("""
        <p>The factors construction code is stored in &apos;<em>src/hedging/factors</em>&apos;. &nbsp;I have constructed two different types of parsers to incorporate this factors into the framework. FYI, this parsers are called from &apos;<em>src/pages/hedging</em>&apos;. Refer functions, Hedge and Hedge_Dataframe to see how this factors are parsed and how the dollar neutral hedging is performed.</p>
<p>More details on Github Page.&nbsp;</p>
        """, unsafe_allow_html=True)
        st.write("----")

    st.write("## Future Work")
    st.markdown("""
    <ol>
    <li>Add more Factors</li>
    <li>Incorporate TA-Lib with Feature set</li>
    <li>Add multiple user interface</li>
    <li>Checkout more TODOs on Github Page</li>
    </ol>
    """, unsafe_allow_html=True)

    st.write("## Credits")
    st.markdown("""
<ol>
    <li>Big round of thanks to <a href="https://insightfellows.com">Insight</a> community for helping me create this framework.</li>
    <li>I would also like to thank <a href="https://www.streamlit.io">Streamlit</a> community for helping me create this Web Application</li>
    <li>The codebase of this web application is inspired from <a href="https://www.linkedin.com/in/marcskovmadsen">Mark Skov Madsen</a>&apos;s <a href="https://github.com/MarcSkovMadsen/awesome-streamlit">Awesome-Streamlit</a>&nbsp;</li>
</ol>
<p><br></p>
    """, unsafe_allow_html=True)
