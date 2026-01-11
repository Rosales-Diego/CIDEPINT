import axios from '../common/services';
export const UserServices = {
    getProfile: (action,headers) => {
        axios.get('/api/me/profile/',headers)
        .then((data)=> {
            action(data.data)
        })
        .catch((error)=> console.error(error));

    }
}

export const UserNote = {
    getProfile: (action,headers) => {
        try{
            return axios.get('/api/me/profile/',headers)

        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

    }
}
export const finishedRequest = {
    getFinished: (headers) => {
        try{
            const aux = axios.get('/api/me/requests/finished',{headers})
        console.log(aux)
        return aux;
        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

        
    }
}

export const listRequest = {
    getList: (headers) => {
        try{
            const aux = axios.get('/api/me/requests/list',{headers})
        return aux;
        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

        
    }
}

export const listRequestWithNameService = {
    getList: (headers) => {
        try{
            const aux = axios.get('/api/me/requests/listWithName',{headers})
        return aux;
        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

        
    }
}


export const listNotesForService = {
    getList: (params, headers) => {
        try{
        
            const aux = axios.get('/api/notes/me_notes_for_solicitude',
            {
                params: params,
                headers: headers,
            })
            return aux;

        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

        
    }
}




export const commentNote = {
    send: (body, params, headers) => {
        try{
        
            const aux = axios.post('/api/me/requests/notes/',
            body,
            {
                params: params,
                headers: headers,
            })
        return aux;
        } catch (e){
            console.log("Tenes un problemita por acá ",e)
        }

        
    }
}