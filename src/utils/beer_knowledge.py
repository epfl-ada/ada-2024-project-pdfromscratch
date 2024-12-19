import pandas as pd
import numpy as np


def number_of_beer_per_style(df_ratings: pd.DataFrame) -> pd.DataFrame:
    df_beer_first_app = (
        df_ratings[["beer_id", "day", "beer_global_style"]]
        .groupby(["beer_global_style", "beer_id"])
        .min()
        .reset_index()
    )
    df_beer_first_app = pd.concat(
        [
            df_beer_first_app,
            pd.get_dummies(df_beer_first_app["beer_global_style"], prefix="max").astype(
                int
            ),
        ],
        axis=1,
    ).drop(["beer_global_style", "beer_id"], axis=1)
    df_new_beer_per_day_style = (
        df_beer_first_app.groupby("day")
        .sum()
        .sort_values(by="day")
        .reset_index()
    )
    df_current_beer_per_style = pd.concat(
        [
            df_new_beer_per_day_style["day"],
            df_new_beer_per_day_style.drop("day", axis=1).cumsum(),
        ],
        axis=1,
    )

    df_dates = pd.DataFrame(
        {
            "day": pd.date_range(
                start=pd.to_datetime(df_ratings["day"].min()),
                end=pd.to_datetime(df_ratings["day"].max()),
                freq="D",
            )
        }
    )
    df_current_beer_per_style = df_dates.merge(df_current_beer_per_style, how="left", on="day").sort_values(by="day").ffill()

    return df_current_beer_per_style


def add_global_knowledge(
    df_current_beer_per_style_year: pd.DataFrame,
    df_users_past_beer_style: pd.DataFrame,
    count_columns: list,
) -> tuple[pd.DataFrame]:
    n_beer_style = len(count_columns)
    df_mean_beers = pd.concat(
        [
            df_current_beer_per_style_year["day"],
            df_current_beer_per_style_year.iloc[:, 1:].mean(axis=1),
        ],
        axis=1,
    ).rename(columns={0: "mean_beers"})

    df_users_past_beer_style["style_tried"] = np.sign(
        df_users_past_beer_style[count_columns]
    ).sum(axis=1)
    df_users_past_beer_style["style_tried_share"] = (
        df_users_past_beer_style["style_tried"] / n_beer_style
    )
    df_users_past_beer_style["mean_beer_tried"] = (
        df_users_past_beer_style[count_columns].sum(axis=1)
        / df_users_past_beer_style["style_tried"]
    )
    df_users_past_beer_style = df_users_past_beer_style.merge(
        df_mean_beers, how="left", on="day"
    )

    df_users_past_beer_style.loc[
        df_users_past_beer_style["style_tried"] == 0, "mean_beer_tried"
    ] = 0

    df_users_past_beer_style["global_knowledge"] = (
        df_users_past_beer_style["style_tried_share"]
        * np.log(1 + df_users_past_beer_style["mean_beer_tried"])
        / np.log(1 + df_users_past_beer_style["mean_beers"])
    )

    return df_users_past_beer_style


def add_local_knowledge(
    df_current_beer_per_style_year: pd.DataFrame,
    df_users_past_beer_style: pd.DataFrame,
    max_columns: list,
    count_columns: list,
) -> tuple[pd.DataFrame]:
    df_users_past_beer_style = df_users_past_beer_style.merge(
        df_current_beer_per_style_year, how="left", on="day"
    )
    df_users_past_beer_style.sort_values(by=["user_id","day"]+count_columns)
    df_users_past_beer_style[max_columns] = df_users_past_beer_style[
        max_columns
    ].ffill()

    df_shares_by_style = pd.DataFrame(
        df_users_past_beer_style[count_columns].values
        / df_users_past_beer_style[max_columns].values
    )

    df_local_knowledge = np.pow(df_shares_by_style, 1 / 3)
    df_local_knowledge.rename(
        columns={
            0: "Bock",
            1: "Brown Ale",
            2: "Dark Ales",
            3: "Dark Lager",
            4: "Hybrid Beer",
            5: "India Pale Ale",
            6: "Pale Ale",
            7: "Pale Lager",
            8: "Porter",
            9: "Speciality Beer",
            10: "Stout",
            11: "Strong Ale",
            12: "Wheat Beer",
            13: "Wild/Sour Beer",
        },
        inplace=True,
    )
    df_local_knowledge = df_local_knowledge.merge(
        df_users_past_beer_style[["user_id", "day","beer_id"]],
        how="inner",
        left_index=True,
        right_index=True,
    )
    df_users_past_beer_style["local_knowledge"] = df_local_knowledge.iloc[:, :-3].max(
        axis=1
    )

    return df_users_past_beer_style, df_local_knowledge


