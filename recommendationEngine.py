import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import SVD, Dataset, Reader


def get_dataframe_from_products(products):
    """Create a dataframe from product data."""
    data = [{"Handle": p[0], "Title": p[1], "Tags": " ".join(p[4]), "Body": p[2]} for p in products]
    df = pd.DataFrame(data).set_index('Handle')
    df['Features'] = df['Tags'] + ' ' + df['Body']
    return df


def calculate_similarity(df, column_name):
    """Calculate similarity scores for a given column."""
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df[column_name])
    return cosine_similarity(tfidf_matrix)


def get_content_based_recs(df_products, product_idx, cosine_sim_body, cosine_sim_tags, weight_factor, handle):
    """Get content-based recommendations with weighted scores, excluding the product itself."""
    content_scores = [
        (df_products.index[i], weight_factor * cosine_sim_tags[product_idx][i] + (1 - weight_factor) * cosine_sim_body[product_idx][i]) 
        for i in range(len(df_products)) if df_products.index[i] != handle
    ]
    return content_scores


def parse_line_items(order_data):
    """Parse the line items from the order data."""
    product_combinations_map = {}

    for order in order_data:
        if isinstance(order, tuple):
            _, _, _, line_items = order
        else:
            line_items = order['lineItems']

        product_handles = [item['handle'] for item in line_items]
        for handle in product_handles:
            for other_handle in product_handles:
                if handle != other_handle:
                    product_combinations_map.setdefault(handle, {}).setdefault(other_handle, 0)
                    product_combinations_map[handle][other_handle] += 1

    return product_combinations_map


def collaborative_filtering(product_combinations_map):
    """Implement collaborative filtering based on product combinations."""
    data = []
    for product_handle, combinations in product_combinations_map.items():
        for other_handle, count in combinations.items():
            data.append({'product_handle': product_handle, 'other_handle': other_handle, 'rating': count})
    df = pd.DataFrame(data)
    reader = Reader(rating_scale=(0, max(df['rating'])))
    data = Dataset.load_from_df(df[['product_handle', 'other_handle', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD(n_factors=150, n_epochs=30, lr_all=0.005, reg_all=0.02)
    algo.fit(trainset)
    return algo


def get_collaborative_recs(svd_model, product_handle, products):
    """Get collaborative filtering recommendations."""
    product_handles = [p for p in products if p != product_handle]
    predictions = [svd_model.predict(product_handle, other_handle) for other_handle in product_handles]
    return [(pred.iid, pred.est) for pred in predictions]


def get_recommendations_please(handle, products, orders=None, customer_id=None, num_recs=99999, weight_factor=0.5):
    """Generate product recommendations for content-based and collaborative filtering."""
    df_products = get_dataframe_from_products(products)
    product_idx = df_products.index.get_loc(handle)

     # Content-Based Filtering
    cosine_sim_body = calculate_similarity(df_products, 'Features')
    cosine_sim_tags = calculate_similarity(df_products, 'Tags')
    content_based_recs = get_content_based_recs(df_products, product_idx, cosine_sim_body, cosine_sim_tags, weight_factor, handle)

    # Collaborative Filtering
    product_combinations_map = parse_line_items(orders)
    
    for product_handle in df_products.index:
        if product_handle != handle:
            product_combinations_map.setdefault(handle, {}).setdefault(product_handle, 0)
            product_combinations_map[handle][product_handle] += 1

    svd_model = collaborative_filtering(product_combinations_map)
    collaborative_recs = get_collaborative_recs(svd_model, handle, df_products.index)

    # Prepare final result
    combined_recs = combine_scores(content_based_recs, collaborative_recs, num_recs)

    return combined_recs


def combine_scores(content_based_recs, collaborative_recs, num_recs, content_weight=0.65, collaborative_weight=1):
    content_based_dict = dict(content_based_recs)
    collaborative_dict = dict(collaborative_recs)

    combined_scores = {}

    # Combineer de scores van beide aanbevelingssystemen met wegingen
    for product, score in content_based_dict.items():
        combined_score = score * content_weight + collaborative_dict.get(product, 0) * collaborative_weight
        combined_scores[product] = combined_score

    for product, score in collaborative_dict.items():
        if product not in combined_scores:
            combined_scores[product] = score * collaborative_weight

    # Sorteer de producten op basis van hun gecombineerde score en beperk de lijst tot het gewenste aantal aanbevelingen
    sorted_products = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)[:num_recs]


    recommendation_handles = [product[0] for product in sorted_products]
    recommendation_scores = [product[1] for product in sorted_products]

    return recommendation_handles, recommendation_scores
