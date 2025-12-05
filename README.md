![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-yellow)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2025-orange)
![Repo Size](https://img.shields.io/github/repo-size/aggarwalharshit21/NSE-Securities-Categorization)

---

# 📊 NSE Securities Categorization  
### **A Data Analyst Assignment for Listing Category Classification**

This project automates the classification of NSE-listed securities into **5x**, **3x**, or **Only Delivery** categories by integrating and processing multiple raw market data sources, including:

- BhavCopy traded-value files  
- Security master file (`security.txt`)  
- VAR (Value at Risk) reports  
- F&O underlying list  

The final categorized output is stored in:

output/securities_categorized.csv

yaml
Copy code

---

# 🚀 Why This Project Matters

Accurate classification helps:

- Reduce market risk  
- Improve margin estimation  
- Support compliance decisions  
- Assist risk management teams  
- Enable better investment and trading controls  

This project reflects practical **data cleaning**, **file parsing**, **aggregation**, and **rule-based classification** — essential skills for Data Analysts and Financial Engineers.

---

# ⭐ Features

- Parses raw & inconsistent NSE file formats  
- Extracts symbol-level insights cleanly  
- Computes price band % dynamically  
- Aggregates multi-day Bhav Copy traded values  
- Integrates VAR-based F&O logic  
- Produces a clean category label per security  
- Complete Python processing pipeline (`main.py`)  

---

# 🛠 Technologies Used

| Technology | Purpose |
|-----------|----------|
| **Python 3.12** | Core programming |
| **Pandas** | Data manipulation & merging |
| **NumPy** | Numeric operations |
| **File Parsing** | Handling large TXT, DAT, CSV files |
| **GitHub** | Version control & submission |

---

# 📁 Project Structure

NSE-Securities-Categorization/
│
├── data/
│ ├── security.txt
│ ├── BhavCopy_NSE_CM (1).csv
│ ├── BhavCopy_NSE_CM (2).csv
│ ├── BhavCopy_NSE_CM (3).csv
│ ├── C_VAR1_06112025_6.DAT
│ ├── FNO_Underlyings.csv
│
├── src/
│ └── main.py
│
├── output/
│ └── securities_categorized.csv
│
└── README.md

yaml
Copy code

---

# 🚀 How to Run

### 1️⃣ Install dependencies  
pip install pandas numpy

shell
Copy code

### 2️⃣ Run the processing script  
python src/main.py

makefile
Copy code

or:

py src/main.py

yaml
Copy code

---

# 🧠 Categorization Rules

### **5x Category**
- SERIES ∈ {EQ, BE, BZ}  
- Avg traded value > ₹50,00,000  
- Price band % > 5  
**OR**  
- VAR ≤ 20 and stock is in F&O list  

---

### **3x Category**
- SERIES ∈ {EQ, BE, BZ}  
- Avg traded value > ₹20,00,000  
- Price band % > 5  
**OR**  
- VAR ≤ 33.33 and stock is NOT eligible for 5x  

---

### **Only Delivery**
Default category for all other cases.

---

# 📤 Output Columns

- SYMBOL  
- SERIES  
- PRICE_RANGE  
- PRICE_BAND  
- TRADED_VALUE  
- VAR  
- is_fno  
- category  

---

# 📌 Sample Output Preview

`output/securities_categorized.csv` contains final category assignment for each NSE symbol.

---

# 👨‍💻 Developed By  
### **Harshit Aggarwal**  
Data Analyst & Software Engineer  
📧 Email: *ha2884730@gmail.com*  
🔗 GitHub: **https://github.com/aggarwalharshit21**

---

# 📄 License  
This project is released under the **MIT License**.

---

# ⭐ Feedback  
If you found this helpful or have suggestions, feel free to open an issue or contribute!

---
