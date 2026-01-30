from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import services

@api_view(["GET"])
def dashboard_options(request):
    return Response(services.options(request.query_params))

@api_view(["GET"])
def dashboard_summary(request):
    return Response(services.summary(request.query_params))

@api_view(["GET"])
def dashboard_grouped(request):
    group_by = request.query_params.get("group_by", "city")
    metric = request.query_params.get("metric", "median")
    limit = int(request.query_params.get("limit", "20"))
    try:
        return Response(services.grouped(request.query_params, group_by, metric, limit))
    except ValueError:
        return Response({"error": "INVALID_GROUP_BY"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def dashboard_distribution(request):
    bins = int(request.query_params.get("bins", "20"))
    return Response(services.distribution(request.query_params, bins=bins))

@api_view(["GET"])
def dashboard_compare(request):
    return Response(services.compare(request.query_params))
