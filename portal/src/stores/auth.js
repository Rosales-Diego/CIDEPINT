import { apiService } from '@/api'

const namespaced = true;
const state = {
    user: {},
    isLoggedIn: false
};

const getters = {
    isLoggedIn: state => state.isLoggedIn, user: state => state.user
};
const actions = {
    async loginUser({ dispatch }, user) {
        await apiService.post ('/auth/login_jwt', user)
        await dispatch( 'fetchUser')
    },
    async fetchUser ({ commit }) {
        await apiService.get('/auth/user_jwt')
            .then (({ data }) = commit ('setUser', data))
    },
    async logoutUser ({ commit }) {
        await apiService.get('/auth/logout_jwt');
        commit ('logoutUserState');
    }
}
const mutations = {
    setUser (state, user) {
        state.isLoggedIn = true;
        state.user = user;
    },
    LogoutUserState (state) {
        state.isLoggedIn = false;
        state.user = {};
    }
};