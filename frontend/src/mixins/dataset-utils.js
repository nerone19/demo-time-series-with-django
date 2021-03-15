import axios from 'axios';
export default { 
    methods: {
        //TO-DO
        saveDataset() {
            var formData = new FormData();
            formData.append("isGtPresent", true);
            formData.append("dataset-file", this.fileObj);
            formData.append("data-type", this.datasetTypeSelected);
            formData.append("model-type", this.modelSelected);

            axios.post('http://127.0.0.1:8000/predictor/save-dataset/',   //entrypoint
            formData,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {
                console.log(res)
            })
        },
        /**
         * it asks for an asynchronous prediction request to the backend and give the promise back
         * @param 
         * payload: the dataset's details to predict
         * @returns 
         * promise
         */
        async sendAutomaticPrediction( payload) {
            console.log(payload)
            var formData = new FormData();
            formData.append("dataset-file", payload.file);
            formData.append("data-type", payload.data_type);
            formData.append("model-type", payload.model_type);
            
            return await axios.post('http://127.0.0.1:8000/predictor/predict-dataset/',   //entrypoint
                    formData,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
    
        }
    }
}