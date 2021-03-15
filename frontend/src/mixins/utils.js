var xlsx = require('xlsx');
const allowed_extensions = ['xlsx', 'csv']
export default { 
    methods: {
        /**
         * handles the input data (xlsx and csv) 
         * @param file input data file
         * @returns 
         */
        checkInputFile(file) {     
            return new Promise((resolve) => {
                var reader = new FileReader();

                if(file.name.split('.')[1] == 'csv'){
                    reader.onload = resolve
                    reader.readAsText(file);
                }
                else if(file.name.split('.')[1] == 'xlsx') {

                    reader.onload = resolve
                    reader.readAsBinaryString(file);
                } 
            })
            
        },

        /**
         * check the file's extension and and whether it is a copy before creating its component
         * @param 
         * file: input data file
         * isInvalid(boolean): whether the dataset is vaild or not
         * @returns 
         */
        checkExtensionAndCopy(file,isInvalid) {
            var file_extension = (file.name).split(".")[1]
            if(!allowed_extensions.includes(file_extension)) {
                //TO-DO: raise error with toast notification
            }

            var file_array = Array.from(this.files)
            //duplicated file won't be added to the file array
            var is_a_copy = false
            file_array.forEach(file2 => {
                if(file2.name == file.name){
                    is_a_copy = true
                }
            });

            if(!is_a_copy && !isInvalid) {
                this.files.push(file)
            }
        },
        /**
         * filters the file list, removing copies and invalid datasets. Then emit a signal for creating the components which host valid datasets
         * @param 
         * files: input data file list
         * @returns 
         */
        async filterUploadedFiles(files) {

            var isNeeded = this.isFrictionNeeded
            for(var i = 0; i<files.length;i++){

                var isInvalid = await this.checkInputFile(files[i],isNeeded).then( function(event){
                    if(files[i].name.split('.')[1] == 'csv') {
                        var csv = event.target.result;
                        if(csv.includes('friction') == isNeeded) { 
                            console.log('error with friction')
                            return true
                            //TO-DO : toast
                        }
                    }

                    if(files[i].name.split('.')[1] == 'xlsx') {
                        var data = event.target.result 
                        var workbook = xlsx.read(data, {
                            type: 'binary'
                        });

                        var sheet_name_list = workbook.SheetNames;
                        var xlData = xlsx.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]);
                        if(!isNeeded) {
                            if(xlData[0]['Friction Torque [Nm]']|| xlData[0]['Friction Torque [Nm]'] ){
                                        console.log('error: friction detected')
                                        return true
                                    }
                        }
                        else if(isNeeded) {
                            if(xlData[0]['Friction Torque [Nm]'] == null || xlData[0]['Friction Torque [Nm]'] == null){
                                        console.log('error: friction detected')
                                        return true
                                    }
                        }
                        

                    }
                    return false   
                })

                this.checkExtensionAndCopy(files[i],isInvalid) 
            }
            this.$emit('files-uploaded', this.files)
        },

    }
}