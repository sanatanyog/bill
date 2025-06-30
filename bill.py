#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import numpy as np
from scipy.stats import norm

st.title("How Much Must We Verify to Trust a Bill?")
st.markdown("""
This tool helps you decide how many records (e.g., calls on your bill) you need to check to be statistically confident that your bill is correct, based on the principles discussed in [this article](https://www.linkedin.com/pulse/how-much-must-we-verify-trust-bill-dr-partha-majumdar-gtktf).
""")

# User Inputs
N = st.number_input("Total number of records on your bill (e.g., number of calls)", min_value=1, value=300)
confidence = st.selectbox("Confidence level", [90, 95, 99], index=1)
margin_error = st.slider("Margin of error (%)", min_value=1, max_value=10, value=5)

# Statistical Calculations
Z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
Z = Z_scores[confidence]
p = 0.5  # Most conservative estimate
E = margin_error / 100

# Infinite population sample size
n_0 = (Z**2 * p * (1 - p)) / (E**2)

# Finite population correction
n = n_0 / (1 + (n_0 - 1) / N)
n = int(np.ceil(n))

st.subheader("Results")
st.write(f"To be **{confidence}% confident** that your bill is accurate within ±{margin_error}% margin of error, you need to check at least **{n} out of {N} records**.")

st.markdown("""
- Checking more than this number yields diminishing returns.
- This approach is widely used in quality control, polling, and auditing.
""")

# Optional: Visualization
import matplotlib.pyplot as plt

sample_sizes = []
for Ni in range(1, N+1):
    ni = n_0 / (1 + (n_0 - 1) / Ni)
    sample_sizes.append(ni)

st.subheader("Sample Size vs. Bill Size")
fig, ax = plt.subplots()
ax.plot(range(1, N+1), sample_sizes)
ax.set_xlabel("Total Records on Bill")
ax.set_ylabel("Sample Size Needed")
st.pyplot(fig)


# In[ ]:




