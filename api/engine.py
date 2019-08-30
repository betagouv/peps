from data.models import Problem
from data.models import Weed, Pest
from data.models import Practice, Culture
from api.utils import AlpacaUtils
from api.models import ResponseItem


class Engine:

    form = None
    blacklisted_practices = []
    blacklisted_types = []

    def __init__(self, answers, blacklisted_practices, blacklisted_types):
        self.form = AlpacaUtils(answers)
        self.blacklisted_practices = blacklisted_practices
        self.blacklisted_types = blacklisted_types


    def calculate_results(self):
        """
        Returns an array of Response objects ordered by weight.
        """
        practices = Practice.objects.all()
        results = []

        for practice in practices:
            weight = self._calculate_weight(practice)
            results.append(ResponseItem(practice, weight))

        def _take_weight(elem):
            return elem.weight

        return sorted(results, key=_take_weight, reverse=True)

    def get_suggestions(self, results):
        """
        Given an array of Response objets it will return the suggestions
        to present to the user. It takes into consideration the difficulty
        of the practice and their score.
        """
        number_of_suggestions = 3
        minimum_weight = 0.5

        # We will only suggest practices above the minimum weight that have information on their difficulty.
        eligible_results = list(filter(lambda x: x.weight >= minimum_weight and x.practice.difficulty, results))
        eligible_results.sort(key=lambda x: x.practice.difficulty, reverse=True)

        # If we have less eligible results than number of suggestions needed, we just
        # return them
        if len(eligible_results) <= number_of_suggestions:
            return eligible_results

        # We will divide the list of difficulty-ordered items in chunks, and will
        # add the element of the highest weight of each chunk, as long as its practice
        # groups haven't been used before.
        chunk_size = len(eligible_results) // number_of_suggestions

        # We need to create the chunks in which we will take practices.
        chunks = [eligible_results[x:x + chunk_size] for x in range(0, len(eligible_results), chunk_size)]
        if len(chunks) > number_of_suggestions:
            chunks[number_of_suggestions - 1] += chunks[number_of_suggestions]
            chunks = chunks[:number_of_suggestions]

        # Now we will find the best practices accross the board and
        # add them if no other practice with the same family has been
        # already added
        suggestions = [None for x in range(number_of_suggestions)]

        for _ in range(number_of_suggestions):
            max_values = list(map(lambda x: max(x, key=lambda y: y.weight) if x else None, chunks))
            candidate = max(list(filter(lambda x: x is not None, max_values)), key=lambda x: x.weight)
            index = max_values.index(candidate)

            # Remove all practices from that chunk because we
            # already have a suggestion from there
            chunks[index] = []

            # Remove all practices with its family because we
            # already have a suggestion from that family
            family = candidate.practice.airtable_json['fields'].get('Famille')
            if family:
                for i in range(len(chunks)):
                    chunks[i] = list(filter(lambda x: x.practice.airtable_json['fields'].get('Famille') != family, chunks[i]))

            suggestions[index] = candidate

        return suggestions

    def _calculate_weight(self, practice):
        weight = 1
        form = self.form

        practice_added_cultures = [Culture(x) for x in (practice.added_cultures or [])]
        practice_target_cultures = [Culture(x) for x in (practice.target_cultures or [])]
        practice_problems_addressed = [Problem(x) for x in (practice.problems_addressed or [])]
        practice_weeds = [Weed(x) for x in (practice.weeds or [])]
        practice_pests = [Pest(x) for x in (practice.pests or [])]
        practice_types = list(practice.types.all())

        # If the practice is blacklisted we return 0
        if str(practice.id) in self.blacklisted_practices:
            return 0

        # If the practice type is blacklisted we return 0
        for practice_type in practice_types:
            if str(practice_type.id) in self.blacklisted_types:
                return 0

        # If this practice applies to a culture that the user does not have, there
        # is no need to keep it. On the other hand, if the practice applies to a culture
        # the user has, we should bump it up a bit because it will be more relevant.
        target_culture_multiplier = 1.3
        if practice_target_cultures:
            if not form.cultures:
                return 0
            relevant_user_cultures = [x for x in form.cultures if x in practice_target_cultures]
            if not relevant_user_cultures:
                return 0
            else:
                weight *= target_culture_multiplier

        # If the practice adds a culture that the user already has,
        # we can return a score of 0
        if form.cultures and practice_added_cultures:
            redundant_cultures = [x for x in form.cultures if x in practice_added_cultures]
            if redundant_cultures:
                return 0

        # If the practice needs ground work / tillage and the
        # user can't carry it out, the score should be 0
        if practice.needs_tillage and form.tillage_feasibility is not None and not form.tillage_feasibility:
            return 0

        # If the practice is favorable or unfavorable to livestock
        # farms, it's score will change
        if form.livestock and practice.livestock_multiplier:
            weight *= float(practice.livestock_multiplier)

        # If the practice is favorable or unfavorable to direct sale
        # farms, it's score will change
        if form.direct_sale and practice.direct_sale_multiplier:
            weight *= float(practice.direct_sale_multiplier)

        # We check what kind of problem the user has to see if the practice
        # corresponds to it
        problem = form.problem
        correct_problem_multiplier = 1.5

        if problem and practice_problems_addressed and (problem in practice_problems_addressed):
            weight *= correct_problem_multiplier

        # Additionally, if the practice specifically targets one of the
        # pests or weeds the user is having problems with, we will bump it
        # even higher
        correct_target_multiplier = 1.2

        if problem == Problem.DESHERBAGE and form.weeds and practice_weeds:
            common_weeds = set(form.weeds).intersection(practice_weeds)
            if common_weeds:
                weight *= correct_target_multiplier

        if problem == Problem.RAVAGEURS and form.pests and practice_pests:
            common_pests = set(form.pests).intersection(practice_pests)
            if common_pests:
                weight *= correct_target_multiplier

        # We take a look at what kind of initiatives the user has already
        # tried. If the user has tried one of the practice types that have
        # a penalty, we will multiply the practice by the lowest penalty among
        # the eligible ones in order to handicap it.
        applicable_practice_types = list(filter(lambda x: x.penalty and x.penalty < 1.0, practice_types))

        applicable_penalties = []
        if form.tested_practice_types:
            for tested_practice_type in form.tested_practice_types:
                applicable_practice_type = next(filter(lambda x: x.category == tested_practice_type.value, applicable_practice_types), None)
                if applicable_practice_type:
                    applicable_penalties.append(float(applicable_practice_type.penalty))

        if applicable_penalties:
            weight *= min(applicable_penalties)

        # We take a look at the advancement level to determine whether or not
        # this practice should be bumped up
        # TODO - How do we do it?
        advancement_level = form.advancement_level

        # We check the department. If the user department has a multiplier
        # in this practice we will use it.
        department_multiplier = practice.get_user_department_multiplier(form.department)
        weight *= float(department_multiplier)

        # We will multiply by the precision level to favor more
        # specific practices
        # TODO: What do I do with the precision ? I could combine it with weight and practice groups?
        # weight *= float(practice.precision)

        return weight
