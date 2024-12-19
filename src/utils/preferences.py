import pandas as pd
import networkx as nx

def analyse_relationships(dataframe: pd.DataFrame) -> pd.DataFrame:
    relationships = []
    for group_style in dataframe['beer_global_style'].unique():
        group = dataframe[dataframe['dominant_style'] == group_style]
        group_users = group['user_id'].unique()
        group_mean  = group['rating'].mean()

        for target_style in dataframe['beer_global_style'].unique():
            style_ratings = dataframe[
                (dataframe['user_id'].isin(group_users)) &
                (dataframe['beer_global_style'] == target_style)
            ]['rating'] - group_mean
            
            if not style_ratings.empty:
                relationships.append({
                    'group_style': group_style,
                    'target_style': target_style,
                    'mean_rating': style_ratings.mean(),
                    'std_rating': style_ratings.std(),
                    'num_ratings': style_ratings.count()
                })
    return pd.DataFrame(relationships)

def create_preference_digraph(dataframe: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()

    for _, row in dataframe.iterrows():
        if row['num_ratings'] > 200 and abs(row['mean_rating']) > 0.25:
            G.add_edge(
                row['group_style'], 
                row['target_style'], 
                weight=row['num_ratings'], 
                rating=row['mean_rating']
            )
        
    return G