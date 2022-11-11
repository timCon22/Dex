"use strict";

const $pokeList = $("#pokemon-list")
const $searchForm = $("#search-form")
const myPokemon = []

async function getPokemon(query){
    let getPkmn = await axios.get(`https://pokeapi.co/api/v2/pokemon/${query}`)
    console.log(getPkmn)

    populatePokemon(getPkmn)

    const dict_value = {getPkmn};

    const s = JSON.stringify(dict_value);

    $.ajax({
        url:"/grabPkmn",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s)})
    
}


async function populatePokemon(getPkmn) {
    const $pokeList = $("#pokemon-list")
    $pokeList.empty();
      const $item = $(
        `<div data-show-id="${getPkmn.data.id}" id="newpokemon" class="text-center">
           <div class="">
             <img 
                src= ${getPkmn.data.sprites.front_default}  
                class="w-20 mr-3">
             <div class="media-body">
               <h5 class="text-primary" id="pokemon-name">${getPkmn.data.name}</h5>
               <div><small>${getPkmn.data.types[0].type.name}</small> ${getPkmn.data.types.length > 1 ? `/ <small>${getPkmn.data.types[1].type.name}</small>` : ''}</div>
               <form action="/addPkmn" method="POST">
                  <input type="submit" value="Catch!"></input>
               </form>
             </div>
           </div>  
         </div>
        `);
  
      $pokeList.append($item);
}

async function searchForShowAndDisplay() {

    //Add logic to check if pokemon is in a list (txt file)
    
    const query = $("#search-query").val().toLowerCase();

    if (query == ""){
        alert("Please enter a valid Pokemon");
    }
    
    if (isFinite(query)){
        alert("Please enter a valid Pokemon");
    }

    else{
        const pkmn = await getPokemon(query);
    }
}


$searchForm.on("submit", async function(evt){
    evt.preventDefault();
    await searchForShowAndDisplay();
});