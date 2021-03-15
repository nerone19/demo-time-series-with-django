
<template>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="brand">Variable prediction</div>
         
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
            <a class="nav-item nav-link"> <router-link to="/predictor/">References</router-link> </a>
            <a class="nav-item nav-link"><router-link to="/predictor/about/">To predict</router-link></a>
           <!-- <a class="nav-item nav-link"><router-link to="/predictor/about">Help</router-link></a>-->
            
        </div>
        </div>
    </nav>
</template>


<script>
export default {
  name: 'Navbar'
}
</script>

<style lang="scss">


.navbar {

    .brand {
        color: #2dac56;
        font-weight: bold;
        margin-right: 3em;
    }

    a {
        color: gray;
        .router-link-exact-active {
            color: black;
        }
    }
}



</style>