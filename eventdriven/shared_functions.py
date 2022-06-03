def run_query(model, filename, options=None, params=None):
    with open(filename, 'r') as f:
        query = ""
        for line in f:
            query += line
        
        if options is None:
            if params is None:
                return model.objects.raw(query)
            else:
                return model.objects.raw(query, params)
        else:
            format_str = "query.format("

            for i, key in enumerate(options):
                if i > 0:
                    format_str += ", "
                format_str += "{}={}".format(key, "options['{}']".format(key))
            
            format_str += ")"

            formatted_query = eval(format_str)

            if params is None:
                return model.objects.raw(formatted_query)
            else:
                return model.objects.raw(formatted_query, params)

            
