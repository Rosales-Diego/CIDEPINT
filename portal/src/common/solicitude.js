import axios from '../common/services';
export const SolicitudePost = {
    postSolicitude: (data,headers) => {
        axios.post('/api/me/requests/', data,headers)
        .then(response => {
            // Manejar la respuesta
            console.log('Código de estado:', response.status);
            console.log('Respuesta:', response.data);
        })
        .catch((error)=> console.error(error));

    }
}