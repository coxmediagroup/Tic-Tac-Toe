

class View(object):
    """
        Defines the needed __new__ method to make 
        classes work as view callables.  Extend this class
        for all views that you want to use as class callables.
    """

    # from codysoyland, this might be more thread safe
    def __new__(cls, *args, **kwargs):
        def view_wrapper(request, *args, **kwargs):
            view = object.__new__(cls)
            return view(request, *args, **kwargs)
        return view_wrapper

    """
    # this is our older version, may not be thread safe
    def __new__(cls, request, *args, **kwargs):
        obj = super(View, cls).__new__(cls)
        return obj(request, *args, **kwargs)
    """
    
    #def __init__(self):
    #    pass
        
    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        if self.request.method == 'POST':
            return self.post()
        return self.get()
        
def decorate_method(function_decorator):
    """
        This decorator allows you to use standard
        Django decorators on class style views 
        
        Example:
        
        >>> @decorate_method(django_decorator(params))
        ... def class_method(self, request)
        ...    pass
    """
    def d_method(unbound_method):
        def method_proxy(self, *args, **kwargs):
            def f(*a, **kw):
                return unbound_method(self, *a, **kw)
            return function_decorator(f)(*args, **kwargs)
        return method_proxy
    return d_method
            
