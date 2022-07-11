const container = document.querySelector('#container');
	const content = document.createElement('results');
	content.classList.add('results');

let wins = 0, losses = 0, draws = 0;



// EVENT LISTENERS
const rockBtn = document.querySelector('#rock');

const paperBtn = document.querySelector('#paper');

const scissorsBtn = document.querySelector('#scissors');

rockBtn.addEventListener('click', () => {
	result = playRound('rock',computerPlay())
});

paperBtn.addEventListener('click', () => {
	result = playRound('paper',computerPlay())
});

scissorsBtn.addEventListener('click', () => {
	result = playRound('scissors',computerPlay())
});




// FUNCTIONS

function computerPlay() {
	a = Math.floor(Math.random() * 3);

	return a;
}

function playRound(playerSelection, computerSelection){

	playerSelection = playerSelection.toLowerCase();

	if(playerSelection == "rock"){
		if(computerSelection == 1){
			displayResults("loss")
		} else if(computerSelection == 2){
			displayResults("win")
		} else {
			displayResults("draw")
		}
	} else if(playerSelection == "paper"){
		if(computerSelection == 0){
			displayResults("win")
		} else if(computerSelection == 2){
			displayResults("loss")
		} else {
			displayResults("draw")
		}
	} else if(playerSelection == "scissors"){
		if(computerSelection == 0){
			displayResults("draw")
		} else if(computerSelection == 1){
			displayResults("loss")
		} else {
			displayResults("draw")
		}
	} 
}

function displayResults(result){
	if(result == "win"){
		content.textContent = 'You Win!';
	} else if(result == "loss"){
		content.textContent = 'You Lose :(';
	} else {
		content.textContent = 'Draw!';
	}

	container.appendChild(content);

}






// Legacy function for when the game outputed to console and played 5 games back to back.
function game() {
	let wins = 0, losses = 0, draws = 0;
	
	/*
	for(i = 0; i < 5; i++){
		let result = playRound(getPlayerInput(),computerPlay());
		if(result == "win"){
			wins++;
		} else if(result == "loss"){
			losses++;
		} else {
			draws++;
		}
		console.log(result);
	}
	*/

	if(wins > losses) {
		console.log("Congrats! You win!")
	} else if(wins < losses) {
		console.log("You lose :(")
	} else {
		console.log("It was a draw.")
	}
}