import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_sanity_check(df):
    
    print(f"--- Dataset Overview ({len(df)} Products) ---")
    print(f"Average Rating Variance (Std): {df['rating_std'].mean():.3f}")
    print(f"Average Listing Subjectivity: {df['listing_sub_first'].mean():.3f}")
    
    top_number = 10
    # 1. The "Controversial" Kings (High Variance)
    print(f"\n### Top {top_number} Most Controversial Products (Highest Rating Std):")
    controversial = df.sort_values('rating_std', ascending=False).head(top_number)
    for _, row in controversial.iterrows():
        print(f"- {row['product_title_first']} (Std: {row['rating_std']:.2f}, Subj: {row['listing_sub_first']:.2f})")

    # 2. The "Persuasive" Sellers (High Subjectivity)
    print(f"\n### Top {top_number} Most Subjective Listings:")
    subjective = df.sort_values('listing_sub_first', ascending=False).head(top_number)
    for _, row in subjective.iterrows():
        print(f"- {row['product_title_first']} (Subj: {row['listing_sub_first']:.2f}, Std: {row['rating_std']:.2f})")
def show_subjectivity_plot(df):
    # Calculate Pearson Correlation
    r_val = df['listing_sub_first'].corr(df['rating_std'])

    print(f"Overall Correlation (Subjectivity -> Variance): {r_val:.3f}")

    # Visualize the 'Fan Effect'
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='listing_sub_first', y='rating_std', 
                scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title(f'Health & Personal Care: Market-wide Subjectivity Effect (r={r_val:.3f})')
    plt.show()


def normalized_sentiment(df):
    # Normalizing both to a 0-1 scale to compare apples to apples
    df['norm_rating'] = (df['rating_mean'] - 1) / 4
    df['norm_sentiment'] = (df['review_pol_mean'] + 1) / 2 # Assuming pol is -1 to 1

    # The 'Gap': Positive means the text is 'nicer' than the stars suggest
    df['sentiment_gap'] = df['norm_sentiment'] - df['norm_rating']

    print(f"Average Sentiment Gap: {df['sentiment_gap'].mean():.3f}")
    print(f"Correlation (Listing Subj vs. Sentiment Gap): {df['listing_sub_first'].corr(df['sentiment_gap']):.3f}")
if __name__ == "__main__":
    products_pkl_path =  "data/processed/health_and_personal_care_products.pkl"
    df = pd.read_pickle(products_pkl_path)
    # run_sanity_check(df)
    # show_subjectivity_plot(df)
    # normalized_sentiment(df)

