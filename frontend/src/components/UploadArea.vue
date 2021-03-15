<template>
<div id='UploadArea' class="jumbotron" :key="keyComponent">

    <div class="upload-area"  id="dragAndDropArea" @dragenter="dragEnter" v-on:drop ="drop" v-on:dragover ="dragOver">
        
        <h5><slot></slot></h5>
        <!--TO-DO <font-awesome-icon class="DragIcon" style="width:50%;" :icon="['fas','upload']"/>-->
        <div class="custom-file mb-3">
            or <input class="btn btn-dark btn-sm"  type="file" id="files" ref="files"  v-on:change="handleMultiUploadedFile()"  multiple><br><br>
        </div>
    </div>
    <button id="clearButton" class="btn btn-dark btn-sm fade-in jumbotron-button" v-if="files.length > 0" @click ="clearEverything()">Clear everything</button> 
    
</div>

</template>


<script>
 import $ from 'jquery';
 import store from '../store'
 import utilsMixin from '../mixins/utils'
 export default {
    name: 'UploadArea',      
    components: {
    },
    data() {
        return {
            files:[],
            keyComponent: 0
        }
    },
    mixins:[utilsMixin],
    props: {
        isVariableNeeded: Boolean
    },
    methods: {
        clearEverything(){
            this.$refs.files = []
            this.keyComponent++
            this.files = []
            store.commit('clearTable')
            this.$emit('files-uploaded', this.files)
        },
        handleMultiUploadedFile() {
            var files =  this.$refs.files.files;
            this.filterUploadedFiles(files)

        },
        dragEnter(e) {
            e.preventDefault();
            e.stopPropagation();
        },
        dragOver(e) {
                e.preventDefault();
                e.stopPropagation();
        },
        drop(e) {
                var files = e.dataTransfer.files
                this.filterUploadedFiles(files)
                e.stopPropagation();
                e.preventDefault();

        }
    },
    created() {

        $(function() {
            
            // preventing page from redirecting
            $("html").on("dragover", function(e) {
                e.preventDefault();
                e.stopPropagation();
            });

            $("html").on("drop", function(e) { e.preventDefault(); e.stopPropagation(); });

        });
    }
}
</script>