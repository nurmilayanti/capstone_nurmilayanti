import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import cartopy.crs as ccrs
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import altair as alt


st.set_page_config(layout='wide')
st.header('Product Analyst for Top 3 E-commerce in Indonesia')

df = pd.read_excel('top_3_ecommerce_edited2.1.xlsx')

produk_terjual_per_ecommerce = df.groupby('e_commerce')['prd_sales_1'].sum()
produk_per_ecommerce = df['e_commerce'].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.write('Jumlah Produk per per E-commerce') 
    st.bar_chart(produk_per_ecommerce,  use_container_width=True, color='#535C91')

with col2:
    st.write('Jumlah Produk Terjual per E-commerce') 
    st.bar_chart(produk_terjual_per_ecommerce, color='#535C91')


##



# Ensure there's data to plot

if not df.empty:
    fig = go.Figure()

    # Scatter plot based on product sales (single plot)
    st.write('hg')
    fig.add_trace(go.Scattergeo(
        lon=df['longitude'],
        lat=df['latitude'],
        mode='markers',
        marker=dict(
            size=10,
            opacity=0.8,
            color=df['prd_sales_1'],
            colorscale='viridis',
            colorbar=dict(
                title="Product Sales"
            )
        ),
        text=df['shop_loc']
    ))

    fig.update_geos(
        projection_type="orthographic",
        showocean=True,
        oceancolor="#0E1218",  # Warna laut yang lebih terang
        showland=True,
        landcolor="lightgray",   # Warna daratan yang lebih terang
        showcountries=True,
        countrycolor="white",    # Warna batas negara yang lebih terang
        countrywidth=1,
        showcoastlines=True,
        showframe=False,
        lataxis_range=[-10, 6],
        lonaxis_range=[90, 141]
    )

    fig.update_layout(
        #title='Product Sales Heatmap',
        width=1100,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth',
            bgcolor='rgba(2,0,0,0)'  # Set background color to transparent
            
        ),
        plot_bgcolor='rgba(0,0,0,0)' , # Set plot background color to transparent
        autosize=True,  # Mengaktifkan penyesuaian otomatis ukuran plot
    margin=dict(l=0, r=0, t=0, b=0) 
    )

    st.plotly_chart(fig)
else:
    st.write("No data available to plot.")

#####   
    
top_brands = df.groupby('merk')['prd_sales_1'].sum()
top_brands = top_brands.nlargest(5)
top_brands_df = pd.DataFrame({'Merk': top_brands.index, 'Number of Products Sold': top_brands.values})

# Kelompokkan DataFrame dan hitung total penjualan per merek per e-commerce

top_products_per_ecommerce = df.groupby(['e_commerce', 'merk'])['prd_sales_1'].sum().reset_index(name='prd_sales_1')

# Urutkan DataFrame berdasarkan e-commerce dan total penjualan secara menurun
top_products_per_ecommerce = top_products_per_ecommerce.sort_values(by=['e_commerce', 'prd_sales_1'], ascending=False)

# Ambil lima merek teratas per e-commerce
top_products_per_ecommerce = top_products_per_ecommerce.groupby('e_commerce').head(5)

plot_width = 600
plot_height = 400

# Create a Streamlit layout with two columns
col1, col2 = st.columns([2, 1]) 

# Inside col1, display the chart
with col1:
    chart = alt.Chart(top_products_per_ecommerce).mark_bar().encode(
        x='prd_sales_1:Q',
        y='merk:N',
        color=alt.Color('e_commerce:N', scale=alt.Scale(scheme='viridis')),
        tooltip=['prd_sales_1', 'merk', 'e_commerce']
    ).properties(
        width=plot_width,
        height=plot_height,
        title='Top Products per E-commerce'
    ).interactive()
    st.altair_chart(chart, use_container_width=False)

# Inside col2, display the table with adjusted right margin
with col2:
    st.write(
        """
        <div style="margin-right: 5px;">
            <h7>Top Selling Brands</h7>
            {}
        </div>
        """.format(top_brands_df.to_html()), 
        unsafe_allow_html=True
    )