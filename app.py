import pandas as pd
import PyPDF2
import streamlit as st
st.title("🔍 Easy Keyword Matcher")
st.write("Upload your files below to search for keywords.")
# Simple Uploaders
keyword_file = st.file_uploader("1. Upload Keyword List (.txt)", type=["txt"])
doc_file = st.file_uploader("2. Upload Document (.txt or .pdf)", type=["txt", "pdf"])
if keyword_file and doc_file:
 # Load the words
 keywords_raw = keyword_file.getvalue().decode("utf-8")
 keywords = [k.strip() for k in keywords_raw.splitlines() if k.strip()]
 # Load the main text document
 if doc_file.type == "text/plain":
   document_text = doc_file.getvalue().decode("utf-8")
 else:
   # Process PDF safely
   reader = PyPDF2.PdfReader(doc_file)
   document_text = "".join([page.extract_text() or "" for page in reader.pages])
 document_text_lower = document_text.lower()
 # Check matches
 results = []
 for kw in keywords:
   count = document_text_lower.count(kw.lower())
   if count > 0:
     results.append({"Keyword": kw, "Matches Found": count})
 # Show results
 st.write("### 📊 Search Results")
 if results:
   df = pd.DataFrame(results)
   st.dataframe(df)
   # Download results button
   csv = df.to_csv(index=False).encode("utf-8")
   st.download_button(
       "📥 Download Results as CSV", csv, "matches.csv", "text/csv"
   )
 else:
   st.write("❌ No matching keywords found.")
