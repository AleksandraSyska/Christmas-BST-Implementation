# 🎄 Christmas Tree BST (Binary Search Tree)

## 📌 Project Overview
This project is a specialized implementation of a **Binary Search Tree (BST)**, where the structure is modeled as a "Christmas Tree". It was developed as part of the *Algorithms and Data Structures* course at the **Warsaw University of Technology** (Faculty of Mathematics and Information Science).

In this implementation, tree nodes represent Christmas ornaments. The type, color, and properties of each ornament are determined by the mathematical properties of its numerical key.

## 🖥️ Standalone Application (.exe)
For ease of use, a compiled **executable file (.exe)** is included in this repository. This allows Windows users to run the *Christmas Tree Management System* directly without needing a Python environment. The app features an interactive menu to build trees, run tests, and visualize the tree structure.

## 🧮 Mathematical Ornament Logic
The classification of ornaments is based on the key $k$ of each node:
* **Bauble:** Key is an odd number ($k \pmod 2 \neq 0$).
* **Light:** Key is an even number ($k \pmod 2 = 0$).
    * 🟡 **Yellow Light:** Key is divisible by 4 ($k \pmod 4 = 0$).
    * 🔴 **Red Light:** Key is even but not divisible by 4.

## 🚀 Key Features
Beyond standard BST operations (Insert, Delete, Search), the project includes advanced recursive algorithms using **DFS (Depth-First Search)**:

* **Stability Analysis:** Checks if the difference in the number of descendants between left and right subtrees is $\le 2$ for every node.
* **Illumination Check:** Verifies that every internal node has at least one light in its subtrees.
* **Aesthetic Evaluation:**
    * `is_stylish`: Ensures no **Bauble** is placed above a **Red Light**.
    * `is_elegant`: True if the number of **Colorful Paths** (lights only) is greater than or equal to the number of **Monochromatic Paths**.
    * `is_traditional`: Verifies if there is a "Golden Path" with a perfect 1:1 balance of yellow and red lights.
* **Visualization:** Provides a textual view of the tree structure (rotated 90 degrees) for easy structural analysis.

## 🛠️ Technical Details
* **Language:** Python 3.x.
* **Optimization:** Used `__slots__` in `Node` and `ChristmasTree` classes for memory efficiency.
* **Testing:** Includes a built-in automated test module that generates reports for 8 different analytical scenarios.

## 👤 Authors
* **Zuzanna Okońska** – path logic, and property counting methods.
* **Aleksandra Syska** – Class architecture, core BST operations (insert/delete), and automated test module.

---
*Project completed: December 2025*
