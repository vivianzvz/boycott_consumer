from otree.api import *
import csv
from pathlib import Path

class C(BaseConstants):
    NAME_IN_URL = 'block1_effort_wage'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        # Load math questions from CSV
        csv_path = Path(__file__).parent / 'math_questions.csv'
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            question_pairs = [(int(row['num1']), int(row['num2']), int(row['answer'])) for row in reader]

        for p in self.get_players():
            if p.role() == 'worker':
                p.participant.vars['math_questions'] = question_pairs

class Group(BaseGroup):
    final_wage = models.CurrencyField(label="Final wage", min=0)
    correct_sums = models.IntegerField(initial=0)

class Player(BasePlayer):
    offered_wage = models.CurrencyField(label="Offered wage", min=0)
    message = models.LongStringField(blank=True, label="Optional message to worker")
    fairness_rating = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label="How fair was your employer's behavior?",
        widget=widgets.RadioSelect,
        blank=True,
    )

    # 30 answer fields
    answer_1 = models.IntegerField(label="Answer",blank=True)
    answer_2 = models.IntegerField(label="Answer",blank=True)
    answer_3 = models.IntegerField(label="Answer",blank=True)
    answer_4 = models.IntegerField(label="Answer",blank=True)
    answer_5 = models.IntegerField(label="Answer",blank=True)
    answer_6 = models.IntegerField(label="Answer",blank=True)
    answer_7 = models.IntegerField(label="Answer",blank=True)
    answer_8 = models.IntegerField(label="Answer",blank=True)
    answer_9 = models.IntegerField(label="Answer",blank=True)
    answer_10 = models.IntegerField(label="Answer",blank=True)
    answer_11 = models.IntegerField(label="Answer",blank=True)
    answer_12 = models.IntegerField(label="Answer",blank=True)
    answer_13 = models.IntegerField(label="Answer",blank=True)
    answer_14 = models.IntegerField(label="Answer",blank=True)
    answer_15 = models.IntegerField(label="Answer",blank=True)
    answer_16 = models.IntegerField(label="Answer",blank=True)
    answer_17 = models.IntegerField(label="Answer",blank=True)
    answer_18 = models.IntegerField(label="Answer",blank=True)
    answer_19 = models.IntegerField(label="Answer",blank=True)
    answer_20 = models.IntegerField(label="Answer",blank=True)
    answer_21 = models.IntegerField(label="Answer",blank=True)
    answer_22 = models.IntegerField(label="Answer",blank=True)
    answer_23 = models.IntegerField(label="Answer",blank=True)
    answer_24 = models.IntegerField(label="Answer",blank=True)
    answer_25 = models.IntegerField(label="Answer",blank=True)
    answer_26 = models.IntegerField(label="Answer",blank=True)
    answer_27 = models.IntegerField(label="Answer",blank=True)
    answer_28 = models.IntegerField(label="Answer",blank=True)
    answer_29 = models.IntegerField(label="Answer",blank=True)
    answer_30 = models.IntegerField(label="Answer",blank=True)

    def role(self):
        return 'employer' if self.id_in_group == 1 else 'worker'
