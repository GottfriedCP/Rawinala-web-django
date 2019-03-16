def set_template_language(template_name, lang_code=None):
    final_template = template_name
    if lang_code == 'en':
        final_template = final_template + '_en'
    return final_template + '.html'
