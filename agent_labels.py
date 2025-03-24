_labels = {}

def label(*label_names):
    def decorator(cls):
        for label_name in label_names:
            if label_name not in _labels:
                _labels[label_name] = []
            _labels[label_name].append(cls)
        
        cls._labels = label_names
        return cls
    return decorator

def get_classes(label_name):
    return _labels.get(label_name, [])