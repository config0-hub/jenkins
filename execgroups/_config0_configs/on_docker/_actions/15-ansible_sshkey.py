def default():

    task = {'method': 'shelloutconfig',
            'metadata': {'env_vars': ['config0-publish:::ansible::ssh_key'],
                         'shelloutconfigs': ['config0-publish:::ansible::resource_wrapper']}}

    return task
