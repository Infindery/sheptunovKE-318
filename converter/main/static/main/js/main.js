function showFile() {
	var title = document.querySelector('.title');
	var subtitle = document.querySelector('.subtitle');
	var input = document.querySelector('#id_file');
	var btn = document.querySelector('.btn');
	var link = document.querySelector('.link');

	// console.log(input.files[0].slice(-5)[0]);
	if (input.files[0].name.split('.').slice(-1)[0] === 'docx') {
		title.textContent = 'Скачивание файла';
		subtitle.textContent = 'Загрузка начнётся в ближайшее время. Пожалуйста, дождитесь её окончания';
		input.style.display = 'None';
		btn.style.display = 'None';
		link.style.display = 'Inline-block';
	}
}