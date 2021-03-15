<!-- modal component which shows the model's weights-->
<template>
    <div class="modal fade" :id="idModal"  tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
    <div class="modal-dialog" role="document">
    <div class="modal-content" >
      <div class="modal-header" id='rotationDialogHeader'>
        <h6 class="modal-title" id="modalTitle">Dataset's weights influence on variable <br>
        </h6>
      </div>
      <div class="modal-body" id="body" @wheel="handleScroll($event)">
          <LineChart v-if='dataset != null' :options='opt' :chartData="dataset"></LineChart>
          <div class="xlabel">variable</div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary btn-sm" data-dismiss="modal">Save and close</button>

      </div>    
    </div>
  </div>
</div>
</template>

<script>
import LineChart from './Chart.vue'
import $ from 'jquery';
window.jQuery = $
require('bootstrap')
export default {
    data() {
        return {
            colors: ['#9b5de5','#fee440','#00bbf9'],
            dataset: null,
            idModal: '',
            opt: {}
        }
    },
    components: {
        LineChart 
    },
    props: {
        weigthted_data: Array,
        dataset_headers: Array,
        filename:String,
        showModal:Boolean
    },
    methods: {

    },
    watch: { 
        showModal: function() { // watch it
            $('#' + this.idModal).modal()
        
        }
    },
    mounted() {
        var list = []
        var arr = new Array(100);
        this.idModal = this.filename.split('.')[0] + "_modal"

        //create data to plot
        for(var i = 0; i < this.dataset_headers.length; i++) {
            var obj = {
                ['data'] : this.weigthted_data[i],
                ['backgroundColor']: this.colors[i],
                ['label']: this.dataset_headers[i]

            }
            list.push(obj)
        }

        for(var j = 0; j < 100; j++)  {
            arr[j] = j
        }

        this.dataset = 
        {
            labels: arr,
            datasets: list
        }
    }
}
</script>
<style lang="scss">
    #modalTitle{
        margin-left: auto;
        margin-right: auto;
    }

    .xlabel{color: gray;}
</style>