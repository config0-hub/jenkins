def default():

    task = {'method': 'shelloutconfig',
            'metadata': {'env_vars': ['config0-publish:::ansible::hosts'],
                         'shelloutconfigs': ['config0-publish:::ansible::resource_wrapper']}}

    return task
