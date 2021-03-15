import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    chosenModel: '',
    chosendatasetType: '',
    weight_list: [],
    header_list: [],
    filename_list: []
  },
  
  getters: {
    getChosenModel: state => { 
        return state.chosenModel
    },

    getDatasetType: state => { 
        return state.chosendatasetType
    },
    tableCount: state => {
      return state.weight_list.length

    },
    getWeightList: state => {
      return state.weight_list

    },
    getHeaderList: state => {
      return state.header_list

    },
    getFilenameList: state => {
      return state.filename_list
    }
  },
  
  mutations: {
    addFileName(state,filename) { 
      state.filename_list.push({filename})
    },
    setModelForPrediction(state, value) {
      state.chosenModel = value
    },
    setDatasetTypeForPrediction(state,value) { 
        state.chosendatasetType = value
    },
    clearTable(state) {
      state.filename_list = []
      state.weight_list = []
      state.header_list =  []
    },
    addWeights(state,weights) {
      state.weight_list.push({weights})
    },
    addHeaders(state,headers) {
      state.header_list.push({headers})
    },
    deleteDataset(state, dataset) { 
      const index = state.filename_list.indexOf(dataset);
      state.filename_list.splice(index, 1);
      state.weight_list.splice(index, 1);
      state.header_list.splice(index,1); 
    }

  },
  actions: {
    
  }
  });