import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Laad producten in via CSV (wordt database, lijkt mij)
df = pd.read_csv('products.csv', encoding='latin-1', sep=',')

# Simpele data voorverwerking
df = df[['Handle', 'Title', 'Tags', 'Body (HTML)']]
df = df.dropna()
df = df.set_index('Handle')

# Voeg zowel tags als body samen in een nieuwe kolom genaamd Features
df['Features'] = df['Tags'] + ' ' + df['Body (HTML)']

# TF-IDF matrix dingen - zie https://en.wikipedia.org/wiki/Tf%E2%80%93idf
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Features'])

# Cosinus vergelijkings matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Functie om aanbevelingen te genereren
def get_recommendations(title, cosine_sim=cosine_sim, df=df, num_recs=15, weight_factor=0.5):
    # Krijg de index van het product dat overeenkomt met de titel
    idx = df.index.get_loc(title)

    # Krijg scores voor overeenkoming op basis van de tags
    tfidf_tags = TfidfVectorizer(stop_words='english')
    tfidf_tags_matrix = tfidf_tags.fit_transform(df['Tags'])
    cosine_sim_tags = cosine_similarity(tfidf_tags_matrix)
    sim_scores_tags = list(enumerate(cosine_sim_tags[idx]))

    # Krijg scores voor overeenkoming op basis van de beschrijving uit Body (HTML)
    sim_scores_body = list(enumerate(cosine_sim[idx]))

    # Combineer de scores maar neem een wegingsfactor mee, dit omdat de tag man of vrouw bijvoorbeeld zwaarder moet wegen dan de beschrijving
    sim_scores = [(i[0], weight_factor * sim_scores_tags[i[0]][1] + (1 - weight_factor) * i[1]) for i in sim_scores_body]

    # Sorteer de producten op basis van de scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Krijg de top 5 meest overeenkomende producten en hun scores
    sim_scores = sim_scores[1:num_recs+1]
    product_indices = [i[0] for i in sim_scores]
    similarity_scores = [i[1] for i in sim_scores]

    # Create a list of dictionaries containing the product title and similarity score for each recommendation
    # Maak een lijst van de aanbevelingen en hun scores
    recommendations = []
    for i in range(len(product_indices)):
        recommendation = {}
        recommendation['product_title'] = df.iloc[product_indices[i]]['Title']
        recommendation['similarity_score'] = similarity_scores[i]
        recommendations.append(recommendation)

    # Return de top 5 meest overeenkomende producten en hun scores
    return [recommendations[i]['product_title'] for i in range(len(recommendations))], similarity_scores

# Testfunctionaliteit
# recs, scores = get_recommendations('red-sports-tee', num_recs=4)
# print(recs)
# print(scores)