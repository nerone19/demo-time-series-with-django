<template>
<div>   

    <table v-if="tableCount > 0" class="table table-dark">
    <thead>
        <tr>
            <th>Filename</th> 
            <th>variables</th> 
            <th>values</th> 
        </tr>
    </thead>
    <tbody>
        <tr v-for="(el,index) in filename_list" :key="index">
            <td>{{el.filename}}</td>
            <td>{{header_list[index].headers}}</td>
            <td>{{weight_list[index].weights}}</td>
        </tr>        
    </tbody>
    <button class="btn" id="downloadTableButton" v-on:click="exportTableToCSV()"> Download table
    </button>

    
    </table>
    </div>
</template>

<script>
import store  from '../store';
    export default {

        data() {
            return {
                dataset : {}
            }
        },
        methods: {
            downloadCSV(csv, filename) {
                var csvFile;
                var downloadLink;

                // CSV file
                csvFile = new Blob([csv], {type: "text/csv"});

                // Download link
                downloadLink = document.createElement("a");

                // File name
                downloadLink.download = filename;

                // Create a link to the file
                downloadLink.href = window.URL.createObjectURL(csvFile);

                // Hide download link
                downloadLink.style.display = "none";

                // Add the link to DOM
                document.body.appendChild(downloadLink);

                // Click download link
                downloadLink.click();
            },
            exportTableToCSV(filename) {
                var csv = [];
                var rows = document.querySelectorAll("table tr");
                
                for (var i = 0; i < rows.length; i++) {
                    var row = [], cols = rows[i].querySelectorAll("td, th");
                    
                    for (var j = 0; j < cols.length; j++) 
                        row.push(cols[j].innerText);
                    
                    csv.push(row.join(","));        
                }

                // Download CSV file
                this.downloadCSV(csv.join("\n"), filename);
            },
        },
        computed: {
            weight_list() {
                return store.getters.getWeightList
            },
            header_list() {
                return store.getters.getHeaderList
            },
            tableCount() {
                return store.getters.tableCount
            },
            filename_list() {
                return store.getters.getFilenameList
            }
        }        
        
    };
</script>


<style lang="css" scoped>
#downloadTableButton {
    width: 100%;
    background-color: white;
    border: solit black;
    border-color: black;
}
</style>