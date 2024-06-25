# serializers.py
from rest_framework import serializers

class QueryBuilderSerializer(serializers.Serializer):
    Companyname = serializers.CharField(required=False)
    Domain = serializers.CharField(required=False)
    Yearfounded = serializers.IntegerField(required=False)
    Country = serializers.CharField(required=False)
    Currenteployees = serializers.IntegerField(required=False)
    Totalemployees = serializers.IntegerField(required=False)
