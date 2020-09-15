from rest_framework import fields, serializers

from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    def validate_pdf(self, value):
        if value:
            if value.size > 20971520:
                raise serializers.ValidationError(
                    "PDF is too large! The maximum file size is 20MB."
                )
        return value

    class Meta:
        model = Proposal
        fields = "__all__"
