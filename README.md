# DEX #

----------

- The Dex is able to get information about any pokemon from any generation and return that to the page from the pokeapi


- You can add pokemon to your favorites list and release them at any time, the Dex will show you the type(s) that the pokemon has as well


- The features added to the site include creating and signing up for an account, auto-login, and the ability to save a specific pokemon list for each user. I chose these key features so that a user would be able to customize their own favorite list


- The flow for the Dex goes as is: signup or login, show the user their homepage and if they have pokemon to show that list from my sql database, if not then display a message to the user that they dont have any pokemon added and/or release a current pokemon on the site. The user has a list of options to pick from in the top left corner of the page that has the username, home button, the "look up a pokemon" button, and a logout button. On the look up a pokemon button it then redirects the user to that page to type in the pokemon and search for that pokemon. The Dex then makes an axios request to the https://pokeapi.co/ where it queries for that pokemon and displays it on the page with the image, type of that pokemon, the name, and a "catch" button where the pokemon will get saved to that specific user. (Any user that is not logged in will not be able to access the full site and will be redirected to the signup/login page!)


- The technologies used to create the Dex are Python, Javascript, HTML, and CSS
