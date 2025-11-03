# TCP Calculator Chat

This project demonstrates a simple **TCP communication** between a **Client** and a **Server** in Python.  
It simulates the **TCP 3-way handshake** and performs basic arithmetic operations (addition, subtraction, multiplication, division).

---

## 📌 Features
- TCP Handshake (SYN → SYN-ACK → ACK).
- Client sends an operation type and two numbers.
- Server performs the calculation and returns the result.
- Voice feedback using **pyttsx3**.
- Colored terminal output using **colorama**.
- Type `exit` to quit safely.

---

## 🛠 Requirements

Install the required dependencies:
  ```bash
  pip install pyttsx3 colorama
  ```
## 🔍 How to Run

### 1- Start the server:
```bash
python Server.py
```

### 2- Start the client:
```bash
python Client.py
```

### 3- Follow the prompts:

💠 Choose the operation: addition, subtraction, multiplication, or division.

💠 Enter the first number.

💠 Enter the second number.

💠 Get the result from the server.

💠 Type exit at any number prompt to disconnect safely.

---

## 🪪 License

This project is licensed under the MIT License – you’re free to use, modify, and share it.

---

## 👩‍💻 Author

Benkaba Marwa
