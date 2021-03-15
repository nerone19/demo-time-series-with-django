<template>
  <div class="home">
    <UploadArea @files-uploaded="filesUploaded" :isVariableNeeded='true'>
      Drag here your reference Dataset(s) you want to predict the variable with
    </UploadArea>
    
    
    <div class="row">
      <div class="col-lg-6 " v-for="file in files" :key="file.name">                
        <!--<DatasetModel :fileObj="file"> </DatasetModel>-->
        <component :is='currentDatasetType' :fileObj="file"/>
      </div>
    </div>

    <SummaryTable></SummaryTable>
    
  </div>
</template>

<script>
// @ is an alias to /src
import UploadArea from '@/components/UploadArea.vue'
import SummaryTable from '../components/SummaryTable'
import DatasetModel from '@/components/DatasetModel.vue'
import DatasetToPredict from '../components/DatasetToPredict.vue';
export default {
  name: 'Home',
  components: {
    UploadArea,
    DatasetModel,
    DatasetToPredict,
    SummaryTable
  },
  data() {
   return {
            files:[]
        }
  },
  methods: {
    filesUploaded(files) {
      this.files = files
    }

  },
  created() {
    //console.log('created')
  },
  mounted() {
    //console.log(this.$route.name)
    if(this.$route.name == 'toPredict') {
      this.currentDatasetType = DatasetToPredict
    }
    else if (this.$route.name == 'references') { 
      this.currentDatasetType = DatasetModel
    }
  }
}
</script>
