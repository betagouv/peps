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

            # Remove all practices with its families because we
            # already have a suggestion from them
            families = candidate.practice.airtable_json['fields'].get('Familles')
            if families:
                for family in families:
                    for i in range(len(chunks)):
                        chunks[i] = list(filter(lambda x: family not in (x.practice.airtable_json['fields'].get('Familles') or []), chunks[i]))

            suggestions[index] = candidate

        return suggestions

    def _calculate_weight(self, practice):
        weight = 1

        if self._is_blacklisted(practice):
            return 0

        if self._adds_existing_culture(practice):
            return 0

        if self._has_incompatible_tillage_needs(practice):
            return 0

        if self._has_incompatible_weeds(practice):
            return 0

        if self._has_incompatible_pests(practice):
            return 0

        if self._has_incompatible_cultures(practice):
            return 0

        weight *= self._get_livestock_multiplier(practice)
        weight *= self._get_direct_sale_multiplier(practice)
        weight *= self._get_highest_problem_match_multiplier(practice)
        weight *= self._get_highest_weed_multiplier(practice)
        weight *= self._get_highest_pest_multiplier(practice)
        weight *= self._get_highest_glyphosate_use_multiplier(practice)
        weight *= self._get_highest_culture_multiplier(practice)
        weight *= self._get_lowest_type_redundancy_multiplier(practice)
        weight *= self._get_department_multiplier(practice)

        return weight

    def _is_blacklisted(self, practice):
        """
        Whether or not the practice or the practice type is blacklisted
        """
        practice_types = list(practice.types.all())
        if str(practice.id) in self.blacklisted_practices:
            return True

        for practice_type in practice_types:
            if str(practice_type.id) in self.blacklisted_types:
                return True
        return False

    def _adds_existing_culture(self, practice):
        """
        Whether the practice aims to add a culture that is already being
        used by the user.
        """
        practice_added_cultures = [Culture(x) for x in (practice.added_cultures or [])]
        if self.form.cultures and practice_added_cultures:
            redundant_cultures = [x for x in self.form.cultures if x in practice_added_cultures]
            if redundant_cultures:
                return True
        return False

    def _has_incompatible_tillage_needs(self, practice):
        """
        Does the practice need ground work / tillage and the
        user can't carry it out?
        """
        if practice.needs_tillage and self.form.tillage_feasibility is not None and not self.form.tillage_feasibility:
            return True
        return False

    def _get_livestock_multiplier(self, practice):
        """
        We get the multiplier applicable for the practice being favorable
        or unfavorable to livestock farms
        """
        if self.form.livestock and practice.livestock_multiplier:
            return float(practice.livestock_multiplier)
        return 1

    def _get_direct_sale_multiplier(self, practice):
        """
        We get the multiplier applicable for the practice is favorable or
        unfavorable to direct sale farms
        """
        if self.form.direct_sale and practice.direct_sale_multiplier:
            return float(practice.direct_sale_multiplier)
        return 1

    def _get_highest_problem_match_multiplier(self, practice):
        """
        We check what kind of problem the user has to see if the practice
        corresponds to it
        """
        practice_problems_addressed = [Problem(x) for x in (practice.problems_addressed or [])]
        problem = self.form.problem
        correct_problem_multiplier = 1.5

        if problem and practice_problems_addressed and (problem in practice_problems_addressed):
            return correct_problem_multiplier
        return 1

    def _has_incompatible_weeds(self, practice):
        """
        If the user does not use weeds that are whitelisted
        for this practice, we deem they are incompatible.
        """
        practice_weeds_whitelist = [Weed(x) for x in (practice.weed_whitelist or [])]

        if practice_weeds_whitelist:
            if not self.form.weeds:
                return True
            matching_user_weeds = [x for x in self.form.weeds if x in practice_weeds_whitelist]
            if not matching_user_weeds:
                return True
        return False

    def _has_incompatible_pests(self, practice):
        """
        If the user does not use pests that are whitelisted
        for this practice, we deem they are incompatible.
        """
        practice_pest_whitelist = [Pest(x) for x in (practice.pest_whitelist or [])]

        if practice_pest_whitelist:
            if not self.form.pests:
                return True
            matching_user_pests = [x for x in self.form.pests if x in practice_pest_whitelist]
            if not matching_user_pests:
                return True
        return False

    def _has_incompatible_cultures(self, practice):
        """
        If the user does not use cultures that are whitelisted
        for this practice, we deem they are incompatible.
        """
        practice_cultures_whitelist = [Culture(x) for x in (practice.culture_whitelist or [])]

        if practice_cultures_whitelist:
            if not self.form.cultures:
                return True
            matching_user_cultures = [x for x in self.form.cultures if x in practice_cultures_whitelist]
            if not matching_user_cultures:
                return True
        return False

    def _get_highest_weed_multiplier(self, practice):
        if practice.weed_multipliers and self.form.weeds:
            relevant_multipliers = list(filter(lambda x: int(list(x.keys())[0]) in self.form.weeds, practice.weed_multipliers))
            if relevant_multipliers:
                max_multiplier = max(map(lambda x: list(x.values())[0], relevant_multipliers))
                return max_multiplier
        return 1

    def _get_highest_pest_multiplier(self, practice):
        if practice.pest_multipliers and self.form.pests:
            relevant_multipliers = list(filter(lambda x: int(list(x.keys())[0]) in self.form.pests, practice.pest_multipliers))
            if relevant_multipliers:
                max_multiplier = max(map(lambda x: list(x.values())[0], relevant_multipliers))
                return max_multiplier
        return 1

    def _get_highest_glyphosate_use_multiplier(self, practice):
        if practice.glyphosate_multipliers and self.form.glyphosate_uses:
            relevant_multipliers = list(filter(lambda x: int(list(x.keys())[0]) in self.form.glyphosate_uses, practice.glyphosate_multipliers))
            if relevant_multipliers:
                max_multiplier = max(map(lambda x: list(x.values())[0], relevant_multipliers))
                return max_multiplier
        return 1

    def _get_highest_culture_multiplier(self, practice):
        if practice.culture_multipliers and self.form.cultures:
            relevant_multipliers = list(filter(lambda x: int(list(x.keys())[0]) in self.form.cultures, practice.culture_multipliers))
            if relevant_multipliers:
                max_multiplier = max(map(lambda x: list(x.values())[0], relevant_multipliers))
                return max_multiplier
        return 1

    def _get_lowest_type_redundancy_multiplier(self, practice):
        """
        We take a look at what kind of initiatives the user has already
        tried. If the user has tried one of the practice types that have
        a penalty, we will return the lowest penalty among the eligible
        ones in order to handicap it.
        """
        practice_types = list(practice.types.all())
        applicable_practice_types = list(filter(lambda x: x.penalty and x.penalty < 1.0, practice_types))

        applicable_penalties = []
        if self.form.tested_practice_types:
            for tested_practice_type in self.form.tested_practice_types:
                applicable_practice_type = next(filter(lambda x: x.category == tested_practice_type.value, applicable_practice_types), None)
                if applicable_practice_type:
                    applicable_penalties.append(float(applicable_practice_type.penalty))

        if applicable_penalties:
            return min(applicable_penalties)

        return 1

    def _get_department_multiplier(self, practice):
        """
        We check the department in the answers. If the user department has a multiplier
        in this practice we will return it.
        """
        if not self.form.department or not practice.department_multipliers:
            return 1
        relevant_multipliers = [list(x.values())[0] for x in practice.department_multipliers if self.form.department == list(x.keys())[0]]
        return float(max(relevant_multipliers)) if relevant_multipliers else 1
