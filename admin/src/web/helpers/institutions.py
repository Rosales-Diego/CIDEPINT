def fill_form_with_institution(form, institution):
    """
    Función que llena un formulario, a partir un elemento de un modelo.
    """

    form.nombre.default = institution.name
    form.localizacion.default = institution.location
    form.direccion.default = institution.address
    form.web.default = institution.web
    form.palabras_claves.default = institution.key_words
    #form.descripcion.data = institution.contact_info
    form.horario.default = institution.work_schedule
    form.estado.default = "habilitado" if institution.active else "deshabilitado"
    form.telefono.default = institution.contact_info

    return form