def add_experts(
    df_local_knowledge: pd.DataFrame, df_users_past_beer_style: pd.DataFrame, quantile_thresh: float,
) -> tuple[pd.DataFrame]:
    df_best_local_per_user = (
        df_local_knowledge.iloc[:, :-1].groupby("user_id").max().reset_index()
    )
    local_knowledge_quantile_expert = df_best_local_per_user.iloc[:, 1:].quantile(quantile_thresh)
    above_percentiles = (
        df_local_knowledge.iloc[:, :-2]
        .gt(local_knowledge_quantile_expert, axis=1)
        .astype(int)
    )
    for col in above_percentiles.columns:
        above_percentiles.rename(columns={col: col + "_expert"}, inplace=True)
    df_users_past_beer_style = df_users_past_beer_style.merge(
        above_percentiles, how="inner", left_index=True, right_index=True
    )
    return df_users_past_beer_style, local_knowledge_quantile_expert


def get_expert_per_day(
    df_ratings: pd.DataFrame,
    df_users_past_beer_style: pd.DataFrame,
    max_available_beer_per_day: pd.DataFrame,
    expert_columns: list,
    count_columns: list,
) -> pd.DataFrame:
    df_dates = pd.DataFrame(
        {
            "day": pd.date_range(
                start=pd.to_datetime(df_ratings["day"].min()),
                end=pd.to_datetime(df_ratings["day"].max()),
                freq="D",
            )
        }
    )
    ever_local_expert = df_users_past_beer_style.loc[
        df_users_past_beer_style[expert_columns].sum(axis=1) >= 1, "user_id"
    ].drop_duplicates()
    df_expert_dates = df_dates.merge(
        max_available_beer_per_day, how="left", on="day"
    ).ffill()
    df_expert_dates = df_expert_dates.merge(ever_local_expert, how="cross")
    df_expert_dates = df_expert_dates.merge(
        df_users_past_beer_style[count_columns + ["user_id", "day"]],
        how="left",
        on=["user_id", "day"],
    )
    df_expert_dates.loc[
        (df_expert_dates["day"] == "1996-08-22")
        & (df_expert_dates["user_id"] != "todd.2"),
        count_columns,
    ] = 0
    filled_expert = (
        df_expert_dates.sort_values(by=["user_id", "day"])
        .groupby("user_id")
        .ffill()
    )
    filled_expert = filled_expert.merge(
        df_expert_dates["user_id"], left_index=True, right_index=True, how="left"
    )
    filled_expert = filled_expert.groupby(["user_id", "day"]).max().reset_index()

    filled_columns = filled_expert.columns

    comparison_results = {}
    for i in range(len(count_columns)):
        col_a = filled_columns[i + 2]
        col_b = filled_columns[i + 16]
        comparison_name = f"expert_{col_a}"

        comparison_results[comparison_name] = (
            filled_expert[col_b] >= filled_expert[col_a]
        )

    comparison_df = pd.DataFrame(comparison_results).astype(int)

    expert_per_day = (
        comparison_df.merge(
            filled_expert["day"], how="inner", left_index=True, right_index=True
        )
        .groupby("day")
        .sum()
        .reset_index()
    )
    return expert_per_day


def get_global_expert_per_day(
    df_ratings: pd.DataFrame,
    df_knowledge: pd.DataFrame,
    df_users_past_beer_style: pd.DataFrame,
) -> pd.DataFrame:
    df_best_global_per_user = (
        df_knowledge[["user_id", "global_knowledge"]]
        .groupby("user_id")
        .max()
        .reset_index()
    )
    global_knowledge_quantile_expert = df_best_global_per_user.loc[
        :, "global_knowledge"
    ].quantile(0.99)

    df_dates = pd.DataFrame(
        {
            "day": pd.date_range(
                start=pd.to_datetime(df_ratings["day"].min()),
                end=pd.to_datetime(df_ratings["day"].max()),
                freq="D",
            )
        }
    )
    df_dates = (
        df_dates.merge(
            df_users_past_beer_style[["day", "mean_beers"]].drop_duplicates(),
            how="left",
            on="day",
        )
        .sort_values(by="day")
        .ffill()
    )
    ever_global_expert = df_knowledge.loc[
        df_knowledge["global_knowledge"] >= global_knowledge_quantile_expert, "user_id"
    ].drop_duplicates()

    df_global_expert_dates = df_dates.merge(ever_global_expert, how="cross")
    df_global_expert_dates = df_global_expert_dates.merge(
        df_users_past_beer_style[
            ["user_id", "day", "style_tried_share", "mean_beer_tried"]
        ],
        how="left",
        on=["user_id", "day"],
    )
    filled_global_expert = (
        df_global_expert_dates.sort_values(by=["user_id", "day"])
        .groupby("user_id")
        .ffill()
        .bfill()
    )
    filled_global_expert = filled_global_expert.merge(
        df_global_expert_dates["user_id"], left_index=True, right_index=True, how="left"
    )
    filled_global_expert["global_knowledge"] = (
        filled_global_expert["style_tried_share"]
        * np.log(1 + filled_global_expert["mean_beer_tried"])
        / np.log(1 + filled_global_expert["mean_beers"])
    )

    filled_global_expert["active_expert"] = (
        filled_global_expert["global_knowledge"] >= global_knowledge_quantile_expert
    ).astype(int)

    global_active_user_per_day = (
        filled_global_expert[["user_id", "day", "active_expert"]]
        .groupby(["user_id", "day"])
        .max()
        .reset_index()
        .iloc[:, 1:]
        .groupby("day")
        .sum()
        .reset_index()
    )

    return global_active_user_per_day
