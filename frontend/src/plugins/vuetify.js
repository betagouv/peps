import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import theme from '@/theme';

Vue.use(Vuetify);

export default new Vuetify({
    theme: theme,
    iconfont: 'md',
})
