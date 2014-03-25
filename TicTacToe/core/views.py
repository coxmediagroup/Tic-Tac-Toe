# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.

from django.shortcuts import render

def standard(request):
    msg = None
    return render(request, 'grid.html', {'msg': msg})