# Boycott Consumer Game (oTree)

This repository contains the oTree implementation of the Consumer Decision Market Game, created for ECON 165 at UC Santa Cruz. The project idea originated from Luke Catalano, Sadhika Agrawal and Derek Zhao.

## 🧠 Purpose
The experiment explores fairness and market behavior through two blocks:

- **Block 1** is a simple employer-worker task:
  - Employers offer wages and workers solve math problems.
  - Workers rate the perceived fairness afterward.

- **Block 2** is a consumer market:
  - Buyers choose between two sellers with known fairness reputations (based on Block 1).
  - Treatments manipulate exposure to fairness info and boycott coordination.

## 🧪 Experimental Structure
- Each session consists of 2 blocks and multiple rounds.
- Participants switch roles between blocks.
- Treatments include:
  - **T0**: baseline
  - **T1**: fairness reminder
  - **T2**: fairness + boycott poll

## 📁 Repo Contents
- `block1_market/` and `block2_market/` — two oTree apps
  - `models.py` — defines players, groups, payoff logic
  - `pages.py` — defines page flow and logic
  - `templates/` — HTML templates
- `settings.py` — session configuration and treatment control
- `requirements.txt` — dependencies
- `Procfile` — for Heroku deployment

---

## 🧩 How It Works

### Block 1: Employer-Worker Game
1. Employers offer wages and send messages.
2. Workers solve math problems.
3. Employers pay a final wage based on effort.
4. Workers rate fairness.

### Block 2: Market Game
1. Buyers choose between two sellers (A, B).
2. Sellers differ by their past behavior in Block 1.
3. Treatments affect visibility and support for a boycott.

---

## 🔧 Customization

You can configure key settings in `settings.py`:
- `real_world_currency_per_point`
- `num_demo_participants`
- treatment order logic is embedded in `creating_session()` of `block2_market/models.py`
- Effort task content (i.e., math questions) can be modified in `block1_effort_wage/math_questions.csv`
  - Each row in the CSV corresponds to an addition problem (`num1 + num2 = result`) used in the worker's task during Block 1.

---

## ▶️ Running the Game Locally

### 1. Clone the repository
```bash
git clone https://github.com/vivianzvz/boycott_consumer.git
cd boycott_consumer
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the oTree dev server
```bash
otree devserver
```
