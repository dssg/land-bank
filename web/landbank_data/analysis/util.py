def median_value(queryset,term):
    # computes ....surprise, the median
    count = queryset.count()
    return queryset.values_list(term, flat=True).order_by(term)[int(round(count/2))]
