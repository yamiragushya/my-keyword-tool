import pandas as pd
2
import PyPDF2
3
import streamlit as st
4
 
5
st.title("🔍 Cybersecurity Requirements: KEYWORDS - Tool by Yamini")
6
st.write("Upload your files below to search for keywords.")
7
 
8
# Uploaders
9
keyword_file = st.file_uploader(
10
"1. Upload Keyword List (.txt, .xls, .xlsx)",
11
type=["txt", "xls", "xlsx"]
12
)
13
 
14
doc_file = st.file_uploader(
15
"2. Upload Document (.txt or .pdf)",
16
type=["txt", "pdf"]
17
)
18
 
19
if keyword_file and doc_file:
20
 
21
# Load keywords
22
if keyword_file.name.endswith(".txt"):
23
keywords_raw = keyword_file.getvalue().decode("utf-8")
24
keywords = [k.strip() for k in keywords_raw.splitlines() if k.strip()]
25
 
26
elif keyword_file.name.endswith((".xls", ".xlsx")):
27
df_keywords = pd.read_excel(keyword_file)
28
 
29
# Take values from first column
30
keywords = (
31
df_keywords.iloc[:, 0]
32
.dropna()
33
.astype(str)
34
.str.strip()
35
.tolist()
36
)
37
 
38
# Load document
39
if doc_file.type == "text/plain":
40
document_text = doc_file.getvalue().decode("utf-8")
41
else:
42
reader = PyPDF2.PdfReader(doc_file)
43
document_text = "".join(
44
page.extract_text() or "" for page in reader.pages
45
)
46
 
47
document_text_lower = document_text.lower()
48
 
49
# Search keywords
50
results = []
51
 
52
for kw in keywords:
53
count = document_text_lower.count(kw.lower())
54
if count > 0:
55
results.append({
56
"Keyword": kw,
57
"Matches Found": count
58
})
59
 
60
# Display results
61
st.write("### 📊 Search Results")
62
 
63
if results:
64
result_df = pd.DataFrame(results)
65
st.dataframe(result_df)
66
 
67
csv = result_df.to_csv(index=False).encode("utf-8")
68
 
69
st.download_button(
70
"📥 Download Results as CSV",
71
csv,
72
"matches.csv",
73
"text/csv"
74
)
75
else:
76
st.write("❌ No matching keywords found.")
