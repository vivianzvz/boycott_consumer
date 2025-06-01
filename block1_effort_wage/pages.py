from otree.api import *
from .models import C, Subsession, Group, Player


class GeneralIntro(Page):
    def is_displayed(self):
        return self.round_number == 1


class Block1Intro(Page):
    def is_displayed(self):
        return self.round_number == 1


class EmployerOfferMessage(Page):
    form_model = 'player'
    form_fields = ['offered_wage', 'message']

    def is_displayed(self):
        return self.player.role() == 'employer'


class WaitForOffer(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.player.role() == 'worker'

    def after_all_players_arrive(self):
        pass  # nothing needed here

class WorkerTask(Page):
    form_model = 'player'
    form_fields = [f'answer_{i}' for i in range(1, 31)]

    def is_displayed(self):
        return self.player.role() == 'worker'

    def vars_for_template(self):
        problems = self.participant.vars.get('math_questions', [])
        field_names = self.form_fields  # directly use the page's form_fields
        labeled_pairs = list(zip(field_names, problems))

        employer = self.group.get_player_by_role('employer')
        return {
            'labeled_pairs': labeled_pairs,
            'employer_message': employer.message,
        }



    def before_next_page(self):
        correct = 0
        problems = self.participant.vars.get('math_questions', [])
        for i, (_, _, correct_answer) in enumerate(problems):
            field_name = f'answer_{i+1}'
            user_answer = self.player.field_maybe_none(field_name)
            if user_answer == correct_answer:
                correct += 1
        self.group.correct_sums = correct



class WaitForWorkerTasks(WaitPage):
    wait_for_all_groups = False

    def is_displayed(self):
        return self.round_number == 1  # or some logic to control scope



class EmployerDecision(Page):
    form_model = 'group'
    form_fields = ['final_wage']

    def is_displayed(self):
        return self.player.role() == 'employer'

    def vars_for_template(self):
        return {
            'correct_sums': self.group.correct_sums
        }



class WaitForWageDecision(WaitPage):
    wait_for_all_groups = False

    def is_displayed(self):
        return self.player.role() == 'worker'

    def after_all_players_arrive(self):
        pass

class Results(Page):
    def vars_for_template(self):
        employer = self.group.get_player_by_role('employer')
        return {
            'offer': employer.field_maybe_none('offered_wage'),
            'final': self.group.final_wage,
            'message': employer.field_maybe_none('message'),
            'sums': self.group.correct_sums,
            'employer_payoff': self.group.correct_sums - self.group.final_wage,
            'worker_payoff': self.group.final_wage,
        }

    def before_next_page(self):
        # Store Block 1 payoff into participant.vars for use in later apps
        if self.player.role() == 'worker':
            self.participant.vars['block1_payoff'] = self.group.final_wage
        else:  # employer
            self.participant.vars['block1_payoff'] = self.group.correct_sums - self.group.final_wage



class WorkerFairnessRating(Page):
    form_model = 'player'
    form_fields = ['fairness_rating']

    def is_displayed(self):
        return self.player.role() == 'worker'




page_sequence = [
    GeneralIntro,
    Block1Intro,
    EmployerOfferMessage,
    WaitForOffer,
    WorkerTask,
    WaitForWorkerTasks,
    EmployerDecision,
    WaitForWageDecision,
    Results,
    WorkerFairnessRating,
]
