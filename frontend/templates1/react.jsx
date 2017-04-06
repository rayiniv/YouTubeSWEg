function formatName(user) {
  return user.firstName + ' ' + user.lastName;
}

const user = {
  firstName: 'Harper',
  lastName: 'Perez'
};

const page = (
	<div class="row">
	   Hello, {formatName(user)}!
	</div>
);

function renderTable() {
ReactDOM.render(
  page,
  document.getElementById('root')
);
}

function sortBy() {
	console.log("fdfdsf");
}