import streamlit as st
from streamlit_elements import elements, mui, dashboard

# Define the layout for your dashboard items
layout = [
    # dashboard.Item parameters: key, x, y, width, height, isDraggable, isResizable
    dashboard.Item("item1", 0, 0, 1, 1, isDraggable=True, isResizable=True),
    dashboard.Item("item2", 1, 0, 2, 1, isDraggable=True, isResizable=True),
]

# Create the dashboard
with elements("dashboard"):
    with dashboard.Grid(layout):
        mui.Paper("Drag me!", key="item1", sx={"padding": "5px"})
        mui.Paper("Resize me!", key="item2", sx={"padding": "5px"})