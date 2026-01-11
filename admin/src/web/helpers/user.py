def fill_form_with_user(form, user):
    fill_update_form_with_user(form, user)
    form.password.default = user.password
    return form

def fill_update_form_with_user(form, user):
    form.email.default = user.email
    form.name.default = user.name
    form.last_name.default = user.last_name
    form.active.default = "activo" if user.active else "inactivo"
    
    return form
