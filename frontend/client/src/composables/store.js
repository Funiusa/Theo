import { createStore } from 'vuex';

const store = createStore({
  state: {
    technologies: [],
  },
  mutations: {
    setTechnologies(state, data) {
      state.technologies = data;
    },
  },
  actions: {
    async fetchTechnologies({ commit }) {
      try {
        const token = localStorage.getItem("token")
        const response = await fetch('http://0.0.0.0:8000/api/v1/technologies/', {
            headers: { Authorization: 'Bearer ' + token },
        });
        const data = await response.json();
        commit('setTechnologies', data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
  getters: {
    getTechnologies: (state) => state.technologies,
  },
});

export default store;