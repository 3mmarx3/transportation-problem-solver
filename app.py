import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import networkx as nx
import matplotlib.pyplot as plt



st.set_page_config(page_title="Transportation Problem Solver", layout="wide")

st.title("Transportation Problem Solver")
st.markdown("Enter the problem data (Sources, Destinations, Costs, Supply, and Demand) below. The application will calculate the allocations and visualize the final network.")



col1, col2 = st.columns(2)
with col1:
    num_sources = st.number_input("Number of Sources", min_value=2, max_value=10, value=3)
with col2:
    num_destinations = st.number_input("Number of Destinations", min_value=2, max_value=10, value=4)



st.subheader("Data Input")

source_names = [f"Source {i+1}" for i in range(num_sources)]
dest_names = [f"Dest {i+1}" for i in range(num_destinations)]

default_costs = pd.DataFrame(np.zeros((num_sources, num_destinations)), columns=dest_names, index=source_names)
default_supply = pd.DataFrame(np.zeros((num_sources, 1)), columns=["Supply"], index=source_names)
default_demand = pd.DataFrame(np.zeros((1, num_destinations)), columns=dest_names, index=["Demand"])

col_cost, col_sup_dem = st.columns([2, 1])

with col_cost:
    st.write("**Cost Matrix**")
    edited_costs = st.data_editor(default_costs, width="stretch")

with col_sup_dem:
    st.write("**Supply**")
    edited_supply = st.data_editor(default_supply, width="stretch")
    st.write("**Demand**")
    edited_demand = st.data_editor(default_demand, width="stretch")



def least_cost_method(costs, sup, dem):
    c, s, d = costs.copy(), sup.copy(), dem.copy()
    allocation = np.zeros_like(c)
    while np.sum(s) > 0 and np.sum(d) > 0:
        min_val = np.min(c)
        i, j = np.argwhere(c == min_val)[0]
        qty = min(s[i], d[j])
        allocation[i, j] += qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: c[i, :] = np.inf
        if d[j] == 0: c[:, j] = np.inf
    return allocation

def vogel_approximation_method(costs, sup, dem):
    c, s, d = costs.copy(), sup.copy(), dem.copy()
    allocation = np.zeros_like(c)
    while np.sum(s) > 0 and np.sum(d) > 0:
        row_penalties, col_penalties = [], []
        for i in range(c.shape[0]):
            valid_costs = np.sort(c[i, np.isfinite(c[i])])
            row_penalties.append(valid_costs[1] - valid_costs[0] if len(valid_costs) >= 2 else (valid_costs[0] if len(valid_costs) == 1 else -1))
        for j in range(c.shape[1]):
            valid_costs = np.sort(c[:, j][np.isfinite(c[:, j])])
            col_penalties.append(valid_costs[1] - valid_costs[0] if len(valid_costs) >= 2 else (valid_costs[0] if len(valid_costs) == 1 else -1))
        
        max_row_p = max(row_penalties) if row_penalties else -1
        max_col_p = max(col_penalties) if col_penalties else -1
        
        if max_row_p >= max_col_p:
            i = row_penalties.index(max_row_p)
            j = np.argmin(c[i])
        else:
            j = col_penalties.index(max_col_p)
            i = np.argmin(c[:, j])
            
        qty = min(s[i], d[j])
        allocation[i, j] += qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: c[i, :] = np.inf
        if d[j] == 0: c[:, j] = np.inf
    return allocation

def get_optimal_solution(costs, sup, dem):
    c_flat = costs.flatten()
    A_eq, b_eq = [], []
    for i in range(len(sup)):
        constraint = np.zeros_like(costs)
        constraint[i, :] = 1
        A_eq.append(constraint.flatten())
        b_eq.append(sup[i])
    for j in range(len(dem)):
        constraint = np.zeros_like(costs)
        constraint[:, j] = 1
        A_eq.append(constraint.flatten())
        b_eq.append(dem[j])
        
    res = linprog(c_flat, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    if res.success:
        return res.x.reshape(costs.shape), res.fun
    return None, None

def plot_network_graph(allocation_matrix, sources, destinations):
    G = nx.DiGraph()
    
    G.add_nodes_from(sources, bipartite=0)
    G.add_nodes_from(destinations, bipartite=1)
    
    for i, src in enumerate(sources):
        for j, dest in enumerate(destinations):
            if allocation_matrix[i, j] > 0:
                G.add_edge(src, dest, weight=int(allocation_matrix[i, j]))
                
    pos = nx.bipartite_layout(G, sources)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#89CFF0', node_size=2500, edgecolors='black')
    
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
    
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=20, edge_color='gray', width=1.5)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_color='red', font_weight='bold')
    
    plt.title("Transportation Network Graph", fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    
    return fig


if st.button("Solve Problem", type="primary"):
    cost_matrix = edited_costs.values
    supply_arr = edited_supply["Supply"].values
    demand_arr = edited_demand.values.flatten()
    
    total_supply = np.sum(supply_arr)
    total_demand = np.sum(demand_arr)
    
    st.divider()
    
    st.subheader("Balance Check")
    st.write(f"**Total Supply:** {total_supply} | **Total Demand:** {total_demand}")
    
    if total_supply != total_demand:
        st.error("The problem is UNBALANCED! Supply does not equal Demand. Please adjust the values.")
    elif total_supply == 0 or total_demand == 0:
        st.warning("Please enter valid Supply and Demand numbers greater than zero before solving.")
    else:
        st.success("The problem is BALANCED.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Least Cost Method (LCM)", "Vogel's Method (VAM)", "Optimal Solution (SciPy)", "Network Visualization"])
        
        with tab1:
            lcm_alloc = least_cost_method(cost_matrix, supply_arr, demand_arr)
            lcm_cost = np.sum(lcm_alloc * cost_matrix)
            st.dataframe(pd.DataFrame(lcm_alloc, columns=dest_names, index=source_names))
            st.info(f"Total LCM Cost: **{lcm_cost}**")
            
        with tab2:
            vam_alloc = vogel_approximation_method(cost_matrix, supply_arr, demand_arr)
            vam_cost = np.sum(vam_alloc * cost_matrix)
            st.dataframe(pd.DataFrame(vam_alloc, columns=dest_names, index=source_names))
            st.info(f"Total VAM Cost: **{vam_cost}**")
            
        with tab3:
            opt_alloc, opt_cost = get_optimal_solution(cost_matrix, supply_arr, demand_arr)
            if opt_alloc is not None:
                st.dataframe(pd.DataFrame(opt_alloc, columns=dest_names, index=source_names))
                st.success(f"Absolute Optimal Cost: **{opt_cost}**")
            else:
                st.error("An error occurred while calculating the optimal solution.")
                
        with tab4:
            st.write("Visual representation of the Optimal Solution transport routes:")
            if opt_alloc is not None:
                fig = plot_network_graph(opt_alloc, source_names, dest_names)
                st.pyplot(fig)
            else:
                st.warning("No optimal allocation found to draw the graph.")
