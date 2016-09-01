from utils.models import BaseManager, get_distinct_charfield_opts, \
    get_distinct_charfield


class ExperimentManager(BaseManager):
    assessment_relation = 'study__assessment'


class AnimalGroupManager(BaseManager):
    assessment_relation = 'experiment__study__assessment'


class DosingRegimeManager(BaseManager):
    assessment_relation = 'dosed_animals__experiment__study__assessment'


class DoseGroupManager(BaseManager):
    assessment_relation = 'dose_regime__dosed_animals__experiment__study__assessment'


class EndpointManager(BaseManager):

    def optimized_qs(self, **filters):
        return self.get_queryset()\
                    .filter(**filters)\
                    .select_related(
                        'animal_group',
                        'animal_group__dosed_animals',
                        'animal_group__experiment',
                        'animal_group__experiment__study',
                    ).prefetch_related(
                        'groups',
                        'effects',
                        'animal_group__dosed_animals__doses',
                    )

    def get_system_choices(self, assessment_id):
        return get_distinct_charfield_opts(self, assessment_id, 'system')

    def get_organ_choices(self, assessment_id):
        return get_distinct_charfield_opts(self, assessment_id, 'organ')

    def get_effect_choices(self, assessment_id):
        return get_distinct_charfield_opts(self, assessment_id, 'effect')

    def get_effects(self, assessment_id):
        return get_distinct_charfield(self, assessment_id, 'effect')


class EndpointGroupManager(BaseManager):
    assessment_relation = 'endpoint__assessment'
