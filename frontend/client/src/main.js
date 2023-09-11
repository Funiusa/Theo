import { createApp } from 'vue'
import App from './App.vue'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import router from './router'
import './assets/global.css'
import '../node_modules/vue-markdown/dist/vue-markdown.js'
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt();

createApp(App).use(router).directive('markdown', {
    mounted(el, binding) {
        el.innerHTML = md.render(binding.value);
    },
}).mount('#app')
