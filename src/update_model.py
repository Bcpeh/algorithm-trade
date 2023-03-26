import feedparser
from src.utils import preprocess_text
import pandas as pd
def update_model(api, yahoo_news_rss_url,vectorizer):
    # Fetch the latest TSLA news data
    parsed_rss = feedparser.parse(yahoo_news_rss_url)
    latest_news_summary = parsed_rss.entries[0].summary

    # Preprocess the latest news summary
    cleaned_latest_summary = preprocess_text(latest_news_summary)

    # Transform the preprocessed summary into a feature vector
    latest_summary_vector = vectorizer.transform([cleaned_latest_summary]).toarray()

    # Create a DataFrame for the latest news summary
    latest_significant_words = pd.DataFrame(latest_summary_vector, columns=vectorizer.get_feature_names_out())

    # Fetch the latest TSLA historical data
    tsla_data = api.get_barset('TSLA', 'day', limit=1).df['TSLA'].reset_index()

    # Merge the latest TSLA historical data and latest_significant_words DataFrames
    tsla_data['date'] = pd.to_datetime(tsla_data['time']).dt.date
    latest_significant_words['date'] = parsed_rss.entries[0].published_parsed[:3]
    latest_merged_data = pd.merge(tsla_data, latest_significant_words, on='date', how='inner')

    # Update the training data and retrain the linear regression model
    global merged_data, X_train, y_train, lr_model
    merged_data = merged_data.append(latest_merged_data, ignore_index=True)
    X_train = merged_data.drop(['date', 'close'], axis=1)
    y_train = merged_data['close']
    lr_model.fit(X_train, y_train)
    print("Model updated with latest data.")