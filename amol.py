import osmnx as ox
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# گرفتن نقاط خدمات شهری آمل
place_name = "Amol, Iran"
tags = {
    'amenity': True,
    'office': True,
    'leisure': True
}
pois = ox.features_from_place(place_name, tags)
pois = pois[pois.geometry.type == 'Point']

# ساخت دیکشنری رنگ برای هر نوع خدمات
color_dict = {
    'school': 'blue',
    'bank': 'red',
    'mosque': 'green',
    'restaurant': 'purple',
    'hospital': 'darkred',
    'clinic': 'orange',
    'cafe': 'cadetblue',
    'fire_station': 'darkpurple',
    'police': 'darkblue',
    'pharmacy': 'lightred',
    'college': 'lightblue',
    'university': 'beige',
    'kindergarten': 'lightgreen',
    'library': 'darkgreen',
    'post_office': 'lightgray',
    'cinema': 'pink',
    'marketplace': 'black',
    'embassy': 'gray',
    'community_centre': 'white',
    'courthouse': 'darkgray',
    'townhall': 'darkgreen',
    'public_building': 'gray',
    'government': 'gray',
    'other': 'lightgray'
}

# ساخت نقشه آمل
map_amol = folium.Map(location=[36.4704, 52.3468], zoom_start=14)
marker_cluster = MarkerCluster().add_to(map_amol)

# افزودن مارکرها به نقشه
for idx, row in pois.iterrows():
    lat = row.geometry.y
    lon = row.geometry.x

    # شناسایی نوع خدمات
    point_type = None
    for key in ['amenity', 'office', 'leisure']:
        if key in row and pd.notnull(row[key]):
            point_type = row[key]
            break

    # تعیین نام و رنگ
    name = row['name'] if 'name' in row and pd.notnull(row['name']) else 'نام ندارد'
    color = color_dict.get(point_type, 'gray')
    popup = f"{point_type}: {name}"

    # حذف نقاط بی‌نام و ناشناخته
    if point_type is None and name == 'نام ندارد':
        continue

    folium.Marker(
        location=[lat, lon],
        popup=popup,
        tooltip=point_type,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(marker_cluster)

# ذخیره خروجی
map_amol.save("amol_services_colored_clustered.html")
print("✅ نقشه با خوشه‌بندی و رنگ‌بندی ذخیره شد.")
