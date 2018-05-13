

def number_or_str(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            if s == 'True':
                return 'True'
            if s == 'False':
                return 'False'
            return s
