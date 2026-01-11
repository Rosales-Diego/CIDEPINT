import axios from 'axios';

export default (await import('vue')).defineComponent({
    components: {
        MenuBar,
        ButtonInfo,
    },
    data() {
        return {
            ListServices: null,
            page: 1,
            per_page: 5,
            cantInst: null,
            ListIntitutions: null,
        };
    },
    mounted() {
        this.cargarPagina(this.page);
    },
    methods: {
        cargarPagina(pagina) {
            axios.get(`/api/services/search?page=${pagina}&per_page=${this.per_page}`)
                .then(response => {
                    // Verificar si la respuesta tiene la propiedad 'data'
                    if (response && response.data) {
                        // Traigo todos los servicios
                        this.ListServices = response.data;
                        // Traigo la cantidad de Instituciones en una consulta
                        return axios.get('api/institutions?page=1&per_page=1');
                    } else {
                        console.error('La respuesta no tiene la propiedad "data".', response);
                        // Manejar el error o realizar alguna acción necesaria
                    }
                })
                .then(response => {
                    // Verificar si la respuesta tiene la propiedad 'data'
                    if (response && response.data) {
                        // Seteo la cantidad de instituciones para tener una lista completa de todas las instituciones 
                        this.cantInst = response.data.total;
                        return axios.get(`api/institutions?page=1&per_page=${this.cantInst}`);
                    } else {
                        console.error('La respuesta no tiene la propiedad "data".', response);
                        // Manejar el error o realizar alguna acción necesaria
                    }
                })
                .then(response => {
                    // Verificar si la respuesta tiene la propiedad 'data'
                    if (response && response.data) {
                        this.ListIntitutions = response.data.data;
                    } else {
                        console.error('La respuesta no tiene la propiedad "data".', response);
                        // Manejar el error o realizar alguna acción necesaria
                    }
                })
                .catch(error => {
                    console.error('Error al obtener servicios:', error);
                });
        },
        verMas(service) {
            // Lógica para manejar la acción "Ver más" de un servicio específico
            if (service.enabled) {
                // Mostrar mensaje de confirmación si el servicio está habilitado
                if (window.confirm('¿Está seguro que quiere ir?')) {
                    console.log(`Ver más sobre el servicio: ${service.name}`);
                }
            } else {
                // Mostrar mensaje de servicio no disponible si el servicio no está habilitado
                alert('Servicio no disponible');
            }
        },
        getInstitutionName(institutionId) {
            // Función para obtener el nombre de la institución a partir de su ID
            const institution = this.ListIntitutions.find(inst => inst.id === institutionId);
            return institution ? institution.name : 'No disponible';
        },
        truncateDescription(description) {
            // Función para truncar la descripción a 100 caracteres
            return description.length > 100 ? description.slice(0, 100) + '...' : description;
        },
        mostrarVistaInfo(servicioId) {
            // Lógica para mostrar la vista Info_Service con el ID del servicio
            // Puedes usar un enrutador (router) o mostrarla de alguna otra manera
            console.log(`Mostrar la vista Info_Service para el servicio con ID: ${servicioId}`);
        },
    }
});
