from rest_framework import serializers


class TimeSeriesQuerySerializer(serializers.Serializer):
    param = serializers.ChoiceField(
        choices=[
            'param1',
            'param2',
            'param3',
            'param4',
            'param5'
        ],
        default='param1'
    )

    from_time = serializers.DateTimeField(
        required=False
    )

    to_time = serializers.DateTimeField(
        required=False
    )

