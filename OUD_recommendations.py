# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PY
# OUD, ZIE RECOMMENDATIONENGINE.PYv







# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer

# def get_dataframe_from_products(products=None):
#     """Create a dataframe from product data."""
#     if products:
#         data = [{"Handle": p[0], "Title": p[1], "Tags": " ".join(p[4]), "Body": p[2]} for p in products]
#         print("Dataframe dynamically created from products.")
#     else:
#         data = pd.read_csv('products.csv', encoding='latin-1').dropna()
#         data = data[['Handle', 'Title', 'Tags', 'Body (HTML)']].rename(columns={"Body (HTML)": "Body"})

#     df = pd.DataFrame(data).set_index('Handle')
#     df['Features'] = df['Tags'] + ' ' + df['Body']
#     return df

# def calculate_similarity(df, column_name):
#     """Calculate similarity scores for a given column."""
#     tfidf = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = tfidf.fit_transform(df[column_name])
#     return cosine_similarity(tfidf_matrix)

# def get_recommendations(handle, products=None, num_recs=99999, weight_factor=0.5):
#     """Get product recommendations based on similarity scores."""
#     df = get_dataframe_from_products(products)

#     # Calculate similarity for both tags and body
#     cosine_sim_tags = calculate_similarity(df, 'Tags')
#     cosine_sim_body = calculate_similarity(df, 'Features')

#     idx = df.index.get_loc(handle)

#     # Combine scores with weighting
#     combined_scores = [(i, weight_factor * cosine_sim_tags[idx][i] + (1 - weight_factor) * cosine_sim_body[idx][i]) for i in range(len(df))]
#     sorted_scores = sorted(combined_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]

#     recommendations = [{'product_handle': df.index[i[0]], 'similarity_score': i[1]} for i in sorted_scores]
#     return [r['product_handle'] for r in recommendations], [r['similarity_score'] for r in recommendations]
