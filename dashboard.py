import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    
    return daily_orders_df

def create_by_season_df(df):
    df['season'] = df['season'].astype('category')
    df['season'] = df['season'].cat.rename_categories({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'})

    season_order_items_df = df.groupby("season", observed=True).agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False).reset_index()

    return season_order_items_df

def create_by_days_df(df):
    df['weekday'] = df['weekday'].astype('category')
    df['weekday'] = df['weekday'].cat.rename_categories({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})

    day_orders_items_df = df.groupby("weekday", observed=True).agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }, observed=True).sort_values(by='cnt', ascending=False).reset_index()

    return day_orders_items_df

def create_by_month_df(df):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
            6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
            11: 'November', 12: 'December'}

    df['mnth'] = df['mnth'].astype('category')
    df['mnth'] = df['mnth'].cat.rename_categories(months)

    month_order_items_df = df.groupby("mnth", observed=True).agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }, observed=True).sort_values(by='cnt', ascending=False).reset_index()

    return month_order_items_df

def create_by_year_df(df):
    df['yr'] = df['yr'].astype('category')
    df['yr'] = df['yr'].cat.rename_categories({0: 2011, 1: 2012})

    year_order_items_df = df.groupby(["yr", "season", "mnth"], observed=True).agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }, observed=True).sort_values(by='cnt', ascending=False).reset_index()

    return year_order_items_df

hour_df = pd.read_csv("hour.csv")
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

daily_df = pd.read_csv("day.csv")
daily_df.sort_values(by="dteday", inplace=True)
daily_df.reset_index(inplace=True)

df_cluster = pd.read_csv("df_cluster.csv")

# st.write(cluster_df)


hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])

min_date = daily_df["dteday"].min()
max_date = daily_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("https://static.wikia.nocookie.net/fategrandorder/images/a/a7/Gudao_Command_Seal.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = daily_df[(daily_df["dteday"] >= str(start_date)) & 
                (daily_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
season_order_items_df = create_by_season_df(main_df)
month_order_items_df = create_by_month_df(main_df)
day_order_items_df = create_by_days_df(main_df)
year_order_items_df = create_by_year_df(main_df)

st.header('Revanantyo Dwigantara Simple Dashboard')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.casual.sum()
    st.metric("Total casual customer:", value=total_orders)

with col2:
    total_orders = daily_orders_df.registered.sum()
    st.metric("Total registered customer:", value=total_orders)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Persebaran Pelanggan")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 15))

    sns.barplot(
        y="cnt", 
        x="season",
        data=season_order_items_df.sort_values(by="cnt", ascending=False),
        hue="season",
        palette='RdBu',
        ax=ax
    )
    ax.set_title("Total orders by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 15))

    sns.barplot(
        x="cnt", 
        y="weekday",
        data=day_order_items_df.sort_values(by="cnt", ascending=False),
        hue="weekday",
        palette="flare",
        ax=ax
    )
    ax.set_title("Total orders by days", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    x="cnt", 
    y="mnth",
    data=month_order_items_df.sort_values(by="cnt", ascending=False),
    hue="mnth",
    palette='autumn',
    ax=ax
)
ax.set_title("Total orders by months", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

col1, col2 = st.columns([1, 2])

# st.write(year_order_items_df, month_order_items_df)

with col1:
    fig, ax = plt.subplots(figsize = (4, 6))

    # sns.countplot(x='yr', y='cnt', hue='season', data=year_order_items_df.sort_values(by="cnt", ascending=False), palette='flare')
    sns.barplot(x = "yr", y = "cnt", hue='season', data = year_order_items_df.sort_values(by='cnt', ascending=False), palette = sns.color_palette(palette = ["SteelBlue" , "Salmon", "Crimson", "MediumSlateBlue"], n_colors = 4))
    
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize = (5, 6))

    # sns.countplot(x='yr', y='cnt', hue='season', data=year_order_items_df.sort_values(by="cnt", ascending=False), palette='flare')
    sns.barplot(x = "cnt", y = "yr", hue='mnth', data = year_order_items_df.sort_values(by='cnt', ascending=False), palette = 'flare_r')
    
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Persebaran Pelanggan Berdasarkan Pengelompokkan (Clustering)")

fig, ax = plt.subplots(figsize=(5, 3))
plt.scatter(df_cluster.total[df_cluster.cluster_id == 0], df_cluster['registered'][df_cluster.cluster_id == 0], color = 'Salmon', s=30, edgecolor = 'black', label= '0')
plt.scatter(df_cluster.total[df_cluster.cluster_id == 1], df_cluster['registered'][df_cluster.cluster_id == 1], color = 'SteelBlue', s=30, edgecolor = 'black', label = '1')
plt.scatter(df_cluster.total[df_cluster.cluster_id == 2], df_cluster['registered'][df_cluster.cluster_id == 2], color = 'Tan', s=30, edgecolor = 'black', label = '2')

plt.legend(title= "Cluster ID", labelspacing=1.5, borderpad=1)
plt.xlabel('total')
plt.ylabel('registered')
st.pyplot(fig)

st.subheader("Persebaran Pelanggan Pada Cluster 2 (Kelompok Pelanggan Paling Sedikit)")

col1, col2 = st.columns(2)

cluster0 = df_cluster[df_cluster.cluster_id == 0]
cluster1 = df_cluster[df_cluster.cluster_id == 1]
cluster2 = df_cluster[df_cluster.cluster_id == 2]

with col1:
    fig, ax = plt.subplots(figsize=(5, 4))
    plt.title('Persebaran pelanggan berdasarkan musim (cluster 2)')
    plt.xlabel('Count')
    plt.ylabel('Season')

    sns.barplot(y=cluster2['season'].value_counts().keys().to_list(), hue=cluster2['season'].value_counts().keys().to_list(), x=cluster2['season'].value_counts().to_list(), palette='RdBu')

    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{int(width)}', (width, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', xytext=(-30, 0), textcoords='offset points')


    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 6))
    plt.title('Persebaran pelanggan berdasarkan bulan (cluster 2)')
    plt.xlabel('Count')
    plt.ylabel('Months')

    sns.barplot(y=cluster2['month'].value_counts().keys().to_list(), hue=cluster2['month'].value_counts().keys().to_list(), x=cluster2['month'].value_counts().to_list(), palette='YlOrRd_r')

    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{int(width)}', (width, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', xytext=(-30, 0), textcoords='offset points')


    plt.tight_layout()
    st.pyplot(fig)