<template>
  <div class="about">
    <UploadArea @files-uploaded="filesUploaded" :isVariableNeeded='false'>
      Drag here the Dataset(s) you want to predict
      </UploadArea>
    
    
    <div class="row">
      <div class="col-lg-6 " v-for="file in files" :key="file.name">                
        <component :is='currentDatasetType' :fileObj="file"/>
      </div>
    </div>
  </div>
</template>

<script>
import DatasetToPredict from '../components/DatasetToPredict.vue';
import UploadArea from '@/components/UploadArea.vue'
import DatasetModel from '@/components/DatasetModel.vue'
export default {
  name: 'About',
  data() {
    
        return {
          currentDatasetType:'',
          files:[]
        }

  },
  components: {
    UploadArea,
    DatasetModel,
    DatasetToPredict
  },
  methods: {
    filesUploaded(files) {
      this.files = files
    }
  },
  mounted() {
    console.log(this.$route.name)
    if(this.$route.name == 'toPredict') {
      this.currentDatasetType = DatasetToPredict
    }
  }



}
</script>>