from core.models import ParameterConfig


def get_param_config_tag(tag):
    """ Get all param configs related to the tag"""
    recs = ParameterConfig.objects.filter(tag=tag)
    if not recs:
        return None

    return {rec.name: rec.content for rec in recs}
