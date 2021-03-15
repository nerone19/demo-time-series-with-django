<!-- dataset with gt component used for showing the models' performance and let the user choose the algorithm for predicting the variable-->
<template>
    <!--compontent which handles the logic for one uploaded dataset -->
    <div id = "DatasetModel" :key="componentKey">
        <!--component displayed as a card  -->
        <div class="card">
            <div class= "card-header">
                <div class='card-text"' >{{fileObj.name}}</div>

                <div v-if='isPredicted'>
                    <label for="formGroupExampleInput" >Choose the model to predict with</label>
                    <select v-model="modelSelectedForPrediction" @change="modelForPredictionSelected()">
                        <option v-for="model in model_list" v-bind:key="model.value">{{model}}</option>
                    </select>
                </div>
            </div>
            <img class="card-img-top">
            <!-- the card's body  -->
            <div class="card-body">

                <!---->
                <div class ="row" v-if='!isPredicted'>
                    <div class = "col-lg-4">
                        <select class="form-control" v-model="modelSelected" multiple>
                            <option disabled value="">Select one model</option>
                            <option v-for="model in model_list" v-bind:key="model.value">{{model}}</option>
                        </select>
                    </div>
                    <div class = "col-lg-4">
                        <select class="form-control" v-model="datasetTypeSelected" @change="dataTypeToPredict()">
                            <option disabled value="">Select the dataset type</option>
                            <option>KRL</option>
                            <option>5316</option>
                            <option>FBT</option>
                        </select>
                    </div>  

                    <div class = "col-lg-4">
                        <button type="button" class="btn btn-success" v-on:click='sendPredictionRequest()'
                            v-if="modelSelected != '' && datasetTypeSelected != '' && !isPredicted">Predict
                        </button>
                    </div>

                </div>




                <div v-if="isPredicted">
                    <button class="btn btn-primary btn-sm buttons" id = 'backButton' v-on:click='goBack()' > Try another model</button>
                    or
                    <button class="btn btn-primary btn-sm buttons" id = 'saveButton'>Save it	</button>
                </div>     

                
                <img :src="'data:image/png;base64,' + variable_prediction_image" v-if="isPredicted" class="cardImg">
            </div>

            <div v-if='areWeightsPresent' class="card-footer text-muted">
                <button class="btn btn-primary btn-sm buttons" v-on:click="showModalWithWeights()">show weights</button>
            </div>
                
        </div>

    <WeightsDialog v-if="areWeightsPresent"  :showModal="showModal" :filename="filename" :weigthted_data="weigthted_data" :dataset_headers="dataset_headers"  
          ></WeightsDialog>
   
    </div>

    
    
</template>


<script>
import axios from 'axios';
import store  from '../store';
import utilsMixin from '../mixins/utils'
import WeightsDialog from '../components/weightsDialog'
export default {
    name: 'DatasetModel', 
    components: {
        WeightsDialog 
    },
    mixins:[utilsMixin],
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
            isPredicted: false,
            componentKey: 0,
            data:[],
            weigthted_data: [],
            dataset_weigths: [],
            dataset_headers: [],
            areWeightsPresent: false,
            dataset: null,
            showModal: false,
            filename: '',
        }
    },
    methods: {

        /**
         * it clears the component and restores it as it was before the prediciton
         * @param 
         * @returns 
         */
        goBack() {
            this.isPredicted = false
            this.modelSelected = []
            this.datasetTypeSelected = ''
            this.predictedVariable = []
            this.areWeightsPresent = false
            this.componentKey++
            store.commit('deleteDataset') 

        },
        /**
         * it updates the model chosen yb the user for predicting the dataset without ground-truth
         * @param 
         * @returns 
         */
        modelForPredictionSelected() {
            store.commit('setModelForPrediction', this.modelSelectedForPrediction)
        },
        /**
         * it updates the current analysed dataset type in order to update next every "Dataset-to-predict" with the chosen model
         * @param 
         * @returns 
         */
        dataTypeToPredict() {
            store.commit('setDatasetTypeForPrediction', this.datasetTypeSelected)
        },
        /**
         * it sends the prediction request to the backend and handles the http response
         * @param 
         * @returns 
         */
        sendPredictionRequest() {
            var formData = new FormData();
            formData.append("isGtPresent", true);
            formData.append("dataset-file", this.fileObj);
            formData.append("data-type", this.datasetTypeSelected);
            formData.append("model-type", this.modelSelected);

            axios.post('http://127.0.0.1:8000/predictor/predict-dataset/',   //entrypoint
            formData,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {
                this.isPredicted = true          
                this.variable_prediction_image = res.data.plot
            })
            this.show_weights() 


        },
        /**
         * it turned on/off the weightsDialog's prop for showing the modal 
         * @param 
         * @returns 
         */
        showModalWithWeights() {
            this.showModal = !this.showModal
        },
         /**
         * it sends an ajax request to the system for showing the model's weights for the required dataset
         * @param 
         * @returns 
         */
        show_weights() {
            var formData = new FormData();
            formData.append("dataset-file", this.fileObj);

            axios.post('http://127.0.0.1:8000/predictor/show-weights/',   //entrypoint
            formData,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {      
                this.dataset_weigths = res.data.weights
                this.dataset_headers = res.data.headers
                this.weigthted_data = res.data.plot_data
                //console.log(this.weigthted_data[0]) 
                store.commit('addFileName',this.fileObj.name.split('.')[0])
                store.commit('addWeights', this.dataset_weigths)
                store.commit('addHeaders', this.dataset_headers)
                this.areWeightsPresent = true
            })
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
        }
    },
    created() {
        document.getElementById('model_list').children.forEach(child => {
            this.model_list.push(child.innerHTML)
        });
        this.filename =this.fileObj.name.split('.')[0]
    }
}
</script>


<style lang="scss">

    .cardImg {
        max-height:100%; max-width:100%;
    }
</style>