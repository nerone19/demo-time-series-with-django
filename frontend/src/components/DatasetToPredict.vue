
<!-- dataset-without-gt-component used for showing the predicted variable by the previous model chosen-->
<template>
    <!--compontent which handles the logic for one uploaded dataset -->
    <div id = "DatasetToPredict" :key="componentKey">
        <!--component displayed as a card  -->
        <div class="card">
            <div class= "card-header"> <p class="card-text">{{fileObj.name}}</p>
            
            </div>
            <img class="card-img-top">
            <!--cthe card's body  -->
            <div class="card-body">
                

                <!---->
                <div class ="row" v-if='!isPredicted'>
                    <div class = "col-lg-4">
                        <select class="form-control" v-model="datasetTypeSelected" @change="datasetTypeChosen()">
                            <option disabled value="">Select the dataset type</option>
                            <option>KRL</option>
                            <option>5316</option>
                            <option>FBT</option>
                        </select>
                    </div>  

                    <div class = "col-lg-4">
                        <button type="button" class="btn btn-success" v-on:click='sendPredictionRequest()'
                            v-if="chosenModel != '' && datasetTypeSelected != '' && !isPredicted">Predict
                        </button>
                    </div>

                </div>




                <div v-if="isPredicted">
                    <button class="btn btn-primary btn-sm buttons" id = 'saveButton'>Save it	</button>
                </div>     

                
                <img :src="'data:image/png;base64,' + variable_prediction_image" v-if="isPredicted" class="cardImg">
            </div>

            <div v-if='isPredicted' class="card-footer text-muted">
            </div>
                
        </div>

   
    </div>


    
</template>


<script>
import store  from '../store';
import utilsMixin from '../mixins/utils'
import datasetMixin from '../mixins/dataset-utils'
//import axios from 'axios';
//import LineChart from './Chart.vue'
export default {
    name: 'DatasetToPredict', 
    components: {
        //LineChart 
    },
    mixins:[utilsMixin,datasetMixin],
    props: {
        fileObj: File
    },
    data() {
        return {
            files:[],
            model_list:[],
            modelSelected: [],
            modelSelectedForPrediction: '',
            datasetTypeSelected: '',
            predictedVariable: [],
            variable_prediction_image: '',
            isPredicted: false,
            componentKey: 0,
            data:[]
        }
    },
    methods: {
        /**
         * when the user select the data type, a prediction request will be sent to the system 
         * @param 
         * @returns 
         */
        datasetTypeChosen() {
            if(this.datasetTypeSelected != '' && this.datasetTypeSelected == this.chosenDatasetType && this.chosenModel != '' ) {
                this.variable_prediction_image = ''
                this.sendPredictionRequest()
            }
        },
        /**
         * it handles the an asynchronous prediction request
         * @param 
         * @returns 
         */
        async sendPredictionRequest() {

            await this.sendAutomaticPrediction({'file': this.fileObj, 'data_type': this.datasetTypeSelected, 'model_type':this.chosenModel })  
            .then( (res) => {  
                this.isPredicted = true          
                this.variable_prediction_image = res.data.plot 
            }).catch(err => {console.log(err)})
                

        },
        /**
         * function which will be used in the future for using a third party software for plotting interactive data(now it is bugged)
         * @param predictionList the list of predictions done by the models
         * @returns 
         */
        readPredictionlist(predictionList) {
            var modelPredictionData = []
            for (var i = 0; i < predictionList.length; i++) {
                predictionList[i].forEach(el => {
                        modelPredictionData.push(el[0])
                    });
                this.data.push(modelPredictionData)
            }
        },
        
    },
    computed: {
        chosenModel() {
            return store.getters.getChosenModel
        },
        chosenDatasetType() {
            return store.getters.getDatasetType
        },
    },
    watch: {
        chosenModel(newValue,oldValue) {
            console.log(`yes, computed property changed: ${newValue}`)
            console.log(`before: ${oldValue}`)
            if(this.datasetTypeSelected != '' && this.datasetTypeSelected == this.chosenDatasetType && this.chosenModel != '' ) {
                this.variable_prediction_image = ''
                this.sendPredictionRequest()
            }
        }
    },
    created() {
        document.getElementById('model_list').children.forEach(child => {
            this.model_list.push(child.innerHTML)
        });

    }
}
</script>


<style lang="scss">

    .cardImg {
        max-height:100%; max-width:100%;
    }
</style>