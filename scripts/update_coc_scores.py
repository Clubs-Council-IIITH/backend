import json
from misc.models import COC


def run():
    scores = {}
    with open("scripts/scores.json") as f:
        scores = json.load(f)

    for cluster, score in scores.items():
        coc_instance, _ = COC.objects.get_or_create(cluster=cluster)
        coc_instance.score = score
        coc_instance.save()

    print("Updated scores.")
