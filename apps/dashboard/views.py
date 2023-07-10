"""
Request handlers/action
"""

import folium
import pandas as pd
from django.shortcuts import render
import geopandas as pd
import logging
logger = logging.getLogger(__name__)
# import geopandas as gpd
from django.views.generic.base import TemplateView

from apps.dashboard.models import WorldHealthStatistics
from  django.views.generic.base import ContextMixin


# https://stackoverflow.com/questions/35925391/serving-multiple-templates-from-a-single-view-or-should-i-use-multiple-views
class BaseContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context_data = super(BaseContextMixin, self).get_context_data(**kwargs)
        context_data["health_data"] = WorldHealthStatistics.objects.all()
        return context_data
    
class WorlMapView(TemplateView, BaseContextMixin):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context_data = super(WorlMapView, self).get_context_data(**kwargs)

        # map
        map = folium.Map([51.5, -0.25], zoom_start=10)
        map = map._repr_html_()
        context_data['health_stats_map1'] = map
        return context_data

    def create_map(map_name, legend_name, geo_df, col_name, sex):
        if sex:
            plot_df = geo_df.query('sex == "' + sex + '"')
        else:
            plot_df = geo_df
        # https://towardsdatascience.com/folium-and-choropleth-map-from-zero-to-pro-6127f9e68564
        # add folium code from jupyter here and make it generic
        world_map = folium.Map(location=[31, 30], zoom_start=2, tiles="openstreetmap")
        # custom_scale = (
        #     geo_df["deaths_per_1lac_diabetes"].quantile((0, 0.2, 0.4, 0.6, 0.8, 1))
        # ).tolist()  # optional

        folium.Choropleth(
            geo_data="./static/countries.geo.json",
            name="choropleth",
            data=plot_df,
            columns=["id", col_name],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            nan_fill_color="White",  # Use white color if there is no data available for the county,
            highlight=True,
            line_color="black",
            #     threshold_scale=custom_scale,  # use the custom scale we created for legend
        ).add_to(world_map)

        folium.LayerControl().add_to(world_map)

        # Add Customized Tooltips to the map - not working yet
        folium.features.GeoJson(
            data=plot_df,
            name=map_name,
            smooth_factor=2,
            style_function=lambda x: {
                "color": "black",
                "fillColor": "transparent",
                "weight": 0.5,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=["id", col_name],
                aliases=["Country:", map_name+":"],
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border: 2px solid black;
                    border-radius: 3px;
                    box-shadow: 3px;
                """,
                max_width=800,
            ),
            highlight_function=lambda x: {"weight": 3, "fillColor": "grey", "fillOpacity": 1},
        ).add_to(world_map)

        return world_map


    def health_dashboard_map_final(self, **kwargs):
        context = super().get_context_data(**kwargs)
        health_stats_data = WorldHealthStatistics.objects.all()
        stats_df = pd.DataFrame(list(health_stats_data.values()))
        geojson = gpd.read_file(r"./static/countries.geo.json")
        geojson = geojson[["id", "geometry"]]  # shape= 180, 2
        # print(type(geojson))
        geojson.head()
        geo_df = geojson.merge(stats_df, left_on="id", right_on="country", how="outer")
        # Merge Issues: https://stackoverflow.com/questions/60271854/valueerror-cannot-render-objects-with-any-missing-geometries-when-using-a-geopa
        print(type(geo_df))
        geo_df.isna().sum()
        geo_df = geo_df[~geo_df["geometry"].isna()]
        geo_df = geo_df[~geo_df["country"].isna()]
        print(geo_df.shape)
        geo_df.isna().sum()

        col_name = "deaths_per_1lac_diabetes"
        map_name = "Deaths Per 1lac Diabetes Cases"
        legend_name = "Deaths Per 1lac Diabetes Cases"
        world_map = self.create_map(map_name, legend_name, geo_df, col_name, "Female")


        # # Later: Switching between different columns
        # # Based on radio button selected, send correct map by calling create_map()
        # if request.button[0] == "deaths_per_1lac_diabetes":
        #     if request.button[1] == "Female":
        #         sex = "Female"
        #     elif request.button[1] == "Male":
        #         sex = "Male"
        #     elif request.button[1] == "All":
        #         sex = None
        #     else:
        #         sex = "Other"
        #     col_name = "deaths_per_1lac_diabetes"
        #     map_name = "Deaths Per 1lac Diabetes Cases"
        #     legend_name = "Deaths Per 1lac Diabetes Cases"
        #     world_map = self.create_map(map_name, legend_name, geo_df, col_name, sex)
        # elif request.button[0] == "deaths_per_1lac_diabetes":
        #     pass
        # else:
        #     # throw an error
        #     pass

        # return render(request, 'dashboard.html' , {'health_stats_map': world_map})
        context['health_stats_map2'] = world_map
        return context
    

# class FoliumView(TemplateView, BaseContextMixin):
#     template_name = "dashboard.html"
    
#     def get_context_data(self, **kwargs):
#         figure = folium.Figure()
#         m = folium.Map(
#             location=[45.372, -121.6972],
#             zoom_start=12,
#             tiles='Stamen Terrain'
#         )
#         m.add_to(figure)

#         folium.Marker(
#             location=[45.3288, -121.6625],
#             popup='Mt. Hood Meadows',
#             icon=folium.Icon(icon='cloud')
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3311, -121.7113],
#             popup='Timberline Lodge',
#             icon=folium.Icon(color='green')
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3300, -121.6823],
#             popup='Some Other Location',
#             icon=folium.Icon(color='red', icon='info-sign')
#         ).add_to(m)
#         figure.render()

#         context_data = super(FoliumView, self).get_context_data(**kwargs)
#         context_data["figure"] = figure
#         return context_data