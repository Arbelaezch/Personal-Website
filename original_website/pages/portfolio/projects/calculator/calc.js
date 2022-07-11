const container = document.querySelector('#container');

let display = '';
operand1 = 0;
operand2 = 0;
operator = '';
document.getElementById('display').innerHTML = 'Simple Calculator';


//EVENT LISTENERS
const btn1 = document.getElementById('1');
const btn2 = document.getElementById('2');
const btn3 = document.getElementById('3');
const btn4 = document.getElementById('4');
const btn5 = document.getElementById('5');
const btn6 = document.getElementById('6');
const btn7 = document.getElementById('7');
const btn8 = document.getElementById('8');
const btn9 = document.getElementById('9');
const btn0 = document.getElementById('0');
const btnAdd = document.getElementById('+');
const btnSub = document.getElementById('-');
const btnMult = document.getElementById('*');
const btnDiv = document.getElementById('/');
const btnEval = document.getElementById('=');
const btnAC = document.getElementById('clear');
const btnDec = document.getElementById('.');

btn1.addEventListener('click', () => {
	setDisplay(1);
});
btn2.addEventListener('click', () => {
	setDisplay(2);
});
btn3.addEventListener('click', () => {
	setDisplay(3);
});
btn4.addEventListener('click', () => {
	setDisplay(4);
});
btn5.addEventListener('click', () => {
	setDisplay(5);
});
btn6.addEventListener('click', () => {
	setDisplay(6);
});
btn7.addEventListener('click', () => {
	setDisplay(7);
});
btn8.addEventListener('click', () => {
	setDisplay(8);
});
btn9.addEventListener('click', () => {
	setDisplay(9);
});
btn0.addEventListener('click', () => {
	setDisplay(0);
});
btnDec.addEventListener('click', () => {
	// Ensures user cannot input more than one decimal per operand.
	if(!(display.includes('.'))){
		setDisplay('.');
	}
	
});
btnAdd.addEventListener('click', () => {
	document.getElementById("+").style.backgroundColor = 'darkGrey';

	// Allows user to change operation mid expression.
	if(operand1 != '' && display == ''){
		operator = '+'
		document.getElementById("-").style.backgroundColor = '';
		document.getElementById("*").style.backgroundColor = '';
		document.getElementById("/").style.backgroundColor = '';
		
		return;
	}

	// Allows user to evaluate multiple expressions without hitting '='
	if(operand1 != ''){
		evaluate(display);
		operator = '+'
	}
	
	// Processes first number entered.
	if(display != ''){
		operand1 = parseFloat(display);
	}

	operator = '+';

	display = '';
});
btnSub.addEventListener('click', () => {
	document.getElementById("-").style.backgroundColor = 'darkGrey';

	// Allows user to change operation mid expression.
	if(operand1 != '' && display == ''){
		operator = '-'
		document.getElementById("+").style.backgroundColor = '';
		document.getElementById("*").style.backgroundColor = '';
		document.getElementById("/").style.backgroundColor = '';
		
		return;
	}

	if(operand1 != ''){
		evaluate(display);
		operator = '-'
	}
	
	if(display != ''){
		operand1 = parseFloat(display);
	}
	operator = '-';

	display = '';
});
btnMult.addEventListener('click', () => {
	document.getElementById("*").style.backgroundColor = 'darkGrey';

	// Allows user to change operation mid expression.
	if(operand1 != '' && display == ''){
		operator = '*'
		document.getElementById("-").style.backgroundColor = '';
		document.getElementById("+").style.backgroundColor = '';
		document.getElementById("/").style.backgroundColor = '';
		
		return;
	}
	
	if(operand1 != ''){
		evaluate(display);
		operator = '*'
	}
	
	if(display != ''){
		operand1 = parseFloat(display);
	}
	operator = '*';

	display = '';
});
btnDiv.addEventListener('click', () => {
	document.getElementById("/").style.backgroundColor = 'darkGrey';

	// Allows user to change operation mid expression.
	if(operand1 != '' && display == ''){
		operator = '/'
		document.getElementById("-").style.backgroundColor = '';
		document.getElementById("*").style.backgroundColor = '';
		document.getElementById("+").style.backgroundColor = '';
		
		return;
	}

	if(operand1 != ''){
		evaluate(display);
		operator = '/'
	}
	
	if(display != ''){
		operand1 = parseFloat(display);
	}
	operator = '/';

	display = '';
});
btnEval.addEventListener('click', () => {
	evaluate(display);
	
	
});
btnAC.addEventListener('click', () => {
	clear();
});





//FUNCTIONS
// Sets the display after hitting numerical buttons.
function setDisplay(num){
	display += num;
	document.getElementById('display').innerHTML = display;
}

// For when user hits '='
function evaluate(display){
	operand2 = parseFloat(display);
	operate(operand1,operand2,operator);
	operand1 = display;
	operator = '';
	display = '';
}

// For when clear button is hit, or reset after divide by zero.
function clear(){
	display = '';
	document.getElementById('display').innerHTML = 'Simple Calculator';
	operand1 = 0;
	operand2 = 0;
	operator = '';
	document.getElementById("+").style.backgroundColor = '';
	document.getElementById("-").style.backgroundColor = '';
	document.getElementById("*").style.backgroundColor = '';
	document.getElementById("/").style.backgroundColor = '';
}

// Ensures proper operator functions are called.
function operate(num1, num2, operator){
	switch (operator){
		case '+':
			display = add(num1,num2);
			document.getElementById('display').innerHTML = display;	
			document.getElementById("+").style.backgroundColor = '';
			break;
		case '-':
			display = sub(num1,num2);
			document.getElementById('display').innerHTML = display;
			operand1 = 0;
			document.getElementById("-").style.backgroundColor = '';
			break;
		case '*':
			display = mult(num1,num2);
			document.getElementById('display').innerHTML = display;
			operand1 = 0;
			document.getElementById("*").style.backgroundColor = '';
			break;
		case '/':
			display = div(num1,num2);
			document.getElementById('display').innerHTML = display;
			if(display == 'Good try, punk.'){
				display = '';
			}
			operand1 = 0;
			document.getElementById("/").style.backgroundColor = '';
			break;
		default:
			break;
	}

}

// Basic math functions that each add,subtract,multiply, and divide two numbers.
function add(a, b){
	let c = a+b;
	
	return c;
}
function sub(a,b){
	let c = a-b;
	
	return c;
}
function mult(a,b){
	let c = a*b;

	return c;
}
function div(a,b){
	// If dividing by zero, clear operators and start calc fresh.
	if(b==0){
		clear();
		//document.getElementById('display').innerHTML = 'Good try, punk.';
		return 'Good try, punk.';
	}

	let c = a/b;

	return c;
}