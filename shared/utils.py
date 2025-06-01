# shared/utils.py

def classify_employers(players):
    """
    Returns the lowest and highest paying employers among those whose workers exerted effort.
    """
    employers_with_effort = [
        (p, p.group.correct_sums, p.group.final_wage)
        for p in players
        if p.role == 'employer' and p.group.correct_sums > 0
    ]
    if not employers_with_effort:
        return None, None
    sorted_by_wage = sorted(employers_with_effort, key=lambda x: x[2])
    unfair_employer = sorted_by_wage[0][0]
    fair_employer = sorted_by_wage[-1][0]
    return unfair_employer, fair_employer
