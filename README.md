# 🧠 CPU Scheduling with Deadlock Detection & Recovery

## 📌 Description
This project simulates a CPU scheduling system combined with deadlock detection and recovery mechanisms.

The system manages multiple processes with:
- CPU bursts
- I/O bursts
- Resource requests and releases

It uses:
- Priority Scheduling
- Round Robin (Time Quantum)

---

## ⚙️ Features
- Priority-based scheduling
- Round Robin execution
- CPU & I/O burst handling
- Resource allocation (Request / Release)
- Deadlock detection using resource allocation graph
- Deadlock recovery (process termination)
- Gantt chart generation
- Waiting time & turnaround time calculation

---

## 📥 Input Example
0 0 2 CPU{R[1], 5,R[1]} IO{3} CPU{3}
1 3 1 CPU[R[1],3, F[1],4]
2 6 2 CPU{4} IO{2} CPU{2}


---

## 🚀 How to Run
python main.py

---


## 📊 Output
Gantt Chart
Waiting Time
Turnaround Time
Deadlock detection messages


---



## ⚠️ Deadlock Handling
Deadlock is detected when processes form a circular dependency
The system resolves it by terminating one process and freeing resources


---

## 🖥️ Environment
OS: Linux (Virtual Machine)
Language: Python

---

## 📁 Project Structure
CPU-Scheduling-Deadlock/
=> main.py
=> input.txt
=> report.pdf
=> README.md
