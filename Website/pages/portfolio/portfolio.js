

var frmvalidator  = new Validator("contactform");
frmvalidator.addValidation("name","req","Please provide your name");

frmvalidator.addValidation("email","req","Please provide your email");

frmvalidator.addValidation("email","email",
	"Please enter a valid email address");



/*
let myLibrary = [];

//Book Constructor
function Book(title, author) {
	this.title = title;
	this.author = author;
}

function addBookToLibrary(title, author) {
	

}

//const addBtn = document.getElementById('add');



const addBtn = document.querySelector("#add");



addBtn.addEventListener('click', (e) => 
{
	const title = document.getElementById('title').value;
	const author = document.getElementById('author').value;
	addBookToLibrary(title, author);

});
*/