import pandas as pd
import json
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

def get_content_based_recs(cosine_sim, product_idx, num_recs):
    """Get content-based recommendations."""
    scores = cosine_sim[product_idx]
    sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[1:num_recs+1]
    return sorted_scores

# def combine_recommendations(content_based_recs, collaborative_recs, num_recs):
#     """Combine content-based and collaborative recommendations."""
#     combined = set([rec[0] for rec in content_based_recs] + collaborative_recs)
#     return list(combined)[:num_recs]

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
    algo = SVD()
    algo.fit(trainset)
    return algo

def get_collaborative_recs(svd_model, product_handle, products, num_recs):
    product_handles = [p[0] for p in products if p[0] != product_handle]  # exclude the given product_handle
    predictions = [svd_model.predict(product_handle, other_handle) for other_handle in product_handles]
    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:num_recs]
    return [pred.iid for pred in sorted_predictions]

def get_recommendations_please(handle, products, orders=None, customer_id=None, num_recs=99999, weight_factor=0.5):
    """Generate product recommendations for content-based and collaborative filtering."""
    df_products = get_dataframe_from_products(products)
    product_idx = df_products.index.get_loc(handle)

    # Content-Based Filtering
    cosine_sim_body = calculate_similarity(df_products, 'Features')
    cosine_sim_tags = calculate_similarity(df_products, 'Tags')
    content_scores = [(df_products.index[i], weight_factor * cosine_sim_tags[product_idx][i] + (1 - weight_factor) * cosine_sim_body[product_idx][i]) for i in range(len(df_products))]
    sorted_content_scores = sorted(content_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]
    content_based_recs = [(rec[0], rec[1]) for rec in sorted_content_scores]

    # Collaborative Filtering
    product_combinations_map = parse_line_items(orders)

    if not customer_id:
        for product in products:
            if product[0] != handle:
                product_combinations_map.setdefault(handle, {}).setdefault(product[0], 0)
                product_combinations_map[handle][product[0]] += 1

    svd_model = collaborative_filtering(product_combinations_map)
    collaborative_predictions = [svd_model.predict(handle, other_handle) for other_handle in df_products.index]
    sorted_collaborative_predictions = sorted(collaborative_predictions, key=lambda x: x.est, reverse=True)[:num_recs]
    collaborative_recs = [(pred.iid, pred.est) for pred in sorted_collaborative_predictions]

    # Prepare final result
    content_based_product_handles = [rec[0] for rec in content_based_recs]
    content_based_scores = [rec[1] for rec in content_based_recs]
    collaborative_product_handles = [rec[0] for rec in collaborative_recs]
    collaborative_scores = [rec[1] for rec in collaborative_recs]

    return {
        "content_based_recommendations": content_based_product_handles,
        "content_based_scores": content_based_scores,
        "collaborative_recommendations": collaborative_product_handles,
        "collaborative_scores": collaborative_scores
    }   
