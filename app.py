# python3 -m streamlit run app.py
#   Network URL: http://10.223.134.207:8501
#   External URL: http://34.213.214.55:8501

import streamlit as st
import psutil
import matplotlib.pyplot as plt
import platform
import pandas as pd

# Retrieve the OS name
os_name = platform.system()  # Basic OS type (e.g., 'Linux', 'Windows', 'Darwin')
os_release = platform.release()  # OS release version
os_version = platform.version()  # OS version
# More detailed OS information
detailed_os_name = platform.platform()  # Detailed OS info (e.g., 'Linux-5.4.0-42-generic-x86_64-with-Ubuntu-20.04-focal')
# Printing results
# print(f"Basic OS Name: {os_name}")
# print(f"OS Release: {os_release}")
# print(f"OS Version: {os_version}")
# print(f"Detailed OS Information: {detailed_os_name}")


# Set the page configuration
st.set_page_config(page_title=f"System Monitor", layout="wide")


# Title of the app
st.title("System Monitor")
st.write(f"Basic OS Name: " + "' %s '"%(os_name))
st.write(f"OS Release: ' {os_release} '")
st.write(f"OS Version: ' {os_version}' ")
st.write(f"Detailed OS Information: ' {detailed_os_name} ' ")

# Create columns for better layout
col1, col2, col3 = st.columns(3)

# CPU Usage
with col1:
    st.header("CPU Usage")
    cpu_usage = psutil.cpu_percent(interval=1)
    st.metric(label="CPU Usage (%)", value=cpu_usage)

    # Plotting CPU usage pie chart
    fig, ax = plt.subplots()
    ax.pie([cpu_usage, 100 - cpu_usage], labels=["Used", "Free"], autopct='%1.1f%%', colors=['#FF6F61', '#6BCB77'])
    ax.set_title("CPU Usage Distribution")
    st.pyplot(fig)

# Memory Usage
with col2:
    st.header("Memory Usage")
    memory = psutil.virtual_memory()
    st.metric(label="Memory Usage (%)", value=memory.percent)

    # Plotting Memory usage pie chart
    fig, ax = plt.subplots()
    ax.pie([memory.percent, 100 - memory.percent], labels=["Used", "Free"], autopct='%1.1f%%',
           colors=['#FFD700', '#6495ED'])
    ax.set_title("Memory Usage Distribution")
    st.pyplot(fig)

# Disk Usage
with col3:
    st.header("Disk Usage")
    disk = psutil.disk_usage('/')
    st.metric(label="Disk Usage (%)", value=disk.percent)

    # Plotting Disk usage pie chart
    fig, ax = plt.subplots()
    ax.pie([disk.percent, 100 - disk.percent], labels=["Used", "Free"], autopct='%1.1f%%',
           colors=['#FF6347', '#87CEEB'])
    ax.set_title("Disk Usage Distribution")
    st.pyplot(fig)

# Display system details
st.subheader("Detailed System Information")
st.write(f"CPU Cores: {psutil.cpu_count(logical=True)}")
st.write(f"Total Memory: {memory.total // (1024 ** 3)} GB")
st.write(f"Available Memory: {memory.available // (1024 ** 3)} GB")
st.write(f"Total Disk Space: {disk.total // (1024 ** 3)} GB")
st.write(f"Free Disk Space: {disk.free // (1024 ** 3)} GB")



# Display top processes by CPU and memory usage
st.subheader("Top Processes")

# Retrieve processes sorted by CPU usage
def get_top_processes(num=5):
    # Fetch all processes info
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    # Convert to DataFrame for sorting and display
    df = pd.DataFrame(processes)
    df.sort_values(by='cpu_percent', ascending=False, inplace=True)
    return df.head(num)

# Show top 5 processes by CPU usage
top_processes = get_top_processes(10)
st.write("### Top Processes by CPU Usage")
st.dataframe(top_processes[['pid', 'name', 'cpu_percent', 'memory_percent']])